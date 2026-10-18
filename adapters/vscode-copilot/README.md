# VS Code Copilot adapter

Memory = instruction files, gates = a pre-commit configuration, proof = a
scenario list run once per Copilot version. Everything under `.github/`,
`AGENTS.md` and `user-profile/` is rendered from `SPEC.md` -- edit the
spec and re-render, never these files. `.pre-commit-config.yaml` and this
README are written by hand.

## Install for every workspace (the usual choice)

1. User settings: `chat.instructionsFilesLocations` -> add the absolute
   path of `<checkout>/adapters/vscode-copilot/user-profile`, value `true`.
   Nothing is copied; a `git pull` or a re-render updates every session.
2. Confirm `github.copilot.chat.codeGeneration.useInstructionFiles` is on
   (the default).

Alternative: copy the five `user-profile/` files into the profile's
prompts folder (macOS `~/Library/Application Support/Code/User/prompts/`,
Linux `~/.config/Code/User/prompts/`, Windows `%APPDATA%\Code\User\prompts\`).
Copies go stale; re-copy after every render.

## Install for one repository

1. Copy `.github/` and `AGENTS.md` to the repository root, paths kept.
2. Copy `.pre-commit-config.yaml`; `pip install pre-commit`;
   `pre-commit install`. Adjust the ruff selection and the pyright call to
   the project; drop the `render-adapters --check` hook unless the
   repository carries the spec itself.

A repository's files are applied in addition to the profile's, not instead.

## Prove it

1. In a folder with **no** `.github/` of its own, ask Copilot Chat
   anything; expand the references list under the answer:
   `code-quality.instructions.md` and `agent.instructions.md` must be
   listed. This is step 0: the profile set is loaded. Absent means wrong
   path, a glob that does not match, or the setting is off -- fix that
   before anything else.
2. Open a `.py` file, ask again: `python.instructions.md` and
   `tool-face.instructions.md` join the list.
3. Run the scenarios in `PROOF.md`; append under `Runs`: Copilot version,
   VS Code version, date, passed/failed.
4. Repeat step 1 after every VS Code or Copilot update.

## Why the memory is split

`.github/copilot-instructions.md` travels with **every** request, so it
carries only what applies to every edit (the two axes, CONCISE, the
by-moment checks). Path-scoped files apply only when a matching file is
in context: `python` (`**/*.py`), `tool-face` (`**/*.py,**/*.sh`),
`shell` (`**/*.sh`). `AGENTS.md` is what agent mode reads: how the agent
itself works. In the profile the first and the last become instruction
files with `applyTo: "**"`, since the profile has no equivalent of either.

## Gates

Copilot has no hook that runs on an edit, so every mechanical check is the
repository's: ruff with the spec's codes, pyright strict, shellcheck and
a shell syntax check, a secrets scan -- before every commit. A harness
that ignores its memory still cannot commit the violation.

## Limits

File names, `applyTo`, `chat.instructionsFilesLocations`, the prompts
folder and the references list are Copilot's mechanisms as of mid-2026
and change often; the render script keeps the file names in one place.
