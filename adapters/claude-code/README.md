# Claude Code adapter

What Claude Code gets so that it applies the spec: **memory** as a section
of `CLAUDE.md`, **gates** as hooks in `settings.json`, **proof** as a
scenario list run once per Claude Code version.

`CLAUDE.section.md` and `PROOF.md` are rendered from `SPEC.md` and
`proof/scenarios.md` by `tools/render-adapters`; edit those sources and
re-render, never the rendered files. `hooks/gate.py`,
`settings.snippet.json` and this README are written by hand.

## Memory

Append `CLAUDE.section.md` to `~/.claude/CLAUDE.md` (every project) or to
a project's `CLAUDE.md`. It is rendered from spec sections 1, 2.1, 2.2,
2.3 and 2.5 by default. A `CLAUDE.md` that already states its tool and
agent conventions in its own words wants only the by-moment checks: render
with `--sections 2.1,2.2,2.3,2.5`. A `CLAUDE.md` that has nothing yet
wants everything: `--sections 1,2.1,2.2,2.3,2.4,2.5,2.6`.

Re-render after every spec change and replace the section wholesale; the
stamp in its second line names the spec it came from, so a stale section
is visible.

## Gates

`hooks/gate.py` is one Python file (3.9+, standard library) with three
modes, wired by `settings.snippet.json`:

- `pre-write` (Write and Edit) **refuses** a GNU-only flag in a shell
  file, a secret literal, a mutable default in a Python signature, and
  `sudo` in a script -- exit 2, one line per finding naming the check.
- `pre-bash` **refuses** `sudo`, a forced push, a secret literal on the
  command line, and a known long command piped straight into
  tail/head/grep without a capture.
- `post-write` is **advisory**: it runs ruff and pyright (Python) or
  shellcheck and the shell's `-n` (shell) when they are installed, and
  prints the findings as context; it never refuses.

Block only what is never right; everything else is advice. A gate that
fails internally does not refuse either: it prints one line and lets the
call through, so a bug in the gate cannot stop work.

`python3 hooks/gate.py --run-tests` runs its tests (TAP);
`python3 hooks/gate.py --version` prints the hash of the running file.

## Proof, step by step

1. Install the memory (above) and merge `settings.snippet.json` into
   `settings.json`, with `<checkout>` replaced by the repository's
   absolute path; start a new Claude Code session.
2. Step 0, memory: ask the agent to quote the first line of the CODE
   DESIGN section of its `CLAUDE.md`. If it cannot, the section is not
   loaded.
3. Step 0, gates: ask the agent to write a scratch shell file containing
   `head -5 x`. The Write must be refused with
   `[shell mechanics (BSD userland)]` named; the agent sees the refusal
   in its transcript.
4. Run the scenarios in `PROOF.md` (one task each; observe the stated
   behaviour). Append under `Runs`: Claude Code version, date,
   passed/failed.
5. Re-run steps 2-3 after a Claude Code update before trusting the rest.
