# code-quality-spec

A specification that an AI coding agent reads once and turns into three
things for the harness it runs in: **memories** (checks it applies while
writing), **gates** (checks the harness or the repository enforces) and
**proof** (how anyone can see that both happened). It is written for any
model and any harness; a product name appears only in layer 4.

It is built in four layers, each shorter than the one below it:

| Layer | Holds | Names allowed |
|---|---|---|
| 1 Principles | the two axes and the one ground rule | none |
| 2 Checks | what to verify, at the moment it applies, each with a yes/no test | none |
| 3 Enforcement | for every check: judgement, or which tool decides it | tool names (ruff, pyright, shellcheck, git) |
| 4 Adapters | how 2 and 3 become memory, gates and proof in one harness | product names |

Site specifics -- host names, personal paths, the names of private tools --
appear nowhere. Where a check needs one (the directory a configuration is
read from, say) it names a **parameter** in angle brackets, and the
parameters are listed at the end with their meaning; their values live in a
local file beside this one, never in it.

Distilled from the author's own working rules and from: Ousterhout, *A
Philosophy of Software Design*; Hunt & Thomas, *The Pragmatic Programmer*;
Fowler, *Refactoring*; McConnell, *Code Complete*; Feathers, *Working
Effectively with Legacy Code*; Viafore, *Robust Python*; Slatkin, *Effective
Python*. Where the two sources say the same thing, the working rule's
wording and example win: they are proven on real tools.

---

## 1. Principles

Two axes carry everything below. Either alone produces confident, wrong
code: the first without the second gives simple lies, the second without
the first gives faithful complexity.

**KISS decides what to build.** Complexity is the enemy, and it is
incremental: it arrives one reasonable exception at a time. So an exception
is a smell, not a solution -- when a design starts needing "... except when
X", look for the one rule that covers both sides before adding a second
mechanism. Prefer the simplest thing that works; prefer deep units (a small
interface hiding real work) over many shallow ones; define errors out of
existence before handling them.
*Test:* is there a special case here that one more general rule would
remove?

**CONSISTENCY proves it is what it says.** A name, a help text, a printed
conclusion, a return value, a document and the behaviour behind them are
ONE claim, made in several places. Quality is the absence of any gap
between them: when they disagree, the behaviour is not "the truth" and the
rest "documentation" -- they are a lie the reader acts on. Applied, this
has two faces:

- *agreement* -- every place that states the claim states the same thing;
- *uniqueness* -- no decision is stated twice when once would do. A second
  copy is a second claim, and two claims drift: duplication is tomorrow's
  inconsistency.

*Test:* if the reader took this literally and nothing else, would they be
right? And: is this fact already stated somewhere that could be asked
instead?

**Ground rule for every text produced -- CONCISE = intuitive, clear and
compact.** It governs every channel: a tool's output and messages, help,
README, code comments, commit messages, designs, and the agent's own
replies. The three words are three tests, applied in order, and always
written with their parentheses:

- **intuitive** (right at first reading -- no decoding, nothing to look up),
- **clear** (only one reading, however closely one looks),
- **compact** (nothing that the reader does not need).

Intuitive and clear fail in opposite directions: a legal text is clear and
not intuitive; a flag called `--eject` over a setting that only unmounts is
intuitive and not clear. Compact never wins against the other two: a line
shortened until it needs decoding is not concise.

---

## 2. Checks

Each check names the moment it applies, says what must hold, and ends in a
*Test* answered yes or no on the diff. Checks are grouped by moment so that
they are applied in the edit, not remembered afterwards.

### 2.1 BEFORE writing a unit (a function, class, module, verb or flag)

- **analogue** -- the nearest existing thing in the tool (same read/write
  character, same scope, same destructiveness) is found, its shape copied,
  and named. When the analogue contradicts what taste proposed, the
  analogue wins, and the reply says so. Consistency is derived from the
  tool, never from preference.
  *Test:* the analogue is named.
- **deep** -- the body does real work behind a short signature. A unit that
  only forwards its arguments to a near-identical signature, or two units
  that can only be read together, is ONE unit: merge.
  *Test:* the body is clearly more than its signature and comment.
- **one owner** -- a format, path, constant, protocol detail or order of
  steps known to two places has ONE owner that the others ask. Code is split
  by what it KNOWS, not by when it runs: read / parse / write as three
  functions that all know the file format is one decision spread over three.
  *Test:* grep the literal; a hit outside its owner is a leak.
- **plain call** -- the everyday call carries no flag and no rarely used
  parameter; defaults cover it.
  *Test:* write the everyday call -- does it name anything it does not use?
- **general vs special** -- a shared helper knows nothing of any one
  caller; the special case sits in the caller, at the top. A special-case
  `if` inside a general helper is the KISS exception-smell in code.
  *Test:* a second, different caller could reuse the helper unchanged.
