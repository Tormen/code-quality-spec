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

MUTABLE_DEFAULT = re.compile(r"def\s+\w+\s*\(.*?\w+\s*(?::\s*[^=]*?)?=\s*(\[\]|\{\}|set\(\)|list\(\)|dict\(\))", re.S)
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

def check_write(path: str, text: str) -> list[Finding]:
    """pre-write: what a Write's content or an Edit's new_string must not contain."""
    out: list[Finding] = []
    shell = is_shell(path, text)
    if shell:
        for name, pat in BSD_FLAGS:
            m = pat.search(text)
            if m:
                out.append(Finding("shell mechanics (BSD userland)", f"{name}: `{m.group(0).strip()}`"))
        if SUDO.search(text):
            out.append(Finding("sudo", "a script of yours must not call sudo; run the privileged command and say it needs root"))
    for name, pat in SECRET_LITERALS:
        m = pat.search(text)
        if m:
            out.append(Finding("secret", f"{name}: `{m.group(0)[:40]}`"))
    if is_python(path, text):
        m = MUTABLE_DEFAULT.search(text)
        if m:
            out.append(Finding("mutable default (B006)", f"`{m.group(0).strip()}` -- use an immutable default or None"))
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


def advisory_post_write(path: str) -> str:
    """post-write: run the linters that exist for this file; never refuse."""
    p = Path(path)
    if not p.exists():
        return ""
    text = p.read_text(encoding="utf-8", errors="replace")
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
        return refuse(check_write(path, text), mode)
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

def t_bsd_flags_in_shell_only() -> None:
    assert check_write("x.sh", "#!/bin/dash\nhead -5 f\n"), "head -5 in a shell file must be refused"
    assert not check_write("x.sh", "#!/bin/dash\nhead -n 5 f\n")
    assert not check_write("notes.md", "run head -5 f\n"), "prose is not a shell file"
    assert check_write("tool", "#!/usr/bin/env dash\nsed -r 's/a/b/' f\n")
    assert not check_write("tool", "#!/usr/bin/env dash\nsed -E 's/a/b/' f\n")


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


def t_post_write_is_advisory() -> None:
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "bad.sh"
        p.write_text("#!/bin/dash\nif [ $x = 1 ]; then echo $y fi\n", encoding="utf-8")
        call = {"tool_input": {"file_path": str(p)}}
        assert run_mode("post-write", call) == 0, "advisory never refuses"


TESTS: list[tuple[str, Callable[[], None]]] = [
    ("bsd flags in shell only", t_bsd_flags_in_shell_only),
    ("secret literals refused anywhere", t_secret_literals_refused_anywhere),
    ("mutable default python only", t_mutable_default_python_only),
    ("sudo and forced push", t_sudo_and_forced_push),
    ("long command needs capture", t_long_command_needs_capture),
    ("hook input parsing", t_hook_input_parsing),
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
