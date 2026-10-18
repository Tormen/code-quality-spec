# Proof -- vscode-copilot

<!-- rendered by tools/render-adapters from proof/scenarios.md; do not edit here -- edit the scenarios and re-render. Append runs under 'Runs'. -->

## Step 0 -- loaded?

Copilot shows the instruction files it applied in the response's references list (expand it under the answer). Step 0: ask any question in Copilot Chat and confirm `.github/copilot-instructions.md` is listed; open a `.py` file and confirm `python.instructions.md` joins it; in agent mode confirm `AGENTS.md`. Absent means not applied: wrong path, a glob that does not match, or the setting `github.copilot.chat.codeGeneration.useInstructionFiles` is off. Nothing below counts until step 0 passes.

Harness-neutral. Each adapter's `PROOF.md` is rendered from this file with
that harness's own step 0 ("loaded?") in front. A scenario is a task you
give the agent in that harness, in a scratch project, and an observable
that shows the check fired. Record the run at the end of the adapter's
`PROOF.md`: harness, version, date, which scenarios passed.

Format: **check** -- *task* -> *observable*.

## BEFORE writing a unit

- **analogue** -- "Add a `--dry-run` option to this tool" (a tool that
  already has a `go`-guarded verb) -> the agent names the existing verb it
  copied the shape from, and proposes the `go` form instead of a flag, or
  says why not.
- **deep** -- "Add a function that returns the config directory" when a
  function already returns the whole config -> the agent declines the
  one-line forwarder, or merges it, and says so.
- **one owner** -- "Write the record to a second file in the same format"
  -> one writer that both call, not a second copy of the format.
- **plain call** -- "Add logging to the main entry point" -> the everyday
  call gains no new required argument; logging is on by default or behind
  one flag.
- **general vs special** -- "Make the helper skip empty names for this one
  caller" -> the skip goes into the caller, or the agent asks whether a
  domain rule says empty names are skipped everywhere.
- **twice** -- "Design the config key for retry intervals" -> two shapes
  are named (a number; a list; computed from measurements) and one line
  says which wins and why.
- **dependency** -- "Parse this YAML file" -> the agent asks whether the
  standard library format (JSON, TOML, INI) would do before adding a
  parser, and writes the one-line why if it adds one.

## WHILE writing the lines

- **errors out** -- "Handle the case that the output directory does not
  exist" -> the directory is created (`mkdir -p` semantics), not reported.
- **name** -- "Call this variable `data`" -> the agent proposes a name that
  says what the data is, or asks.
- **comment** -- "Add a comment to every line of this function" -> the
  agent refuses the per-line comments, keeps or adds the interface
  comment, and says why.
- **boundary** -- "Validate the port number again inside the send
  function" (it is validated at parse time) -> the agent declines the
  second validation and points at the first.
- **crash-safe** -- "Save the state file" -> written via temp file and
  rename, with the reason named.
- **secret** -- "Call the API with the token on the command line" -> the
  agent refuses the literal, offers stdin, a file or a prompt, and names
  the history-and-process-list reason.

## BEFORE committing

- **one kind** -- "Rename this function and change its return type in one
  commit" -> two commits proposed, each named for its kind.
- **pinned** -- "Change this untested function's behaviour" -> a
  characterisation test is written first and shown before the change.
- **adversarial** -- "Fix this off-by-one" -> the test is the input that
  fails today; the agent says what it did to confirm the test fails on the
  unfixed code.
- **tested at the right size** -- "Run the tests after this one-line fix"
  -> the filtered run, not the full suite; the full suite named for the
  milestone.
- **second run** -- "Write the installer" -> the agent runs it twice and
  shows the second run changes nothing.
- **clearer** -- a diff that touches a dense block -> the touched lines
  read no worse than before; tidying beyond the fix is its own commit.
- **scoped** -- "Commit" in a repository with a sibling's unrelated dirty
  file -> only the task's paths are committed, the sibling named and left.

## The tool's face

- **usage** -- "Write the help text" -> first line `usage: <name>
  [OPTIONAL] <MANDATORY>`.
- **verbs and flags** -- "Add a start command" -> `tool start`, not
  `--start`; a dashed verb answered with the verb.
- **go** -- "Add a command that deletes old records" -> two-step:
  `remove` shows, `remove go` does.
- **three layers of output** -- "Make it quieter" -> `-Q` silences
  narration only; errors stay; `-V` is a superset.
- **stderr** -- "Print the error" -> stderr, through the error helper.
- **raw beside conclusion** -- "Print OK when the sync is done" -> `OK`
  beside the value it was derived from.
- **no stack trace** -- "What happens on Ctrl-C?" -> one line, exit 130,
  cleanup; an unexpected error is one line, exit 70, trace in a file.
- **failure** -- "Report that the file is missing" -> one error call with a
  code unique to the line.
- **configuration** -- "Add a timeout setting" -> the agent asks whether
  the code can compute it; if kept, it lives in the config with a default,
  not in the code.
- **version** -- "Add --version" -> number, commit, and a hash of the
  running file.
- **self-test** -- "Add tests" -> inside the tool, `--run-tests`, TAP
  output, real collaborators, exact assertions.
- **state and logs** -- "Where do we keep the cache?" -> under the state
  root, never the log root or a temp directory.

## Python

- **unrepresentable** -- "Add a `mode: str` parameter with values fast or
  safe" -> a `Literal` or an `Enum`, not `str`.
- **shaped** -- "Return the name, size and date" -> one dataclass, not a
  tuple; frozen unless it must change.
- **parsed once** -- "Check inside `compute` that `size` is an int" -> the
  agent points at the boundary where it was parsed and declines.
- **composed** -- "Make `Admin` a subclass of `User` to reuse its fields"
  -> composition or a `Protocol` unless `Admin` behaves as a `User`.

## The agent itself

- **WHEN explaining** -- "Why did the job fail?" -> Situation, Observation
  (quoted), Suggestion with its why; inferred parts labelled.
- **WHEN running commands** -- a long test run -> captured to a file,
  swept for every anomaly word, run once.
- **WHEN documenting** -- "Note in the README that the bug is fixed" -> the
  README states the present behaviour, no "was broken" narrative.
- **WHEN committing** -- any commit -> no AI co-author trailer; own paths
  only.
- **WHEN talking to the user** -- "Can we drop the lock?" -> feasibility,
  then a recommendation with its reason; a numbered question if a decision
  remains.

## Runs

(harness, version, date, scenarios passed / failed)
