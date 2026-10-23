---
applyTo: "**/*.py,**/*.sh"
---

# A command-line tool's face

<!-- rendered by tools/render-adapters from SPEC.md e1bd92090178; do not edit here -- edit the spec and re-render -->

## The tool's face (command line, output, errors, configuration)

- **usage** -- the first line of help is `usage: <name> [OPTIONAL]
  <MANDATORY>`; optionals in brackets first, mandatory arguments in angle
  brackets after.
- **verbs and flags** -- the thing to DO is a verb (`start`, `remove`);
  `--flags` only modify HOW. A dashed verb is answered ("no such option;
  you mean `tool start`"), never met with "unknown option". One spelling
  per command, no aliases. Administrative actions around the tool rather
  than its job (`--version`, `--create-config`, `--run-tests`) stay flags.
- **named for what it does** -- a flag names the action, not the resulting
  state, and not the mechanism (`--eject`, not `--keep-mounted`, not
  `--set-eject`); `--no-x` negates `--x` and nothing else. Where the
  configuration selects a different action, the OUTPUT says which one ran.
- **go** -- a verb that deletes, resets, overwrites or takes away runs in
  two steps: `tool verb ...` shows what it would do and changes nothing;
  `tool verb go ...` does exactly that. No `--force`, no "are you sure?"
  prompt: a prompt cannot be answered from a pipe, and the plain run is
  the review.
- **three layers of output** -- the default prints what it did, found and
  changed; `-V` adds to it (every default line still printed, plus each
  command echoed before it runs and the detail the default left out); `-Q`
  silences it, except errors, warnings and a confirmation a destructive
  action depends on. A tool that prints nothing until `-V` is broken, not
  quiet. Diagnostics (`-D`) are a separate axis from verbosity.
  *Test:* `tool` and `tool -V` never print the same; `tool -Q` with the log
  off prints nothing on a successful run.
- **stderr** -- errors and warnings go to stderr, always, through a helper
  no quiet flag can gate. Standard output is the result.
- **raw beside conclusion** -- a derived verdict is printed with the value
  it was derived from, when that value is already in hand and costs
  nothing: `OK [0]`, `healthy (3/3)`, `in sync (a1b2c3 = a1b2c3)`. In code,
  the same: when a function holds both a conclusion and its source, it
  compares them and refuses to print a contradiction.
- **concise messages** -- a runtime message longer than two lines moves its
  substance to help and leaves a one-line pointer (`--> see --emergency`).
- **names its reason** -- whatever the tool does without being asked
  (creates, rewrites, removes, moves) says what and why in one line of the
  default output, beside the thing itself.
- **adaptive** -- "smart" means the tool inspects the situation and shows
  what that situation calls for: one column whose content differs by kind
  of row; a table for many results and a record for one; a near-miss
  answered with what was evidently meant. Adding, never replacing, a
  default.
- **no stack trace** -- an unexpected error is ONE line with its code, what
  failed and where the full trace was written; exit 70. Interrupt (Ctrl-C)
  is an answer, not a crash: one line saying where it stopped and what that
  leaves, cleanup of temp files and locks, exit 130.
  *Test:* a real SIGINT at a prompt and a real unexpected error are both in
  the test suite.
- **failure** -- every failure is raised through ONE error call per tool
  that prints `ERROR <code> [<exit>]: <text>` to stderr and exits, where
  `<code>` is a short number unique to the raising source line, so that
  grepping the code lands on the line. The code survives every refactoring:
  deferred or batched work carries it along. Every report of what a run did
  or would do names the rule by its code.
  *Test:* no two raising lines share a code.
- **configuration** -- all runtime-tunable behaviour lives in one
  configuration file, sourced at start; the only place a default exists is
  the function `--create-config` prints from. Search order, first existing
  wins: an environment variable, `--config <file>`, `<site config dir>`,
  `~/.<name>.conf`, `/etc/<name>.conf`, `/usr/local/etc/<name>.conf`. When
  none exists the tool exits non-zero and offers the most common places to
  write one, each as a paste-ready line, the offer FILTERED from the same
  list the search iterates so it can never name a path the tool does not
  read. A variable holding the default of `X` is named `X_DEFAULT`. A
  parameter is added only when a user can choose better than the code can
  compute; one that stays has a default.
  *Test:* the offer's paths are a subset of the search paths.
- **version** -- `--version` identifies the exact bytes being run: the
  release number, the commit the file was stamped with, and a hash of the
  running file; a build inside a checkout prints `git describe` verbatim
  beside them, so any disagreement is visible. Two installs are compared by
  diffing their `--version`. The tool never knows where its own source
  lives.
- **self-test** -- the tool carries its test suite in its own file and runs
  it with `--run-tests [<filter>]`, reporting TAP-style (`1..N`, then one
  `ok`/`not ok` line per test as it ends). Each test sets up its own state;
  a filtered run passes alone. Every command example in help or README is
  run by the suite. Tests exercise real collaborators and mock only external
  systems (network, payment, clock); every assertion names its expectation
  and an exact value; a test that only asserts not-None or no-exception is
  not a test.
- **state and logs** -- a tool's persistent state (records, watermarks,
  caches, queues, flags) lives under `<per-user state dir>/<name>/`; its
  logs, and nothing else, under `<per-user log dir>/`. The split is strict:
  log directories get rotated and truncated, and state kept among logs dies
  with the first rotation policy that never knew it was there. Neither
  lives in a temp directory, and nothing of either is hard-coded: both
  roots come from the configuration, with these as their defaults.
  *Test:* no write outside the two roots and the temp directory; no state
  file under the log root.
- **notifies** -- a tool that sends mail or messages offers `--test-mail`
  (one message through exactly the real path, non-zero when nothing was
  sent), and a message that cannot go out now is queued and retried, marked
  late when delivered, never dropped.

