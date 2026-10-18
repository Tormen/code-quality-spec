# VS Code Copilot adapter

What a repository gets so that GitHub Copilot in VS Code applies the spec:
**memory** as instruction files, **gates** as a pre-commit configuration,
**proof** as a scenario list you run once per Copilot version.

Everything under `.github/` and `AGENTS.md` here is rendered from
`SPEC.md` by `tools/render-adapters`; edit the spec, re-render, never these
files. `.pre-commit-config.yaml` and this README are written by hand.

## Apply to EVERY VS Code session (user profile) -- the usual choice

A repository install reaches one project. To have the rules in every
workspace, Copilot reads instruction files from the **user profile** as
well; the `user-profile/` directory here holds the same texts in that form
(the repo-wide file and `AGENTS.md` become instruction files with
`applyTo: "**"`, since the profile has no equivalent of either).

Two ways, the first preferred because the files then follow `git pull`:

1. Point VS Code at this directory: in user settings,
   `chat.instructionsFilesLocations` gets the absolute path of
   `adapters/vscode-copilot/user-profile` of your checkout, set to `true`.
   Nothing is copied; a re-render or a pull updates every session.
2. Or copy the five files into the profile's prompts folder, where
   "Chat: New Instructions File -> User" also writes:
   macOS `~/Library/Application Support/Code/User/prompts/`,
   Linux `~/.config/Code/User/prompts/`,
   Windows `%APPDATA%\Code\User\prompts\`. Copies go stale; re-copy after
   every render.

Either way, step 0 of `PROOF.md` must show the files in the references
list of an answer given in a workspace that has NO `.github/` of its own --
that is the proof they come from the profile. A repository's own
`.github/copilot-instructions.md` is applied in addition, not instead.

## Install into a repository

1. Copy `.github/` and `AGENTS.md` to the repository root, keeping the
   paths (`.github/copilot-instructions.md`,
   `.github/instructions/*.instructions.md`, `AGENTS.md`).
2. Make sure the VS Code setting
   `github.copilot.chat.codeGeneration.useInstructionFiles` is on (it is
   the default in current releases).
3. Copy `.pre-commit-config.yaml`, install `pre-commit`, run
   `pre-commit install`. Adjust the ruff selection and the pyright
   invocation to the project; keep the `render-adapters --check` hook only
   in repositories that carry the spec itself.
4. Run `PROOF.md` once: step 0 first (the references list under a
   Copilot answer must show the instruction files), then the scenarios.
   Append the run (Copilot version, VS Code version, date, result) under
   `Runs`.

## Proof, step by step

1. User settings: add the absolute path of
   `<checkout>/adapters/vscode-copilot/user-profile` to
   `chat.instructionsFilesLocations` (value `true`); confirm
   `github.copilot.chat.codeGeneration.useInstructionFiles` is on.
2. Open a folder that has **no** `.github/` of its own. Ask Copilot Chat
   anything. Expand the references list under the answer:
   `code-quality.instructions.md` and `agent.instructions.md` must be
   listed. This is step 0 -- it proves the profile set is applied in
   every workspace.
3. Open a `.py` file and ask again: `python.instructions.md` and
   `tool-face.instructions.md` join the list.
4. Run the scenarios in `PROOF.md` (one task each; observe the stated
   behaviour). Append under `Runs`: Copilot version, VS Code version,
   date, passed/failed.
5. If step 0 fails -- wrong path, a glob that does not match, or the
   setting is off -- fix that and repeat before trusting anything else.

## How the memory is split, and why

Copilot sends `.github/copilot-instructions.md` with **every** request, so
it carries only what applies to every edit: the two axes, the CONCISE rule
and the by-moment checks. Long files there lose effect.

Path-scoped files are applied only when a matching file is in the
context: `python.instructions.md` (`**/*.py`) carries the Python checks
and the linter codes; `tool-face.instructions.md` (`**/*.py,**/*.sh`)
carries the command-line, output, error and configuration checks;
`shell.instructions.md` (`**/*.sh`) the shell mechanics.

`AGENTS.md` is read by Copilot's agent mode and coding agent (and by other
agents that honour the file): it holds how the agent itself works --
explaining, running commands, documenting, committing, talking to the user.

## Gates

Copilot has no hook that runs on an edit, so every mechanical check is the
repository's: `.pre-commit-config.yaml` runs ruff with the rules the spec
names (`BLE001`, `FBT001`/`FBT002`, `B006`, `ANN401` and the project's
selection), pyright in strict mode, shellcheck and a syntax check for
shell, and a secrets scan. A harness that ignores its memory still cannot
commit the violation.

## Limits, stated plainly

The file names, the `applyTo` key, the `chat.instructionsFilesLocations`
setting, the profile's prompts folder and the references list are
Copilot's mechanisms as of mid-2026 and change often. The render script keeps each
harness's file names in one place; run step 0 of `PROOF.md` again after a
VS Code or Copilot update before trusting anything else.
