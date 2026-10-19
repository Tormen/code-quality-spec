#!/usr/bin/env python3
"""Claude Code gates for the code-quality spec -- the mechanical half.

usage: gate.py [-h] [--version] [--run-tests [FILTER]] <pre-write|pre-bash|post-write>

Claude Code runs a hook with the tool call as JSON on standard input. A
gate that refuses exits 2 with the reason on standard error; everything
else exits 0. Only what is never right is refused (a GNU-only flag in a
shell script written for BSD userland, a secret literal in a command, a
mutable default in a Python signature, `sudo`, a forced push, a long
command piped straight into tail/head/grep without a capture); the
post-write gate is advisory: it runs the linters it finds and prints their
findings as context.

Standard library only, Python 3.9 or later; runs the same on macOS, Linux
and Windows (the BSD-flag check applies only to shell files).

settings.json (see settings.snippet.json beside this file):
  PreToolUse  Write|Edit -> python3 <path>/gate.py pre-write
  PreToolUse  Bash       -> python3 <path>/gate.py pre-bash
  PostToolUse Write|Edit -> python3 <path>/gate.py post-write
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import traceback
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

VERSION = "0.1"
EXIT_REFUSE = 2
EXIT_SOFTWARE = 70
EXIT_INTERRUPT = 130


class Err(Exception):
    def __init__(self, code: str, text: str, exit_code: int = 1) -> None:
        super().__init__(text)
        self.code = code
        self.text = text
        self.exit_code = exit_code


def err(code: str, text: str, exit_code: int = 1) -> Err:
    return Err(code, text, exit_code)


@dataclass(frozen=True)
class Finding:
    """One refusal: the check that fired and what it saw."""

    check: str
    what: str


# --- patterns ---------------------------------------------------------------

# GNU-only flags that fail on BSD userland (macOS). Checked in shell files only.
BSD_FLAGS: list[tuple[str, re.Pattern[str]]] = [
    ("head/tail -N (use -n N)", re.compile(r"\b(head|tail)\s+-\d+\b")),
    ("sed -r (use -E)", re.compile(r"\bsed\s+(-\w*\s+)*-r\b")),
    ("grep -P (use -E)", re.compile(r"\bgrep\s+(-\w*\s+)*-P\b")),
    ("xargs -r", re.compile(r"\bxargs\s+(-\w*\s+)*-r\b")),
    ("date -d", re.compile(r"\bdate\s+(-\w*\s+)*-d\b")),
    ("find -printf", re.compile(r"\bfind\b[^\n|;]*\s-printf\b")),
    ("stat -c", re.compile(r"\bstat\s+(-\w*\s+)*-c\b")),
]

# A secret literal on a command line or in code that builds one.
SECRET_LITERALS: list[tuple[str, re.Pattern[str]]] = [
    ("password literal", re.compile(r"(?i)(--?password|-p|--pass|-w)\s*[= ]?\s*['\"][^'\"\s]{4,}['\"]")),
    ("password=literal", re.compile(r"(?i)(password|passwd|pwd)\s*=\s*['\"][^'\"\s]{4,}['\"]")),
    ("token/key literal", re.compile(r"(?i)(api[_-]?key|token|secret)\s*=\s*['\"][A-Za-z0-9_\-]{16,}['\"]")),
    ("user:password in URL", re.compile(r"://[^/\s:@]+:[^/\s@]{4,}@")),
]

_DEF_OPEN = re.compile(r"\bdef\s+\w+\s*\(")
_MUTABLE_VALUE = re.compile(r"=\s*(\[\]|\{\}|set\(\)|list\(\)|dict\(\))")


def mutable_default(text: str) -> str | None:
    """The first parameter list holding a mutable default, or None.

    The parameter list is found by matching parentheses from the opening
    one to its closing one, so an assignment to an empty container in the
    BODY of the function is never mistaken for a default -- a regex that
    spanned the whole definition did exactly that, against this file.
    """
    for m in _DEF_OPEN.finditer(text):
        depth, i = 1, m.end()
        while i < len(text) and depth:
            c = text[i]
            if c in "([{":
                depth += 1
            elif c in ")]}":
                depth -= 1
            i += 1
        params = text[m.end():i - 1]
        v = _MUTABLE_VALUE.search(params)
        if v:
            return f"{text[m.start():m.end()]}... {v.group(0)}"
    return None
SUDO = re.compile(r"(^|[\s;&|(])sudo(\s|$)")
FORCED_PUSH = re.compile(r"\bgit\b[^\n;&|]*\bpush\b[^\n;&|]*(\s--force(-with-lease)?\b|\s-f\b|\s\+refs/|\s\+\w+(\s|$)|\s--mirror\b)")
# a known long-running command piped straight into a reader, with no capture
LONG_CMD = re.compile(r"(--run-tests|\bpytest\b|\bmake\b|\bnpm\s+test\b|\bcargo\s+(test|build)\b|\btox\b)")
STRAIGHT_PIPE = re.compile(r"\|\s*(tail|head|grep)\b")
CAPTURE = re.compile(r"\btee\b|(?<![\d&])>>?\s*(?!&)\S")  # a redirect to a FILE; `2>&1` is not a capture

SHELL_SUFFIXES = {".sh", ".bash", ".dash", ".zsh"}
SHEBANG_SHELL = re.compile(r"^#!\s*\S*/(env\s+)?(sh|dash|bash|zsh|ksh)\b")


def is_shell(path: str, text: str) -> bool:
    return Path(path).suffix in SHELL_SUFFIXES or bool(SHEBANG_SHELL.match(text))


def is_python(path: str, text: str) -> bool:
    return Path(path).suffix == ".py" or text.startswith("#!") and "python" in text.split("\n", 1)[0]


# --- the gates ---------------------------------------------------------------

_ALLOW = re.compile(r"gate:allow\s+([a-z-]+)")


def allowed(text: str) -> set[str]:
    """Checks a file opts out of, by a `gate:allow <check>` token in it.

    For files whose job is to contain the pattern -- a test fixture with a
    sample password, a document listing the forbidden flags. Used
    sparingly; the token is visible in review.
    """
    return set(_ALLOW.findall(text))


def check_write(path: str, text: str, on_disk: str = "") -> list[Finding]:
    """pre-write: what a Write's content or an Edit's new_string must not contain.

    `on_disk` is the file as it is before the call: an Edit's new_string
    is a fragment, so the file's `gate:allow` tokens and its shebang are
    read from there.
    """
    out: list[Finding] = []
    skip = allowed(text) | allowed(on_disk)
    shell = is_shell(path, text) or is_shell(path, on_disk)
    if shell and "bsd" not in skip:
        for name, pat in BSD_FLAGS:
            m = pat.search(text)
            if m:
                out.append(Finding("shell mechanics (BSD userland)", f"{name}: `{m.group(0).strip()}`"))
    if shell and "sudo" not in skip and SUDO.search(text):
        out.append(Finding("sudo", "a script of yours must not call sudo; run the privileged command and say it needs root"))
    if "secret" not in skip:
        for name, pat in SECRET_LITERALS:
            m = pat.search(text)
            if m:
                out.append(Finding("secret", f"{name}: `{m.group(0)[:40]}`"))
    if (is_python(path, text) or is_python(path, on_disk)) and "mutable-default" not in skip:
        hit = mutable_default(text)
        if hit:
            out.append(Finding("mutable default (B006)", f"`{hit}` -- use an immutable default or None"))
    return out


def check_bash(command: str) -> list[Finding]:
    """pre-bash: what a command the agent runs must not be."""
    out: list[Finding] = []
    if SUDO.search(command):
        out.append(Finding("sudo", "never run sudo; hand the command over, or write a rollout step"))
    if FORCED_PUSH.search(command):
        out.append(Finding("forced push", "a forced push only on the user's explicit instruction for that ref, in that turn"))
    for name, pat in SECRET_LITERALS:
        m = pat.search(command)
        if m:
            out.append(Finding("secret", f"{name}: `{m.group(0)[:40]}`"))
    if LONG_CMD.search(command) and STRAIGHT_PIPE.search(command) and not CAPTURE.search(command):
        out.append(Finding("capture first", "a long command is captured to a file (`> file 2>&1` or `| tee file`) and read from there; never piped straight into tail/head/grep"))
    return out


_SENTENCE_END = re.compile(r"(?<=[.!?])\s+")
_WORD = re.compile(r"[a-z0-9]+")
_SETTING = re.compile(r"`?([a-zA-Z]+(?:\.[a-zA-Z]+){2,})`?")
_FILE_SUFFIX = re.compile(r"\.(md|markdown|py|sh|json|ya?ml|toml|txt|html|js|ts)$", re.I)


def markdown_repeats(text: str) -> list[str]:
    """CONCISE applied to the whole file: a sentence stated twice, or a
    setting-like token (a.b.c) named in more than one section, is reported."""
    out: list[str] = []
    seen: dict[str, int] = {}
    body = "\n".join(ln for ln in text.splitlines() if not ln.startswith(("#", "|", "    ")))
    for raw in _SENTENCE_END.split(body):
        words = _WORD.findall(raw.lower())
        if len(words) < 8:
            continue
        key = " ".join(words)
        seen[key] = seen.get(key, 0) + 1
    for key, n in seen.items():
        if n > 1:
            out.append(f"sentence stated {n} times: \"{key[:70]}...\"")
    section = "(top)"
    where: dict[str, set[str]] = {}
    for ln in text.splitlines():
        if ln.startswith("#"):
            section = ln.lstrip("# ").strip()
            continue
        for m in _SETTING.finditer(ln):
            if _FILE_SUFFIX.search(m.group(1)):
                continue  # a file name, not a setting
            where.setdefault(m.group(1), set()).add(section)
    for tok, secs in sorted(where.items()):
        if len(secs) > 1:
            out.append(f"`{tok}` named in {len(secs)} sections: {', '.join(sorted(secs))}")
    return out


def advisory_post_write(path: str) -> str:
    """post-write: run the linters that exist for this file; never refuse."""
    p = Path(path)
    if not p.exists():
        return ""
    text = p.read_text(encoding="utf-8", errors="replace")
    if p.suffix.lower() in (".md", ".markdown"):
        reps = markdown_repeats(text)
        if reps:
            return f" >>> CONCISE check on {p.name} -- the whole file, not the paragraph just added:\n" + "\n".join(f"  {r}" for r in reps)
        return ""
    cmds: list[list[str]] = []
    if is_python(path, text):
        if shutil.which("ruff"):
            cmds.append(["ruff", "check", "--quiet", str(p)])
        if shutil.which("pyright"):
            cmds.append(["pyright", "--outputjson", str(p)])
    elif is_shell(path, text):
        m = SHEBANG_SHELL.match(text)
        dialect = m.group(2) if m else "sh"
        if shutil.which("shellcheck"):
            cmds.append(["shellcheck", "-s", "bash" if dialect == "zsh" else dialect, str(p)])
        if shutil.which(dialect):
            cmds.append([dialect, "-n", str(p)])
    lines: list[str] = []
    for cmd in cmds:
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=60, check=False)
        except (OSError, subprocess.TimeoutExpired) as e:
            lines.append(f" >>> {cmd[0]}: could not run ({e})")
            continue
        if r.returncode != 0:
            body = (r.stdout or r.stderr).strip()
            if cmd[0] == "pyright":
                body = _pyright_summary(body)
            lines.append(f" >>> {cmd[0]} on {p.name} [rc {r.returncode}]:\n{body}")
    return "\n".join(lines)


def _pyright_summary(output: str) -> str:
    try:
        data: dict[str, Any] = json.loads(output)
    except json.JSONDecodeError:
        return output[:2000]
    diags: list[dict[str, Any]] = data.get("generalDiagnostics", [])
    rows = [
        f"  {d.get('range', {}).get('start', {}).get('line', 0) + 1}: {d.get('severity')}: {d.get('message', '').splitlines()[0]}"
        for d in diags[:20]
    ]
    return "\n".join(rows) if rows else output[:500]


# --- hook plumbing ----------------------------------------------------------

def read_tool_call(stream: str) -> dict[str, Any]:
    try:
        data: Any = json.loads(stream or "{}")
    except json.JSONDecodeError as e:
        raise err("00001", f"hook input is not JSON: {e.msg}") from e
    if not isinstance(data, dict):
        raise err("00002", "hook input is not a JSON object")
    return data  # pyright: ignore[reportUnknownVariableType]


def refuse(findings: list[Finding], mode: str) -> int:
    if not findings:
        return 0
    print(f"REFUSED by gate {mode} -- {len(findings)} finding(s); each names the check:", file=sys.stderr)
    for f in findings:
        print(f"  [{f.check}] {f.what}", file=sys.stderr)
    return EXIT_REFUSE


def run_mode(mode: str, call: dict[str, Any]) -> int:
    tool_input: dict[str, Any] = call.get("tool_input") or {}
    if mode == "pre-write":
        path = str(tool_input.get("file_path", ""))
        text = str(tool_input.get("content", tool_input.get("new_string", "")))
        on_disk = ""
        if path and Path(path).is_file():
            on_disk = Path(path).read_text(encoding="utf-8", errors="replace")
        return refuse(check_write(path, text, on_disk), mode)
    if mode == "pre-bash":
        return refuse(check_bash(str(tool_input.get("command", ""))), mode)
    if mode == "post-write":
        out = advisory_post_write(str(tool_input.get("file_path", "")))
        if out:
            print(out)
        return 0
    raise err("00003", f"unknown mode {mode!r}; one of pre-write, pre-bash, post-write")


def build_id() -> str:
    return hashlib.sha256(Path(__file__).resolve().read_bytes()).hexdigest()[:12]


# --- tests -----------------------------------------------------------------
# gate:allow secret
# gate:allow mutable-default
# -- the fixtures below contain sample passwords and mutable defaults on purpose

def t_bsd_flags_in_shell_only() -> None:
    assert check_write("x.sh", "#!/bin/dash\nhead -5 f\n"), "head -5 in a shell file must be refused"
    assert not check_write("x.sh", "#!/bin/dash\nhead -n 5 f\n")
    assert not check_write("notes.md", "run head -5 f\n"), "prose is not a shell file"
    assert check_write("tool", "#!/usr/bin/env dash\nsed -r 's/a/b/' f\n")
    assert not check_write("tool", "#!/usr/bin/env dash\nsed -E 's/a/b/' f\n")


def t_allow_token_exempts_one_check() -> None:
    fixture = "# gate:allow secret\nSAMPLE = \"password = 'hunter22'\"\n"
    assert not check_write("test_x.py", fixture)
    assert check_write("test_x.py", fixture + "def f(a=[]): pass\n"), "other checks still apply"
    assert check_write("test_x.py", "SAMPLE = \"password = 'hunter22'\"\n"), "no token, no exemption"
    # an Edit's fragment carries no token: it is read from the file on disk
    assert not check_write("test_x.py", "X = \"password = 'hunter22'\"\n", on_disk="# gate:allow secret\n")


def t_secret_literals_refused_anywhere() -> None:
    assert check_write("run.sh", "mysql -u root -p'hunter22' db\n")
    assert check_write("conf.py", "password = 'hunter22'\n")
    assert check_bash("curl https://u:secretpw@host/x")
    assert not check_bash("read -rs PW; printf '%s' \"$PW\" | tool --stdin-pass")
    assert not check_write("conf.py", "password = os.environ['PW']\n")


def t_mutable_default_python_only() -> None:
    assert check_write("a.py", "def f(x, items=[]):\n    pass\n")
    assert check_write("a.py", "def f(x: int, m: dict[str, int] = {}) -> None: ...\n")
    assert not check_write("a.py", "def f(x, items=()):\n    pass\n")
    assert not check_write("a.sh", "def f(x, items=[]):\n")
    # the false positive the gate once raised against its own source
    assert not check_write("a.py", 'def g(text: str) -> list[str]:\n    """doc"""\n    out: list[str] = []\n    return out\n')
    assert check_write("a.py", "def h(a: dict[str, int] = {}, b=(1,)) -> None:\n    x = []\n")


def t_sudo_and_forced_push() -> None:
    assert check_bash("sudo chmod 750 x")
    assert check_bash("git push --force origin main")
    assert check_bash("git push origin +main")
    assert check_bash("git push -f")
    assert not check_bash("git push origin HEAD")
    assert not check_bash("echo pseudocode")
    assert not check_bash("git log --format=%f")


def t_long_command_needs_capture() -> None:
    assert check_bash("./tool --run-tests 2>&1 | tail -n 2")
    assert not check_bash("./tool --run-tests > /tmp/t.log 2>&1; tail -n 2 /tmp/t.log")
    assert not check_bash("./tool --run-tests 2>&1 | tee /tmp/t.log | tail -n 2")
    assert not check_bash("ls | head -n 3")


def t_hook_input_parsing() -> None:
    assert read_tool_call("") == {}
    call = read_tool_call('{"tool_name":"Write","tool_input":{"file_path":"a.sh","content":"head -3 f"}}')
    assert run_mode("pre-write", call) == EXIT_REFUSE
    call = read_tool_call('{"tool_name":"Bash","tool_input":{"command":"ls"}}')
    assert run_mode("pre-bash", call) == 0
    try:
        read_tool_call("[1,2]")
    except Err as e:
        assert e.code == "00002"
    else:
        raise AssertionError("array accepted")


def t_markdown_repeats_whole_file() -> None:
    s = "The setting is added to the user profile so that every workspace sees the rules."
    doc = f"# A\n\n{s}\n\n## B\n\nUse `chat.instructions.locations` here.\n\n## C\n\n{s}\n\nSet `chat.instructions.locations` again.\n"
    reps = markdown_repeats(doc)
    assert any(r.startswith("sentence stated 2 times") for r in reps), reps
    assert any("named in 2 sections" in r for r in reps), reps
    assert not markdown_repeats("# A\n\nOne short line.\n\n## B\n\nAnother different sentence with enough words in it.\n")
    assert not markdown_repeats("# A\n\n| x | y |\n| x | y |\n"), "tables are not prose"
    assert not markdown_repeats("# A\n\nSee `python.instructions.md`.\n\n## B\n\nAlso `python.instructions.md`.\n"), "a file name is not a setting"


def t_post_write_is_advisory() -> None:
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "bad.sh"
        p.write_text("#!/bin/dash\nif [ $x = 1 ]; then echo $y fi\n", encoding="utf-8")
        call = {"tool_input": {"file_path": str(p)}}
        assert run_mode("post-write", call) == 0, "advisory never refuses"


TESTS: list[tuple[str, Callable[[], None]]] = [
    ("bsd flags in shell only", t_bsd_flags_in_shell_only),
    ("allow token exempts one check", t_allow_token_exempts_one_check),
    ("secret literals refused anywhere", t_secret_literals_refused_anywhere),
    ("mutable default python only", t_mutable_default_python_only),
    ("sudo and forced push", t_sudo_and_forced_push),
    ("long command needs capture", t_long_command_needs_capture),
    ("hook input parsing", t_hook_input_parsing),
    ("markdown repeats whole file", t_markdown_repeats_whole_file),
    ("post-write is advisory", t_post_write_is_advisory),
]


def run_tests(filt: str | None) -> int:
    defined = sorted(n for n in globals() if n.startswith("t_"))
    listed = sorted(f.__name__ for _, f in TESTS)
    if defined != listed:
        print(f"not ok 0 - test list incomplete: {sorted(set(defined) ^ set(listed))}")
        return 1
    chosen = [(t, f) for t, f in TESTS if not filt or filt in t]
    print(f"1..{len(chosen)}")
    failed = 0
    for k, (title, fn) in enumerate(chosen, 1):
        try:
            # the refusals print to stderr; silence them inside the suite
            real = sys.stderr
            sys.stderr = open(tempfile.gettempdir() + "/gate-test.err", "w", encoding="utf-8")
            try:
                fn()
            finally:
                sys.stderr.close()
                sys.stderr = real
            print(f"ok {k} - {title}")
        except Exception as e:  # noqa: BLE001 -- a runner reports
            failed += 1
            print(f"not ok {k} - {title}: {e!r}")
    return 1 if failed else 0


# --- main ------------------------------------------------------------------

def main(argv: list[str]) -> int:
    if "--version" in argv:
        print(f"gate.py {VERSION} (build {build_id()})")
        return 0
    if "--run-tests" in argv:
        i = argv.index("--run-tests")
        filt = argv[i + 1] if i + 1 < len(argv) and not argv[i + 1].startswith("-") else None
        return run_tests(filt)
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip().split("\n\n", 1)[0] if __doc__ else "")
        print("\nusage: gate.py [-h] [--version] [--run-tests [FILTER]] <pre-write|pre-bash|post-write>")
        return 0 if argv else 1
    return run_mode(argv[0], read_tool_call(sys.stdin.read()))


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        print("gate.py: interrupted (Ctrl-C) -- the tool call was not judged; nothing was changed", file=sys.stderr)
        sys.exit(EXIT_INTERRUPT)
    except Err as e:
        print(f"ERROR {e.code} [{e.exit_code}]: {e.text}", file=sys.stderr)
        sys.exit(e.exit_code)
    except Exception:  # noqa: BLE001 -- one line + a trace file, never a stack on screen
        trace = Path(tempfile.gettempdir()) / "gate.trace"
        trace.write_text(traceback.format_exc(), encoding="utf-8")
        print(f"ERROR 00004 [{EXIT_SOFTWARE}]: unexpected failure in the gate -- trace in {trace}; the tool call was NOT refused", file=sys.stderr)
        sys.exit(0)
