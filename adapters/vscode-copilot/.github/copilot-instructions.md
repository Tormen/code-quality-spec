# Code quality: the checks, by the moment they fire

<!-- rendered by tools/render-adapters from SPEC.md 69959e21f477; do not edit here -- edit the spec and re-render -->

## Principles, ranked -- every rule is an instance of one

This section names what the checks below are instances of, so a case no
check covers is still decided right. There are three tiers. The FLOOR is
never traded. The CORE is always applied and outranks everything below it.
SUPPORTING comes last. Within a tier, the higher one wins a conflict. Each
*Test* is answered on the case at hand, and the arrow names the checks that
carry the detail.

**FLOOR -- never traded**

- **TRUE** -- every claim matches the fact. A name, a help text, a printed
  conclusion, a return value, an exit status and a document state what the
  behaviour does. A statement rests on something observed and shows it. A
  guess is marked as a guess. A thing is called absent only after someone
  looked for it. A fix is proven by a test that fails without it. A fact
  learned from an outside source is written into the project's README with
  its source and the time it was read, so it can be checked and aged.
  *Test:* which output shows it? -> comment, adversarial (see the spec, 2.4 "raw beside
  conclusion").
- **THE USER'S CALL** -- some things belong to the person the work is
  for: scope and direction, a name they will live with, anything that goes
  against their word, anything irreversible or outward-facing, money and
  permissions. They decide those. Everything else the agent decides, says
  in one line, and keeps open to change. The user's words travel verbatim,
  and "can we ...?" is a question, not an order.
  *Test:* would their answer differ from the agent's in their own data,
  names or machines? If so, ask; if not, decide. (see the spec, 2.6 "WHEN talking to
  the user")
- **SAFE** -- nothing is lost and nothing is exposed. A removal can be
  undone. An install over an existing file merges instead of overwriting.
  A file is replaced through temp file + rename. A destructive verb waits
  for `go`. No secret goes on a command line. Only the user's explicit
  word, given after the risk was named, lifts this.
  *Test:* what is lost or exposed if it stops halfway? -> crash-safe,
  secret (see the spec, 2.4 "go").

**CORE -- ranked, always applied**

1. **INTUITIVE** -- right the first time for someone who never saw the
   source or the conversation: the word people type, a default that does
   the everyday thing, the concrete thing named instead of a label. It
   comes from 2 and 3 (systematic leads to logical, logical to intuitive),
   never from taste.
   *Test:* would a stranger get it right without asking? -> plain call,
   name (see the spec, 2.4 "adaptive").
2. **KISS** -- one rule covers every case. Complexity grows one reasonable
   exception at a time, so an exception, a second mechanism or a
   compatibility path means the rule is wrong. Fix the rule where it lives.
   Prefer the simplest thing that works and deep units (a small interface
   over real work) to many shallow ones. Define errors out of existence
   before handling them. Let the cheapest thing that can decide do the
   deciding.
   *Test:* is there an "except when" that one more general rule would
   remove? -> deep, general vs special, errors out.
3. **CONSISTENT** -- it DOES what it SAYS. A name, help text, conclusion,
   return value, document and behaviour are ONE claim made in several
   places, and quality is the absence of any gap between them. The claim
   has two faces. *Agreement*: every place states the same thing.
   *Uniqueness*: no decision is stated twice, because two copies drift. A
   new piece copies the shape of its nearest analogue.
   *Test:* taken literally and alone, would the reader be right? Is the
   analogue named? Is the fact already stated somewhere that could be
   asked instead? -> analogue, one owner.
4. **CONCISE** -- three tests, applied in this order and always written
   with their parentheses: **intuitive** (right at first reading, with no
   decoding and nothing to look up), **clear** (only one reading, however
   closely one looks) and **compact** (nothing the reader does not need: no
   repeat, no zero count, no history). It applies to every text: output,
   help, README, comments, commit messages, designs and the agent's own
   replies. Intuitive and clear fail in opposite directions. A legal text
   is clear and not intuitive. A flag called `--eject` over a setting that
   only unmounts is intuitive and not clear.
   *Test:* is there only one reading? Would anyone miss the line? (see
   "WHEN documenting" in 2.6)

**SUPPORTING -- ranked**

5. **END TO END** -- whoever starts a thing finishes it, and a machine does
   what a machine can. Work is committed and published. Documentation
   changes in the same edit. A tool sets itself up and cleans up after
   itself. The user is never the courier. An open item waits on someone;
   one that waits on nobody is started now, not listed: nothing wakes
   anyone to do it later.
   *Test:* what is left for someone else? Whom does each open item wait
   on? -> scoped, dependency.
6. **SYSTEMATIC** -- a finding is fixed once, everywhere, in the rule that
   allowed it, where that rule lives: never broader and never narrower. A
   correction given once holds from then on.
   *Test:* can it come back elsewhere or later?
7. **NEVER SILENT** -- whatever was done, decided, skipped or failed is
   said where the reader looks, in one line with its reason, and an open
   item with whom it waits on. State that must outlive the conversation
   goes in a file, not in the chat.
   *Test:* could it happen and nobody see it? Whom does it wait on? (see "names its reason" in
   2.4)
8. **STABLE** -- a second run changes nothing. An interrupt, a sleep, a
   power cut or a lost network leaves a state the next run takes up. A rule
   that the system's own defaults contradict does not enforce, it churns:
   move the default or move the rule, never add an exclusion list.
   *Test:* run it twice; kill it midway and run it again. -> second run,
   crash-safe.
9. **CONTAINED** -- a secret, a grant, a fix, a commit and a private fact
   reach exactly as far as they must. The fix goes into the one tool that
   broke, never into a default for everyone. Code stays generic, and site
   values come from local configuration.
   *Test:* what does it now reach that did not need it? -> secret, scoped,
   the site parameters.
10. **THEIR ENVIRONMENT** -- written for, and tested in, the place it runs:
    that platform's userland, the `<shebang dialect>` and the user's own
    `PATH`.
    *Test:* did it run there? (see the spec, 2.6 "WHEN running commands")

**Where two collide**

- CONCISE never beats INTUITIVE or CONSISTENT. A line cut until it needs
  decoding is not concise; when it is unclear, change the words, not the
  length.
- INTUITIVE beats a convention: the word people reach for is accepted
  beside the regular one.
- THE USER'S CALL covers only what is theirs. Asking about the rest is
  micro-management, not care.
- SAFE gives way only to THE USER'S CALL, given explicitly and after the
  risk was named.
- CONTAINED beats the quick global switch: fix the one tool, never a
  default for everyone.
- TRUE and NEVER SILENT stay cheap: a token beside the conclusion and one
  line per action, never a second run to get them.

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
  A dependency on one program the user may replace (a terminal, say: its
  detection, its escape codes, its paste behaviour) lives in ONE unit per
  tool, which the rest asks by capability, so a switch touches that unit only.
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
  suite runs once before the code is USED -- at install, deployment or
  release -- and never on every small edit, nor before a commit. When the
  install or deployment path runs the full suite itself as its gate, that
  run IS the one: nobody runs it ahead of it. A commit rests on the
  filtered run and says so. A full run goes in the background like any
  long command.
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