- **twice** -- for anything that outlives the change (a configuration key,
  a command-line verb, a function others call) a second, genuinely
  different shape is sketched, and one line says why the chosen one wins.
  *Test:* the alternative is named in the design or the reply.
- **dependency** -- standard library first; a third-party dependency is
  added only when it earns its place, and the tool then sets up its own
  environment on first use rather than asking anyone to install anything.
  *Test:* the dependency's one-line "why" is written where it is declared.

### 2.2 WHILE writing the lines

- **errors out** -- the operation is first defined so the edge case is
  simply covered (`mkdir -p`; removing what is already gone is done). A
  guard that every caller would repeat moves INTO the unit. What still
  reaches the caller is something the caller can act on, reported through
  the tool's one error call with its code (see "failure" in 2.4).
  *Test:* no guard repeated at two call sites.
- **name** -- one concept, one word, across the whole tool; named for what
  it does. A name that is hard to find means the unit does not do one clear
  thing: fix the split, not the name. One NAME is one MEANING: every
  consumer of a variable or flag is read before two uses of it are called
  the same.
  *Test:* a reader who sees ONLY the name guesses right.
- **comment** -- says what the code cannot: the interface comment says WHAT
  and WHY for the caller, never HOW; an inline comment gives the non-obvious
  why; a comment that repeats the code is deleted; a comment that must be
  long to be complete says the unit is too complex. Every comment, help
  line and README sentence is a CLAIM about behaviour: re-read in the SAME
  edit that changes the behaviour, and run by the test suite when it is a
  command.
  *Test:* delete the comment -- is anything lost that the code does not say?
