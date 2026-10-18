# Sources: what each book argues, what we took, what we left

One page per book, in our own words -- no sentence of any book is
reproduced here, and no list of theirs is copied; where an author's own
phrase *is* the idea it appears once, attributed. Each page says what the
book argues, which of its ideas became a check in `SPEC.md` (named by the
check's keyword, pointing one way: this file points at the spec, never the
reverse), what we read and chose **not** to adopt and why, and what to read
in full when a check feels arbitrary.

Five of the seven were read cover to cover for this document (page-by-page
notes, in our words, kept privately); the remaining two were written from
long acquaintance with the books and are marked so.

The checks these pages point at are the ones in `SPEC.md` sections 2.1 to
2.6. A pointer written as *candidate* names an idea proposed for the spec
and not yet decided.

---

## Ousterhout -- A Philosophy of Software Design (2nd ed., 2021)

Read in full.

**Thesis.** Software has one enemy, complexity: anything in a system's
structure that makes it hard to understand or change. It comes from
dependencies and obscurity, it is judged by readers and not by the writer,
and it arrives in small increments that each look harmless -- so the only
workable stance is zero tolerance and a steady investment in design over
"working code". The method is red flags: learn to see the symptom, then
try alternatives until it disappears.

**What shaped the spec.**
- The deep module -- much function behind a small interface -- and its
  failures: the shallow wrapper, the pass-through method, the pair of
  methods that can only be read together → *deep*.
- Information hiding, and leakage through shared assumptions rather than
  through interfaces; decomposition by what must be known, not by the order
  things happen (read/parse/write is one decision spread over three) →
  *one owner*.
- The common case should need nothing; rare features must not leak into
  the common path; good defaults are partial information hiding → *plain
  call*.
- A general mechanism carrying one client's special case; special cases
  designed away by choosing a better normal case (a selection that always
  exists and may be empty) → *general vs special*, and the KISS axis.
- Define errors out of existence first; then mask low, aggregate high, or
  crash; every exception is interface the caller must handle → *errors
  out*.
- Sketch two radically different designs before choosing, at every level
  → *twice*.
- Comments carry the informal half of an interface, which code cannot;
  they say what and why, never how; a comment that repeats the identifier
  is noise; a comment that must be long to be complete indicts the
  abstraction; obviousness is decided by the reader → *comment*, *name*.
- Names that paint a picture in isolation; the one-name-many-meanings bug
  that took months to find; hard to name means not one thing → *name*.
- Consistency within a codebase is earned by following what is already
  there and enforcing it in the commit path; a better idea is not a reason
  to break a convention unless the whole old usage is converted →
  *analogue* (and the second face of CONSISTENCY).
- After a change the code should look as if it had been designed for it;
  design knowledge lives next to the code, once, not in commit messages →
  *clearer*, *one kind*.
- Measure before and after any performance change; simplicity is usually
  the faster design → *WHEN running commands*, and the enforcement rule
  that optimisation needs a measurement.
- Configuration parameters are often an unsolved problem exported to the
  user; ask whether the code could compute a better value → *candidate*.
- Write the interface comment before the body and use its length as a
  depth gauge → *candidate*.

**Read and not adopted.**
- The case against test-driven development as "tactical programming in
  pure form". We keep test-first, but only where he too endorses it: for a
  fix, where the test must be shown to trigger the bug (*adversarial*).
  For new design we take his point and do not require tests to lead.
- "Increments of development should be abstractions, not features" -- a
  planning stance, not checkable on a diff; it informs *twice* and nothing
  else.
- The context object as the answer to pass-through variables; he admits it
  has most of a global's drawbacks, and we prefer configuration read once
  at the boundary.
- His defence of long methods as such. We agree length is no reason to
  split, but *deep* is the check, not line count either way.

**Read in full when** a reviewer wants a smaller function "because it is
long", or an interface grows a flag for one caller, or an error is being
thrown that could be defined away.

---

## Hunt & Thomas -- The Pragmatic Programmer (20th anniversary ed., 2019)

From acquaintance, not re-read for this document.

**Thesis.** Craft is a set of habits held by a responsible individual:
own your tools, own your mistakes, keep knowledge in one place, and treat
every piece of software as something that will change. The book is a
catalogue of such habits, each short, each with a reason.

**What shaped the spec.**
- One representation of every piece of knowledge, so a change is made in
  one place -- their DRY, understood as knowledge, not text → *one owner*,
  and the second face of CONSISTENCY (a second copy is a second claim).
- Orthogonality: components that change for different reasons must not
  know about each other → *general vs special*, *deep*.
- Crash early; a program that dies before doing damage tells no lies; do
  not trust input you did not produce → *boundary*.
- Tracer bullets and small, reversible steps; commit and integrate
  continuously → *scoped*, *WHEN committing*.
