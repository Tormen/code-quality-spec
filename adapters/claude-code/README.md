# Claude Code adapter

Memory = a section of `CLAUDE.md`, gates = hooks in `settings.json`,
proof = a scenario list run once per Claude Code version.
`CLAUDE.section.md` and `PROOF.md` are rendered from `SPEC.md` and
`proof/scenarios.md` -- edit those and re-render, never the rendered
files. `hooks/gate.py`, `settings.snippet.json` and this README are
written by hand.

## Install

1. Append `CLAUDE.section.md` to `~/.claude/CLAUDE.md` (every project) or
   to a project's `CLAUDE.md`. Default content: spec sections 1, 2.1-2.3,
   2.5. A `CLAUDE.md` that already states its tool and agent conventions
   wants `--sections 2.1,2.2,2.3,2.5`; an empty one wants
   `--sections 1,2.1,2.2,2.3,2.4,2.5,2.6`.
2. Merge `settings.snippet.json` into `settings.json`, `<checkout>`
   replaced by the repository's absolute path (`python` instead of
   `python3` on Windows).
3. Start a new session.

After every spec change: re-render and replace the section wholesale. Its
second line carries the spec's stamp, so a stale section is visible.

## Gates

`hooks/gate.py` -- one Python file (3.9+, standard library), three modes:

- `pre-write` (Write, Edit) **refuses** a GNU-only flag in a shell file, a
  secret literal, a mutable default in a Python signature, `sudo` in a
  script: exit 2, one line per finding naming the check.
- `pre-bash` **refuses** `sudo`, a forced push, a secret literal, a known
  long command piped straight into tail/head/grep without a capture.
- `post-write` is **advisory**: runs ruff and pyright (Python) or
  shellcheck and the shell's `-n` (shell) when installed; for Markdown,
  reports a sentence stated twice or a setting named in more than one
  section (CONCISE, applied to the whole file); never refuses.

Only what is never right is refused. A file whose job is to contain a
pattern (a test fixture with a sample password) carries a line
`gate:allow <check>` -- `secret`, `bsd`, `sudo` or `mutable-default` --
and that one check is skipped for it; the token is visible in review. A
gate that fails internally prints one line and lets the call through, so
a bug in the gate cannot stop work.
`python3 hooks/gate.py --run-tests` (TAP); `--version` prints the hash of
the running file.

## Prove it

1. Memory: ask the agent to quote the first line of the CODE DESIGN
   section of its `CLAUDE.md`. If it cannot, the section is not loaded.
2. Gates: ask the agent to write a scratch shell file containing
   `head -5 x`. The Write must be refused with
   `[shell mechanics (BSD userland)]` named.
3. Run the scenarios in `PROOF.md`; append under `Runs`: Claude Code
   version, date, passed/failed.
4. Repeat steps 1-2 after every Claude Code update.