- **boundary** -- external input (arguments, configuration, files, the
  network, another tool's output) is checked ONCE, where it enters; inside,
  invariants are asserted and a violation stops the run loudly -- a program
  that dies early tells no lies. Only REAL constraints reject: a bound that
  protects nothing is widened.
  *Test:* no value validated at two depths; every rejection names what
  would break.
- **crash-safe** -- a file is written as temp file + rename; a lock is an
  atomic `mkdir`; whatever state an interrupt leaves is one the next run
  takes up.
  *Test:* kill it mid-write and run it again: nothing lost, nothing doubled.
- **secret** -- a password, token or key never appears as a literal
  argument on a command line (shell history, process lists and synced
  dotfiles all record it): a prompt, standard input, a file, or a secret
  manager instead. A credential is stored only where every reader already
  had the capability it grants.
  *Test:* no secret literal in any command the tool runs or prints.

### 2.3 BEFORE committing

- **one kind** -- a commit is a refactoring (every test passes unchanged) OR
  a behaviour change (with its new test), never both; its message says
  which. Mixing them makes a regression impossible to locate.
  *Test:* the commit message names one of the two, and the diff is only that.
- **pinned** -- code that had no test got a characterisation test FIRST,
  one that records what it does NOW, right or wrong, through a seam (a
  parameter, a function boundary, a configuration key) that needed no edit
  to the logic.
  *Test:* a test touching the changed lines existed BEFORE the change.
- **adversarial** -- the test written for a fix is the input that makes the
  code answer confidently and wrongly, not the input that confirms it
  works; and after it passes, the fix is neutered in a copy and the test
  must fail against it. A test that passes before the fix certifies the
  bug.
  *Test:* the test fails on the neutered copy.
- **tested at the right size** -- while working, only the tests the change
  touches are run (`--run-tests <filter>`: seconds, not minutes); the FULL
  suite runs once before the code is USED -- at install or deployment, at a
  release, and before the commit that closes a slice of work -- and never
  on every small edit. A commit between those points rests on the filtered
  run and says so. A full run goes in the background like any long command.
  *Test:* the install, deployment or release path refuses without a full
  green run; no change triggered the full suite more than once.
- **second run** -- a tool that enforces or installs state is run twice
  before the commit.
  *Test:* the second run changes nothing and prints nothing to change.
- **clearer** -- the code the change TOUCHED is no harder to read than
  before; the tidying it prompted is a commit of its own (see "one kind").
  *Test:* read the touched lines as a stranger -- easier than before, or at
  least not harder.
- **scoped** -- a commit contains only the project it is about, and work is
  committed and pushed at each finished unit, never banked up. Unpublished
  work is invisible to every other machine and every other session, and
  drifts.
  *Test:* `git status` of the project is clean and not ahead when the task
  is called done.

### 2.4 The tool's face (command line, output, errors, configuration)

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
  read. A variable holding the default of `X` is named `X_DEFAULT`.
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
  run by the suite.
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

### 2.5 Python

Static typing is enforced by the type checker in strict mode (layer 3), and
the mechanical style checks are a linter's job, not a memory's. Three
checks need judgement:

- **unrepresentable** -- a value from a fixed set is a `Literal` or an
  `Enum`, never a bare `str`; two kinds of id that must not mix are a
  `NewType` each; constants are `Final`; `X | None` only where None is a
  real answer; a class with an invariant enforces it in `__post_init__`, so
  no broken instance can exist.
  *Test:* no `str`/`int` parameter whose valid values are a known set.
- **shaped** -- a record passed between functions is a dataclass
  (`frozen=True` unless it must change); more than two return values are
  one object, not a tuple; `TypedDict` only for a dict that crosses a
  boundary as JSON.
  *Test:* no `dict[str, Any]` and no 3-tuple crossing an internal boundary.
- **parsed once** -- arguments, configuration, JSON and other tools' output
  become typed objects at the boundary -- parsed, not merely validated, so
  the type carries the proof; inside, `isinstance` on the tool's own data
  is a smell. ("boundary", in Python.)
  *Test:* `isinstance` appears only in parsing code.

A failure is raised as the tool's one root exception carrying its code
(see "failure"), chained with `raise ... from e`; `except Exception` exists
at the top of `main` (where it becomes the one-line ERROR and the trace
file) and where a foreign library's failures are turned into that root
exception, nowhere else. A tool with third-party dependencies creates its
own virtual environment on first run and re-executes itself inside it,
saying so in one line.

### 2.6 The agent itself

The same two axes apply to how the agent works, not only to what it writes;
each group below names the axis and the face it is an instance of.

**WHEN explaining** *(CONSISTENCY, agreement: a cause stated as fact when it
was only inferred is a conclusion without its raw value; CONCISE: the
shape)* -- every explanation, finding or proposal has the shape
**Situation / Context** -> **Problem / Observation** -> **Solution /
Suggestion**, the last with its concise WHY ("like this, because ..."). One
line each where possible. Inside part 2, what was OBSERVED (quote it) is
kept apart from what is INFERRED (say so, and name the one check that would
prove or refute it); a diagnosis is a hypothesis until proven, and nothing
is force-quit, killed or reinstalled on a hypothesis -- "wait and look
again" is offered first. The Situation assumes nothing that exists only in
this conversation: a term coined along the way is replaced by the concrete
file, path or command. A prediction that turned out wrong is said to be
wrong, not reframed.

**WHEN running commands** *(CONSISTENCY, uniqueness: one run is one truth;
a second run to ask a second question is a second, different truth
compared as if it were the first; KISS: capture once, read many)* -- any
output that will be reasoned about is
captured to a file first and analysed from the file: size, a broad sweep
for every anomaly word (not only the one being chased), duplicates folded,
a diff against the last good run. One run answers every question; a
command is never run a second time to ask it a second thing. Anything that
may take longer than about fifteen seconds runs in the background. Every
tool is tested in the user's own environment (their `PATH`, their shell),
and a difference between the agent's result and the user's is an
environment finding first.

**WHEN documenting** *(CONSISTENCY, uniqueness: a resolved issue left
standing, or a design kept beside the docs it was folded into, is a second
and stale claim; CONCISE)* -- a document records present state, never
history:
a resolved issue is removed, not narrated. A design lives in a file, not in
the chat, is updated after every review comment, and is folded into the
real documentation and removed once built. Too much information kills the
information.

**WHEN committing** *(CONSISTENCY, uniqueness: unpublished work is a second
copy that drifts from the one every other machine sees; agreement: the
message says what the diff is)* -- own project only, scoped by path;
committed and
pushed at each finished unit; no AI co-author trailer; a forced push only
on an explicit instruction for that ref, never as the fix for a rejection.

**WHEN talking to the user** *(CONSISTENCY, agreement: what the agent says
it will do, declines, or has done is one claim with what it then does --
feasibility alone is not endorsement, and a silent deviation is a gap
between word and act; CONCISE)* -- "can we X?" is a question about whether X
is a good idea, answered in two beats: feasibility, then recommendation
with its reason. Every question to the user is numbered with a permanent
id, one decision per number, each carrying the agent's recommendation and
a short why. Nothing is implemented while a design is under review;
nothing is treated as settled until the user says so. Initiative is
welcome and never silent: a part declined or changed is named, with the
reason, and the decision is left with the user.

---

## 3. Enforcement

For every check: can a machine decide it? If yes, the machine does, and the
memory only says so. A harness that forgets its memory must still be unable
to commit the violation.

| Check | Decided by | How |
|---|---|---|
| deep, one owner, plain call, general vs special, twice, analogue | judgement | memory; the review asks for the named analogue and alternative |
| dependency | judgement + suite | the suite runs the tool outside its environment once |
| errors out, name, comment | judgement | memory |
| boundary | judgement + linter | linter forbids `isinstance` outside parsing modules (project rule) |
| crash-safe | suite | a test interrupts a write and runs again |
| secret | gate | a grep on every command and file written: `-p'`, `--password=`, `token=` literals |
| one kind, scoped | git hook | commit-msg checks the kind word; a path-scoped commit is the only form offered |
| pinned, adversarial | suite + review | the suite's diff shows the test before the fix; the neutered copy is run |
| tested at the right size | deploy/release path + memory | the step that installs, deploys or releases runs the tool's full `--run-tests` first and refuses on a failure; the working loop (filtered runs only) is memory |
| second run | suite | the suite runs every enforcing command twice and asserts an empty second run |
| clearer | judgement | memory |
| usage, verbs, named for what it does, go | suite | help is parsed: usage regex; every destructive verb has a `go` form; `--x` has `--no-x` |
| three layers | suite | `tool` vs `tool -V` differ; `tool -Q` (log off) prints nothing |
| stderr | suite | stdout of a failing run contains no `ERROR` |
| raw beside conclusion, concise, names its reason, adaptive | judgement | memory |
| no stack trace | suite | real SIGINT -> 130 and one line; real unexpected error -> 70, trace in file |
| failure | script | a renumbering script; the suite fails on a duplicate code |
| configuration | suite | the offered paths are a subset of the searched paths; `--create-config` output sources cleanly |
| version | suite | the file run through its deployed path and in its checkout print the same string |
| self-test | harness | `--run-tests` exists and prints `1..N` first |
| state and logs | suite | the suite runs the tool with both roots pointed at temporary directories and asserts no write elsewhere, and no state file under the log root |
| notifies | suite | `--test-mail` with a stub transport |
| unrepresentable, shaped, parsed once | type checker + judgement | pyright strict (`"strict": ["**"]`); the rest memory |
| Python mechanics | linter | ruff: `BLE001` blind except, `FBT001`/`FBT002` positional boolean, `B006` mutable default, `ANN401` `Any`, plus the project's selected rule set |
| shell mechanics | linter + gate | `shellcheck -s <shebang dialect>`, `<shell> -n`; a gate refuses GNU-only flags in a script that targets BSD userland (`head -N`, `sed -r`, `grep -P`, `xargs -r`, `date -d`, `find -printf`, `stat -c`) |
| WHEN running commands | gate | a gate refuses a known long command piped straight into `tail`/`head`/`grep` without a capture |
| WHEN committing | gate + setting | a gate refuses `sudo`, `--force`, `+refspec`; the harness setting that adds an AI trailer is off |
| everything else in 2.6 | judgement | memory |

Gates **block** only what is never right: a GNU-only flag in a BSD-targeted
script, a secret literal on a command line, `sudo`, a forced push, a
mutable default. Everything else is **advisory**: fed back as a finding,
never refused -- a blocking lint on style makes the agent fight the gate
instead of writing code.

---

## 4. Adapters

An adapter is the rendering of layers 2 and 3 for one harness, in three
parts: **memory** (the judgement checks in that harness's instruction
format, keyed by the moment they fire), **gates** (the mechanical checks,
run by the harness where it can run things, else by the repository's
pre-commit and the project's own suite), and **proof** (one scenario per
check: a task that triggers it, and the observable that shows it fired,
with the harness, its version and the date of the last run).

Adapters are **rendered from this document by one script and never
written by hand** -- the second face of CONSISTENCY: a hand edit would be a
second copy of a check, and would drift. See `adapters/` for the rendered
ones and `tools/render-adapters` for the script. An agent in a harness that
has no adapter yet renders one from layers 2 and 3, following the shape of
the existing ones.

Three questions decide whether an adapter works, in order, none of them
"the file exists": **loaded?** (the harness shows what instructions it
used), **applied?** (the proof scenarios, run in that harness), **enforced
when not applied?** (every mechanical check has a gate outside the model).

---

## Site parameters

The checks above name five things that differ from one site to the next,
in angle brackets. The spec never states their values: an adopter writes
them once, in a local file beside this one, and every adapter reads them
from there. The list below is the contract -- each entry says which check
consumes it, and a parameter no check consumes does not belong here.

| Parameter | Meaning | Consumed by |
|---|---|---|
| `<name>` | the tool's own name; also the name of its configuration file and of its state directory | configuration, state and logs |
| `<site config dir>` | the directory a site keeps its tools' configuration files in, searched before the user's home | configuration |
| `<per-user state dir>` | the root under which a tool's persistent state lives, per user | state and logs |
| `<per-user log dir>` | the root under which a tool's logs live, per user, and nothing else | state and logs |
| `<shebang dialect>` | the shell every script is written for and linted as | shell mechanics (layer 3) |