- The broken-window rule: one tolerated piece of rot invites the next →
  *clearer*, and the KISS axis's zero tolerance.
- Automate what is repeated; a checklist a tool can run is a test → the
  whole of section 3, where machine-decidable checks stop being memory.

**Read and not adopted.**
- Design by contract as a language-level mechanism; we take its spirit
  (preconditions at the boundary, asserted invariants inside) without
  requiring the machinery.
- Much of the career and estimation advice, which is outside a code-quality
  spec.

**Read in full when** a team argues about "duplication" that is really two
different pieces of knowledge, or when a process is being invented that a
script should replace.

---

## Fowler -- Refactoring (2nd ed., 2018)

From acquaintance, not re-read for this document.

**Thesis.** A refactoring is a behaviour-preserving change made in small
steps with the tests green between them; design improves continuously
rather than up front, and a catalogue of named smells with named moves
makes that improvement teachable and reviewable.

**What shaped the spec.**
- Refactoring and behaviour change are two different activities and are
  never mixed in one step ("two hats") → *one kind*.
- Tests are what make a refactoring safe; a change without them is not a
  refactoring but a gamble → *pinned*.
- The smell catalogue as vocabulary: duplicated code, long parameter list,
  feature envy, shotgun surgery, speculative generality, data clumps,
  primitive obsession → *one owner*, *plain call*, *shaped*, *twice*.
- The opening question of every smell is "what would make this change
  easy" -- make the change easy, then make the easy change → *clearer*.

