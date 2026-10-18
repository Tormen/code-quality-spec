# code-quality-spec

A portable, model-agnostic specification that an AI coding agent reads
once and turns into three things for the harness it runs in: **memories**
(checks it applies while writing), **gates** (checks the harness or the
repository enforces) and **proof** (how anyone can see that both
happened). Written for any model and any harness; a product name appears
only in the adapters.

Two axes carry it. **KISS decides what to build** -- complexity is the
enemy, an exception is a smell, errors are defined out of existence.
**CONSISTENCY proves it is what it says** -- a name, a help text, a
printed conclusion, a document and the behaviour behind them are one
claim; and no decision is stated twice, because two copies drift. Beneath
both, one ground rule for every text: **CONCISE** -- intuitive (right at
first reading), clear (only one reading), compact (nothing the reader does
not need).

## Files

| File | What it is |
|---|---|
| `SPEC.md` | the specification: principles, the checks by the moment they fire, what a machine enforces, how adapters are made, the site parameters |
| `SOURCES.md` | one page per source book: thesis, what shaped which check, what was read and not adopted |
| `notes/` | the reading notes behind SOURCES.md: one file per book read in full, chapter by chapter, in our own words, with page references -- the evidence for every pointer in SOURCES.md |
| `proof/scenarios.md` | one task per check and the observable that shows it fired; harness-neutral |
| `tools/render-adapters` | renders every adapter from the spec; `--check` fails when a rendered file was edited by hand or is stale |
| `adapters/claude-code/` | Claude Code: `CLAUDE.section.md` (memory), `hooks/gate.py` + `settings.snippet.json` (gates), `PROOF.md` |
| `adapters/vscode-copilot/` | VS Code Copilot: a per-repository set and a user-profile set for every workspace (memory), `.pre-commit-config.yaml` (gates), `PROOF.md` |

The rendered files inside `adapters/` are never edited by hand: edit
`SPEC.md` or `proof/scenarios.md` and run `python3 tools/render-adapters`.
That is the spec's own second face of CONSISTENCY, applied to itself.

## Use

- **As an agent's input.** Give the agent `SPEC.md`. Its section 4 tells
  the agent to render the adapter for the harness it is in, following the
  shape of the existing ones, and how to prove the result works: loaded?
  applied? enforced when not applied?
- **In Claude Code.** Append `adapters/claude-code/CLAUDE.section.md` to
  your `CLAUDE.md`, merge `settings.snippet.json` into `settings.json`,
  run `PROOF.md`. Details in `adapters/claude-code/README.md`.
- **In VS Code with Copilot.** Point the user setting
  `chat.instructionsFilesLocations` at `adapters/vscode-copilot/user-profile`
  of your checkout (every workspace), or copy the `.github/` set into one
  repository; install the pre-commit configuration; run `PROOF.md`.
  Details in `adapters/vscode-copilot/README.md`.
- **Another harness.** Render from the spec: the memory is sections 1-2,
  the gates are section 3 in that harness's hook or pre-commit mechanism,
  the proof is `proof/scenarios.md` with that harness's own "loaded?"
  step in front. Add it under `adapters/` and teach `tools/render-adapters`
  its file names.

## Site parameters

The spec names five things that differ per site -- the tool's name, the
site's configuration directory, the per-user state and log roots, the
shell dialect -- in angle brackets, and never their values. An adopter
writes the values once in a local file beside the spec; the table at the
end of `SPEC.md` says which check consumes each. Nothing site-specific is
in this repository.

## Tooling

`tools/render-adapters` and `adapters/claude-code/hooks/gate.py` are
Python 3.9 or later, standard library only, and run the same on macOS,
Linux and Windows. Each carries its tests (`--run-tests`, TAP output) and
prints the hash of its own bytes with `--version`. Gates refuse only what
is never right; everything else is advisory.

## Licence

CC BY 4.0 -- see `LICENSE`.
