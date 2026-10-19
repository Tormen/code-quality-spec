# Code quality: the checks, by the moment they fire

<!-- rendered by tools/render-adapters from SPEC.md 4f15993456b9; do not edit here -- edit the spec and re-render -->

## Principles

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

## BEFORE writing a unit (a function, class, module, verb or flag)

- **analogue** -- the nearest existing thing in the tool (same read/write
  character, same scope, same destructiveness) is found, its shape copied,
  and named. When the analogue contradicts what taste proposed, the
  analogue wins, and the reply says so. Consistency is derived from the
  tool, never from preference. A convention is changed only with new
  information and by converting every old use in the same change -- never
  left beside the old.
  *Test:* the analogue is named.
- **deep** -- the body does real work behind a short signature. A unit that
  only forwards its arguments to a near-identical signature, or two units
  that can only be read together, is ONE unit: merge. A getter/setter pair
  that exposes a field, or a method that hands out an internal collection,
  is a shallow unit: expose the behaviour instead. Write the unit's
  interface comment before its body; a comment that cannot be short says
  the abstraction is wrong.
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
  `if` inside a general helper is the KISS exception-smell in code. An `if`
  stays in a shared unit only when a domain expert would state the rule as
  an if; a branch on a type, a flag, a null or an environment name is
  accidental and becomes its own unit or a dispatch.
  *Test:* a second, different caller could reuse the helper unchanged.
- **twice** -- for anything that outlives the change (a configuration key,
  a command-line verb, a function others call) a second, genuinely
  different shape is sketched, and one line says why the chosen one wins.
  *Test:* the alternative is named in the design or the reply.
- **dependency** -- standard library first; a third-party dependency is
  added only when it earns its place, and the tool then sets up its own
  environment on first use rather than asking anyone to install anything.
  *Test:* the dependency's one-line "why" is written where it is declared.

## WHILE writing the lines

- **errors out** -- the operation is first defined so the edge case is
  simply covered (`mkdir -p`; removing what is already gone is done). A
  guard that every caller would repeat moves INTO the unit. What still
  reaches the caller is something the caller can act on, reported through
  the tool's one error call with its code (see the spec, 2.4 "failure"). What
  cannot be defined away is handled as low as the handling is useful and
  aggregated as high as possible -- one handler for a class of failures,
  not one per call; what nobody can act on crashes.
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
  command. Design rationale lives next to the code it explains, once; other
  places point at it; a commit message may carry a copy but is never its
  only home.
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

## BEFORE committing

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


## Scope

Path-scoped instructions in `.github/instructions/` add the tool-level and Python checks; `AGENTS.md` holds how the agent itself works. Checks a tool can decide are enforced by the repository's pre-commit configuration, not by this file.