**Read and not adopted.**
- The move catalogue itself. It belongs in a tool (an IDE's refactorings)
  and in a reader's head, not in a spec of checks; the spec names the
  smells, not the mechanics.
- The focus on object-oriented restructuring; our tools are mostly small
  programs where the unit is a function or a module.

**Read in full when** a diff mixes a rename with a behaviour change, or a
reviewer cannot name why a piece of code feels wrong -- the catalogue
usually has the name.

---

## McConnell -- Code Complete (2nd ed., 2004)

From acquaintance, not re-read for this document.

**Thesis.** Construction -- the writing of routines, variables, control
flow and the code that surrounds them -- is where most of a program's
quality is decided, and most of its advice can be backed by data rather
than taste. The book is the most complete reference for that level.

**What shaped the spec.**
- A routine does one thing, named for what it does, with a small, ordered
  parameter list; a flag that selects between unrelated behaviours is two
  routines → *name*, *plain call*, *general vs special*.
- Defensive programming belongs at the edges; inside, assertions document
  and enforce assumptions, and a failed assertion is a bug, not a condition
  to handle → *boundary*.
- Comments at the level of intent, not of the statement; a comment that
  tracks every line is maintained by no one → *comment*.
- Variables with the smallest scope and one meaning each; no reuse of a
  name for a second purpose → *name*.
- Measure before tuning; the hot spot is almost never where intuition says
  → *WHEN running commands*.

**Read and not adopted.**
- Pseudocode-first construction as a required step; *twice* asks for two
  shapes of an interface, not for a pseudocode draft of every body.
- Its language-era specifics (goto discussions, class layout conventions of
  2004); the principles survived, the examples did not.

**Read in full when** an argument about naming, routine size or defensive
checks is going in circles -- it usually has the data.

---

## Feathers -- Working Effectively with Legacy Code (2004)

From acquaintance, not re-read for this document.

**Thesis.** Legacy code is code without tests. Most real work is changing
such code, and the way to do it safely is to find a seam -- a place where
behaviour can be altered without editing the code -- get a test in through
it that records what the code does now, and only then change anything.

**What shaped the spec.**
- The characterisation test: pin current behaviour, right or wrong, before
  touching it → *pinned*.
- Seams: a parameter, a function boundary, a configuration key where a
  test can get in without editing the logic → *pinned*'s test, and the
  enforcement rule that a change to untested code shows the test before the
  fix.
- Sprout and wrap: add new behaviour in a new, tested unit beside the old
  rather than inside it → *one kind*, *clearer*.
- The dependency-breaking moves exist to make a test possible, never for
  their own sake → the warning in *twice* against speculative shape.

**Read and not adopted.**
- The C++ and Java mechanics (link seams, preprocessor seams); the idea
  transfers, the techniques mostly do not, to small scripts and tools.
- The implicit assumption that the unit under test is a class; for us it is
  usually a command and its output.

**Read in full when** a change is about to be made to code nobody has
tested, and the first instinct is to "just be careful".

---

## Viafore -- Robust Python (2021)

Read in full.

**Thesis.** Code is asynchronous communication with a maintainer you will
never meet; robustness is that person being able to change the code
confidently. In Python the main carrier of intent is the type: annotations
plus a strict checker turn documentation into verification, and the type
system can make illegal states unrepresentable. Everything in the book is
offered as a tool to be weighed, not a rule.

**What shaped the spec.**
- Choose the type by the relationship it models: a fixed set of values is
  an enumeration or a literal type; independent fields are a data class;
  a class exists when there is an invariant to guard in the constructor;
  dictionaries are for data you do not own → *unrepresentable*, *shaped*.
- Optional only where None is a real answer; a function typed to return a
  value never returns None; distinct kinds of value that must not mix get
  distinct types → *unrepresentable*, and the Python failure paragraph.
- Parse at the boundary (a validating model), then trust the type inside;
  a typed dictionary cannot carry a constraint → *parsed once*,
  *boundary*.
- A strict, fast, visible type checker; an ignore comment is for old code
  only and is counted so it shrinks → section 3 (type checker row).
- Inheritance is a behavioural contract (invariants kept, preconditions not
  strengthened, postconditions not weakened); structural needs are met by
  a protocol, and composition comes first → *candidate*.
- Test value against cost; one logical assertion per test, with its
  message; do not mock what you own; mutation testing, not coverage, tells
  whether a suite catches anything → *adversarial* (the manual form of
  mutation testing), and *candidate* for the rest.
- Deduplicate only what changes for the same reason → *one owner*, read
  correctly.

**Read and not adopted.**
- Property-based and acceptance-test frameworks as part of the baseline;
  valuable, but a project adopts them by decision, not by a spec.
- The event-driven, plug-in and composability chapters: architecture for
  larger systems than the tools this spec is written for.
- Do not annotate everything; the author exempts throwaway scripts. Our
  strict-mode rule is deliberately broader, because "throwaway" scripts
  are the ones that live longest.

**Read in full when** a Python design is reaching for a dictionary where a
type would do, or for inheritance where a protocol would do.

---

## Slatkin -- Effective Python (3rd ed., 2025)

Read in full (125 items).

**Thesis.** Python checks almost nothing before running, so correctness has
to come from idiom, tooling and tests. Readability is the deciding
criterion in every item, and the recurring move is "start with the
simplest mechanism and migrate only when it hurts". The enemy named most
often is the silent wrong answer.

**What shaped the spec.**
- Raise, never return None or a success flag for failure; a module raises
  subclasses of its own root exception; chain with the cause and let
  control-flow exceptions pass through; a broad handler logs type and
  value → the Python failure paragraph, *errors out*.
- Keyword-only flags, no positional booleans, no mutable or dynamic
  defaults; more than three return values are an object → the linter row
  of section 3, *shaped*.
- Prefer integration tests that exercise real collaborators over
  mock-heavy unit tests → *candidate*.
- Measure with a profiler and a microbenchmark before optimising; pick the
  data structure before the algorithm → *WHEN running commands*.
- A long chain of `isinstance` tests is a missing dispatch; the counter-
  case, independent behaviours over the same data, is a single-dispatch
  function → *general vs special*.
- Assertions state internal assumptions and stay enabled; raised
  exceptions are the interface → *boundary*.

**Read and not adopted.**
- Most of the 125 items. They are idioms and traps a linter and a type
  checker now own (the section 3 row lists the codes); turning them into
  memory would bury the few that need judgement.
- The concurrency and performance chapters as checks: they are decisions
  made once per project, with measurements, not per diff.
- The author's own exemption of small programs and prototypes from type
  annotations, for the same reason as above.

**Read in full when** a Python diff "works" and still reads wrong; the
item that names the trap is usually there, with its reason.

---

## Two books in the folder that contributed a thesis and no check

- **Contieri -- Clean Code Cookbook (2023).** Read in full. One axiom: the
  model is a partial simulator of reality, and every real thing is exactly
  one object and every object one real thing; from it the author derives
  that objects are behaviour and never data, that nearly every conditional,
  flag, null and type check is an accidental decision to be made
  polymorphic, and that invalid objects must never exist. We took the
  essential-versus-accidental test for a conditional ("would a domain
  expert state this as an if?") into *general vs special* as *candidate*,
  and the fail-fast stance into *boundary*. Not adopted: the wholesale
  programme (no getters, no nulls, no optional parameters, no static
  methods, every class final or abstract, no ids in domain objects); it is
  a coherent object-oriented doctrine for business systems, and most of its
  recipes restate the refactoring catalogue for that setting. Our tools are
  small programs where a function and a file are the units.
- **Sweigart -- Beyond the Basic Stuff with Python (2021).** Read in full.
  The gap between tutorial Python and professional practice is mostly
  readability plus a small toolchain (formatter, linter, type checker,
  version control), and readability is a judgement, not a rule score -- a
  smell is a prompt to look again. We took one thing: his rejection of
  five popular rules (single return, one try per function, no flag
  arguments, no globals, no comments) as dogma, which is why the spec's
  checks each carry a reason and a test instead of a prohibition. Not
  adopted: the material itself, which an experienced developer already
  has.
