# code-quality-spec

A portable, model-agnostic specification that an AI coding agent reads
once and turns into three things for the harness it runs in: **memories**
(checks it applies while writing), **gates** (checks the harness or the
repository enforces) and **proof** (how anyone can see that both
happened). A product name appears only in the adapters.

Two axes carry it. **KISS decides what to build**: complexity is the
enemy, an exception is a smell, errors are defined out of existence.
**CONSISTENCY proves it is what it says**: name, help, output, document
and behaviour are one claim -- and no decision is stated twice, because
two copies drift. Beneath both, one rule for every text: **CONCISE** --
intuitive (right at first reading), clear (only one reading), compact
(nothing the reader does not need).

## Files

| File | What it is |
|---|---|
| `SPEC.md` | the specification: principles, checks by the moment they fire, enforcement, adapters, site parameters |
| `SOURCES.md` | one page per source book: thesis, what shaped which check, what was not adopted |
| `notes/` | the reading notes behind `SOURCES.md`, one file per book, own words, page references |
| `proof/scenarios.md` | one task per check and the observable that shows it fired; harness-neutral |
| `tools/render-adapters` | renders every adapter from the spec; `--check` fails on a stale or hand-edited rendered file |
| `adapters/claude-code/` | Claude Code: memory section, `gate.py` + settings snippet, `PROOF.md`, README |
| `adapters/vscode-copilot/` | VS Code Copilot: repository set and user-profile set, pre-commit config, `PROOF.md`, README |

Rendered files are never edited by hand: edit `SPEC.md` or
`proof/scenarios.md`, run `python3 tools/render-adapters`.

## Use

- **Give an agent `SPEC.md`.** Its section 4 says how to render the
  adapter for the harness it is in and how to prove the result.
- **Claude Code, VS Code Copilot:** install and prove as the adapter's
  README says, in numbered steps.
- **Another harness:** memory = sections 1-2, gates = section 3 in that
  harness's hook or pre-commit mechanism, proof = `proof/scenarios.md`
  behind that harness's own "loaded?" step. Add it under `adapters/` and
  teach `tools/render-adapters` its file names.

## Site parameters

Five things differ per site -- the tool's name, the site configuration
directory, the per-user state and log roots, the shell dialect. The spec
names them in angle brackets and never their values; an adopter writes the
values once in a local file beside it. Nothing site-specific is here.

## Tooling

`tools/render-adapters` and `adapters/claude-code/hooks/gate.py`: Python
3.9+, standard library, same on macOS, Linux and Windows; each has
`--run-tests` (TAP) and `--version` (hash of its own bytes).

## Licence

CC BY 4.0 -- see `LICENSE`.
