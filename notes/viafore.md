# Viafore, Robust Python (O'Reilly 2021) -- working notes

Page numbers in brackets are the book's printed pages (PDF page = printed + 20).
Markers: **KEY** = the author treats it as central; **CONTRARIAN** = unusual against
common Python practice; **AGAINST** = something the author argues against.

## NOT READ

- PDF 1-20 (front matter, table of contents, preface): not read.
- PDF 369-381 (index): not read; no content lost.

Every content page (PDF 21-368 = printed 1-348, including the Part intros) was read.

## Part I intro -- Annotating Your Code with Types [PDF 41]

- Types are glossed over in beginner material and never revisited; Part I is about when to use a type appropriately, not just that types exist [PDF 41].

---

## Ch 1 -- Introduction to Robust Python [1-21]

- Robustness is defined as a codebase staying resilient and error-free while it is constantly changed; the enemy is not today's bug but tomorrow's maintainer misunderstanding yesterday's intent [2-4]. **KEY**
- The whole book rests on "asynchronous communication": the author of code and its future reader never meet, so intent has to be encoded in the code itself, not in someone's head [5, 8].
- Worked example: a recipe-scaling function rewritten "cleaner" introduces three subtle bugs (no longer clears the input, dedupes ingredients via dict, name collision with a "servings" key) because the original intent was never written down; a third version with a `Recipe` type, `Fraction`, and named operations makes the intent explicit [6-8]. **KEY**
- Clean code and tests are table stakes but do not themselves make code robust; the author explicitly defers clean-code practice to other books [3].
- Choice of collection and of loop construct is itself a message: list vs tuple vs set vs dict, and `for` vs `while` vs comprehension each tell the reader what to expect [9-19].
- The "Law of Least Surprise" is the test: a reader who is surprised by behaviour has been failed by the author [19].

## Ch 2 -- Introduction to Python Types [23-33]

- A type has a mechanical representation (bits, behaviours the interpreter knows) and a semantic one (what it means to the reader); the book cares about the semantic half [24-27].
- `datetime` vs `int` is the illustrative pair: same underlying number, different legal operations and constraints; choosing the more specific type tells the reader which operations are allowed [26-27].
- Untyped parameter example (`close_kitchen_if_past_cutoff_time(point_in_time)`): a reader has to dig through callers or guess, and "death by a thousand cuts" of such guesses is what erodes maintainability [27].
- Python is strongly but dynamically typed; strong typing helps (loud `TypeError`s), dynamic typing is the thing to overcome [29-31].
- Duck typing is explained as "works with anything that supports the needed interface", a boon and a risk at once [31-32].
- Author is careful to say weakly or dynamically typed languages can be robust; they just need more discipline and tooling [29-30].

## Ch 3 -- Type Annotations [35-44]

- Annotations are hints, ignored at runtime; their value is communication first, tooling second [36, 39]. **KEY**
- Return-type example: a function with three return paths forces the reader to inspect a database layer, helper calls and a global to learn it returns `list[str]`; one `-> list[str]` removes all that cognitive load [37-38].
- Do NOT annotate everything: obvious locals (`number: int = 0`) add nothing; annotate functions, complicated/unintuitive types, and whatever mypy asks for (empty collections) [39, 43-44]. **CONTRARIAN** against "annotate all the things".
- Typecheckers turn hints into a safety net: three "spot the bug" examples (bytes vs str via `encode`, `update` on a list, returning `None` where a `str` is declared) are all caught statically [41-43].
- Typecheckers do not replace tests; they catch exactly one class of error [43]. **AGAINST** treating a green mypy run as proof.
- Author does not recommend annotations for short scripts or throwaway code; they pay off only for code that lives [44]. **CONTRARIAN**

## Ch 4 -- Constraining Types [45-60]

- Goal: make illegal states unrepresentable; six tools: `Optional`, `Union`, `Literal`, `Annotated`, `NewType`, `Final` [45]. **KEY**
- `None` is Python's billion-dollar mistake: a hot-dog-stand pipeline where any step may return `None` becomes a thicket of `is None` checks, and the alternative (exceptions) still relies on humans remembering to catch [46-49]. **AGAINST** returning `None` from a function typed to return a value; **AGAINST** exceptions for normal control flow [48-49].
- `Optional` buys three things: it flags a possible `None` to the reader, it distinguishes "empty result" from "error", and the typechecker refuses to let a `None` flow into a non-optional use [49-51]. Needs `--strict-optional` in older mypy [51].
- `Union` constrains representable state space: a four-field dataclass has 144 combinations, many illegal; splitting it into `Union[Snack, Error]` (a sum type) drops it to 22 [53-55]. **KEY** Product vs sum types.
- `Literal` restricts a field to a fixed set of values and the typechecker rejects anything else; lighter than an Enum [55-56].
- `Annotated` is presented honestly as communication only: no tool checks the metadata [56-57].
- `NewType` creates a distinct type with one-way conversion through a "blessed" function (`HotDog` -> `ReadyToServeHotDog` only via `prepare_for_serving`); Python has no way to enforce that the blessed function is the only constructor other than a comment [57-59]. Uses: sanitized strings, logged-in user, validated IDs [58-59]. Type aliases are NOT this: they are interchangeable names [59].
- `Final` prevents rebinding (not mutation) and is most useful at module scope [59-60].

## Ch 5 -- Collection Types [61-77]

- Annotate what is *inside* collections (`list[Cookbook]`, `dict[str, int]`), and consider an alias that names the domain meaning [62].
- Collections should nearly always be homogeneous; a heterogeneous list (first element is an int, rest are tuples) forces every user to remember a special case the typechecker cannot see [63-64]. **KEY**
- If heterogeneity is unavoidable, express it as a `Union` so the checker forces handling; too many `Union` members is a smell, and `Any` at the far end "defeats the purpose" [64-65]. **AGAINST** `Any` for collections.
- Dicts with mixed value types (`dict[str, Union[str, int]]`) are a dead end: the user must check every access, nobody knows the keys, and people drift to `Any` [65-66]. **AGAINST** dicts as records.
- `TypedDict` is for data you do not control (JSON/YAML/API responses); if you own the dict, use a dataclass or class instead [67-68]. **KEY** Runtime it is still just a dict; no validation [68].
- Generics (`TypeVar`) keep a collection's type consistent over its lifetime; a `Graph[Node, Edge]` example and a `APIResponse[T] = Union[T, APIError]` alias [69-71].
- Do not subclass `dict`/`list`/`str` to override behaviour: built-ins inline internal calls, so an overridden `__getitem__` is not used by `.get()`; use `collections.UserDict` etc., or `collections.abc` for a from-scratch collection [71-76]. **AGAINST** subclassing built-ins.
- Use `collections.abc.Iterable` and friends as annotations to express the minimal interface needed [75-76].

## Ch 6 -- Customizing Your Typechecker [79-93]

- A typechecker is "verified documentation" (Lehtosalo); configure it rather than accept defaults [79].
- Strictness is a dial: stricter catches more but raises the cost of change; pick the bar per codebase, often per module via config sections [80-81].
- Flags the author recommends: `--disallow-any-expr` / `--disallow-any-generics` to flush out `Any` (but allow `Any` for genuinely untyped caches) [81-82]; `--disallow-untyped-defs` (or the softer `-incomplete-defs` / `-untyped-calls`) [82]; `--strict-optional` always [82]; `--no-implicit-optional` so `x: int = None` must be written as `Optional[int]` [83]. **CONTRARIAN** on implicit Optional (now mypy's default, but not at time of writing).
- Reporting: `--html-report`, `--linecount-report`, `--any-exprs-report` to see how much code is actually checked; `--junit-xml` for CI [83-84].
- Speed matters because slow checkers stop being run: incremental cache, remote cache, `dmypy` daemon (23 s -> under 0.5 s) [84-85].
- Pyre offers codebase queries and Pysa taint analysis (source `input()` -> sink `os.system`) [85-90]; Pyright/Pylance for whole-workspace real-time diagnostics [91-93].

## Ch 7 -- Adopting Typechecking Practically [95-107]

- Legacy code is redefined as code whose authors you can no longer talk to; annotations are the substitute conversation [95].
- Costs of adoption are real (buy-in, learning, tooling, writing, fighting the checker); value = benefits - costs, and both follow curves, so the job is to reach break-even early [96-97]. **KEY**
- Find pain points first: bugs around `None`, wrong attribute access, type conversions (int/str, bytes/str, list/tuple) are the classes annotations eliminate [97-98].
- Target strategically: new code and code you touch; bottom-up (core utilities); the moneymakers (business logic); the churners (most commits); the complex [98-99].
- Lean on tooling: mask existing errors per module rather than leave thousands of errors on (nobody fixes them, new ones drown); `# type: ignore` is for old code only, never new; track that ignores shrink; turn on `warn_unused_ignores` [100-101]. **KEY**
- MonkeyType records runtime types and writes stubs; a `Union` appearing in a generated stub is a code smell worth investigating [101-105]. Pytype infers types statically and is lenient about types changing mid-lifetime; do not use it as an excuse not to annotate [105-106].

## Part II intro -- Defining Your Own Types [109]

- Three user-defined types, each for a different relationship: Enum = restricted set of values; dataclass = relationship between independent concepts; class = relationship with an invariant to preserve [109]. **KEY**

## Ch 8 -- User-Defined Types: Enums [111-122]

- A domain type (`Restaurant`) beats a tuple of primitives in a signature; types build a shared domain vocabulary (Evans) [111-112].
- Tuples of constants plus string parameters invite wrong values and typos (missing accent in a string, "Alabama White BBQ Sauce" accepted silently); an `Enum` rejects unknown values at construction and makes the signature say what is allowed [113-115]. **KEY**
- Do not use Enums for runtime-determined options; use a dict [115, 121]. **AGAINST**
- `auto()` says "the value does not matter"; `_generate_next_value_` belongs in base enums only [116-117].
- Enum vs Literal sidebar: nearly equivalent for the typechecker; Literal for a quick restriction, Enum for iteration, runtime checking, name-to-value mapping [117].
- `Flag` for bitwise-combinable sets of values (allergens) [117-118].
- `IntEnum`/`IntFlag`: avoid unless needed for interoperability; implicit int conversion lets two unrelated enums compare equal and the bug surfaces only when one of them is renumbered [119-120]. **AGAINST**
- Aliases are allowed by default; `@unique` only when uniqueness is actually relied on [120-121]. **CONTRARIAN** default-to-nonunique.

## Ch 9 -- User-Defined Types: Data Classes [123-134]

- Dataclasses group heterogeneous, related, independent fields into a composite type with explicit field types; dicts and tuples hide what is inside [123-126]. **KEY**
- They may carry methods; the soup `Recipe` with `make_vegetarian()` is the example [127].
- Free features: repr, `eq=True`, `order=True` (field order defines comparison; or hand-write `__lt__` etc., but then not `order=True`) [128-130].
- `frozen=True` prevents field rebinding, makes the object hashable, and removes whole error classes (callers assuming stability, half-updated state, data races) -- but it does not freeze the contents of mutable members, so prefer immutable member types [130-132].
- Versus dict: dict for homogeneous mappings, dataclass for heterogeneous records [132]. Versus `TypedDict`: dataclass is the default; `TypedDict` only when you already hold a dict (JSON) and need none of the dataclass features [133]. Versus `namedtuple`: almost always dataclass; `namedtuple` only for Python <= 3.6 [133]. **KEY**
- Closing rule: a dataclass is right only when fields are independent; the moment one field constrains another you have an invariant and need a class [134]. **KEY**

## Ch 10 -- User-Defined Types: Classes [135-152]

- Classes are overused by people who learned them early and underused by people who swung the other way; the deciding question is whether there is an invariant [135].
- An invariant is a property true for the entity's whole lifetime; the constructor is where it is checked, so a user can rely on it afterwards [137-139]. **KEY** Pizza example: radius in 6..12, at most one sauce, sauce ordered first [138].
- Assertions vs exceptions sidebar: assert for "a developer messed up" (may be stripped by `-O`), exceptions for conditions callers must handle; constructors return nothing so `Optional`/`Union` do not apply there [139].
- Never construct a broken object: throw, or massage the data into conformance; a factory function returning `Optional[_Hidden]` is the exception-free alternative, but if you move invariant checks out of the class you have a dataclass again [140].
- Why invariants pay: DRY (checks in one place), writer works so the reader doesn't, easier reasoning, Law of Least Surprise; a dictionary cannot do any of this [141-142]. **KEY**
- One class per set of related invariants (Single Responsibility); unrelated attributes or methods mean low cohesion [142].
- Communicate invariants in the docstring at the class, including those not visible in code and their business reasons; a wiki is too far away [143-144].
- Protect against maintainers with unit tests, and with a context manager that re-checks every invariant as a postcondition (deliberate double-entry bookkeeping) [144-145].
- Encapsulation: invariant-checking costs are paid once at construction (sidebar) [146]; reach for `_` and `__` protection, but accessing a name-mangled attribute from outside is a lint-detectable red flag [148-149]; no reflexive getters/setters, return copies of mutable internals [149]. **AGAINST** Java-style getters/setters.
- Prefer free functions over `@staticmethod`/`@classmethod` [151]. **CONTRARIAN**
- Decision guide (Figure 10-1): dict for runtime key/value mappings (TypedDict only to parse JSON/YAML, then convert), Enum for a scalar from a fixed set, dataclass for an independent bundle, class when invariants exist [152]. **KEY**

## Ch 11 -- Defining Your Interfaces [153-171]

- Paradox of code interfaces: you get one chance to design an interface but it is used far more often than written, so usability is worth paying for up front [155].
- Meyers' rule: easy to use correctly, hard to use incorrectly [157].
- Design methods: TDD as a design technique (write the calling code first), README-driven development (write the docs first), usability testing with colleagues [158-159].
- Natural interactions: an `Order` with a confirmed flag whose operations refuse when unconfirmed [164-165]; magic methods such as `__add__` doing unit conversion so the reader's intuition holds [166].
- Context managers for anything that must be undone (reserve/unreserve ingredients); errors of omission -- the caller forgetting the second half -- are the failure mode they prevent [169-170]. **KEY**

## Ch 12 -- Subtyping [173-185]

- Inheritance is for "is-a" with behavioural substitutability; multiple inheritance only for mixins [175-176]. **AGAINST** general multiple inheritance.
- Square/Rectangle and a `RestrictedMenuRestaurant` with an early return show subclasses that silently break callers' assumptions [177-179].
- Liskov stated as invariants, preconditions, postconditions: a subtype keeps the base's invariants, may not strengthen preconditions, may not weaken postconditions [180]. **KEY**
- Red flags in an override: if-checks on arguments at the top, early returns, different exceptions (especially `NotImplementedError`), skipping `super()` [181].
- Base class authors: avoid changing invariants, tie invariants to protected fields, document them (most important) ; derived class authors: know the base's invariants, call `super`, honour the contract [182-183].
- Composition ("has-a") couples more weakly than inheritance; reach for it first [183-184]. **KEY**
- Duck typing is subtyping too and the same substitutability rules apply [184-185].

## Ch 13 -- Protocols [187-198]

- Problem: a function that needs only `.split_in_half()` and `.name`; typing it as `Any` throws away checking ("cannot condone"), a `Union` of concrete classes is fragile, a base class hierarchy explodes, mixins are "unpythonic" [189-192]. **AGAINST** all four.
- A `Protocol` defines structural typing: any class with the right members satisfies it, no inheritance [193]. **KEY**
- Rule of thumb: protocol when you care about structure, inheritance when you care about a behavioural contract with invariants [194]. **KEY**
- Composite protocols must themselves subclass `Protocol`; `@runtime_checkable` enables `isinstance`, and `issubclass` works only for non-data protocols [195-196].
- Modules can satisfy protocols too (plug-in modules) [196-197].

## Ch 14 -- Runtime Checking with pydantic [199-211]

- Typechecking stops at the boundary; a YAML config can be invalid in 67 ways the author enumerated in five minutes [203].
- `TypedDict` cannot express constraints and checks nothing at runtime [205].
- A pydantic dataclass catches 38 of 67; adding `constr`, `PositiveInt`, `conlist` reaches 55; `@validator` covers the cross-field rest [207-209]. **KEY**
- Parsing vs validation: pydantic parses (coerces) by default, so `"3"` becomes `3`; use `StrictInt` etc. when coercion is itself an error [209-210]. **CONTRARIAN** warn against default coercion.
- Closing: do not give dataclasses invariants; interdependent fields belong in a class or a pydantic model with validators [210]. **KEY**

## Part III intro -- Extensible Python [213]

- Extensibility is adding without modifying; the chapters that follow cover OCP, dependencies, composability, events, plug-ins [213].

## Ch 15 -- Extensibility [215-224]

- Shotgun surgery: a new notification kind requires edits scattered across the codebase; that is the smell of a closed design [217].
- Redesign: a `Union` of notification dataclasses plus `isinstance` dispatch in one place, and the Open-Closed Principle stated as the goal [219-221]. **KEY**
- OCP violation signals: identical conditional chains repeated, giant `if/elif` on a type, sprawling parameter lists, one change touching many files [222-223].
- Drawbacks admitted: extension points add indirection and cost; do not build them speculatively [223].

## Ch 16 -- Dependencies [225-242]

- Dependencies are liabilities as much as assets; left-pad; pin versions (sidebar) [226-228].
- Three kinds: physical (imports, calls -- visible, rigid), logical (same relationship via indirection, e.g. HTTP; enables substitution, invisible to tooling), temporal (ordering constraints) [228-236]. **KEY**
- Dependency inversion: let the system that owns the knowledge (the pizza maker) be depended on, not the payment system [230-231].
- "When code gets too DRY" sidebar: deduplicate only code that changes for the same reason; otherwise refactoring creates coupling [232]. **CONTRARIAN**
- Hidden logical dependencies (ordering of a list relied on by two subsystems) must be made apparent via a function, a type, or at least a comment [233-234].
- Temporal dependencies: mitigate by types (`NewType`-like "configured" state), by embedding preconditions in the callee, or by leaving breadcrumbs [235-236].
- Visualise with `pipdeptree`, `pydeps`, `pyan3`, cProfile+gprof2dot; high fan-in belongs at the bottom and must be stable, high fan-out (business logic) at the top [236-241].

## Ch 17 -- Composability [243-257]

- Composable = small, discrete, little business logic, reusable in ways not foreseen (spice rack vs spice blends) [243-244].
- An extensible design can still be non-composable (AutoKitchen preparers that drag whole dependency chains along) [246-247].
- Policy vs mechanism: business logic vs how it is done; `logging` is the model; split mechanisms out and policies become declarative [247-250]. **KEY**
- Pure functions and decorators compose mechanisms (`backoff` retry policy as stacked decorators vs hand-rolled retry loop that hides intent) [251-254].
- Algorithms compose too: replace a hand-written triple loop with `sorted`/`itertools.groupby`/`takewhile` driven by a `RecommendationPolicy` object [255-257].
- Cost: more files, more moving parts; beware over-flexibility [250].

## Ch 18 -- Event-Driven Architecture [259-269]

- Producers and consumers should depend on a transport, not on each other [260].
- Drawbacks: harder to follow, harder to debug, ordering and delivery guarantees [261].
- Simple events with PyPubSub; the Observer pattern as a plain `list[Callable]` ("Patterns Without Classes" sidebar) [262-266]. **CONTRARIAN** no class hierarchy for observer.
- Streaming events with RxPY for continuous data [266-268].

## Ch 19 -- Pluggable Python [271-282]

- Template Method as a dataclass of `Callable`s rather than the GoF abstract-class form [273-275]. **CONTRARIAN**
- Strategy as a single `Callable` parameter [275-277].
- Plug-ins via `stevedore` entry points with a `Protocol` as the contract; warn that the interface is checked only at runtime [277-281].

## Part IV intro -- Building a Safety Net [283]

- Safety net = static analysis + tests; the chapters cover why and which tests, then acceptance, property-based and mutation testing [283].

## Ch 20 -- Static Analysis [285-296]

- Pylint finds what mypy cannot: mutable default argument, inconsistent returns when `assert False` is stripped by `-O` [286]. **KEY**
- "Shift errors left" sidebar: the earlier an error is caught the cheaper; typecheckers, linters, tests in that order of cost [287].
- Write custom Pylint checkers: a 45-line plug-in that flags creating a `ReadyToServeHotDog` outside the blessed function, enforcing the `NewType` convention the language cannot [288-291]. **KEY** for a diff-check tool.
- Swiss-cheese model: stack linters, complexity checkers, security scanners; each has holes [292].
- Complexity heuristics: cyclomatic via `mccabe`, and a home-grown whitespace/indentation heuristic; no magic threshold [292-295].
- Security: `dodgy` for leaked secrets, `bandit` for flaw patterns [295-296].

## Ch 21 -- Testing Strategy [297-313]

- Write a test strategy as a list of questions about the system and the tests that answer each (Table 21-1) [297-299].
- Tests answer questions about quality ("value to some person"); weigh impact of failure against cost of the test, and skip tests whose cost exceeds their value [300-301]. **CONTRARIAN**
- The testing pyramid's labels do not matter; what matters is value-to-cost ratio, fast tests run often, slow ones on commit [301-302].
- Reduce test cost with AAA (Arrange-Act-Assert, plus Annihilate): big arrange blocks are a red flag; extract helpers and fixtures; mocks are fine but monkeypatching everywhere signals too-rigid physical dependencies [303-307]. **AGAINST** pervasive monkeypatching.
- Share nothing between tests; clean up through context managers or yielding fixtures so cleanup runs on failure too [308-309].
- Act stage one or two lines; parametrize for table-driven tests, but no more than three or four parameters [309-310].
- One logical assertion per test, with a message; Hamcrest matchers for a shared assertion vocabulary [310-313].

## Ch 22 -- Acceptance Testing [315-324]

- Unit/integration tests verify; acceptance tests validate that the right thing was built; developers' tests carry developers' bias [315].
- Gherkin Given-When-Then: plain language, shared vocabulary, requirements that are inherently testable; it forces vague requirements ("should be fast") into concrete ones [316-318].
- `behave` makes specifications executable: traceability from requirement to test; a new GWT clause without a step kick-starts a conversation [318-320].
- Parameterised steps, tables, step reuse, reports [320-324].

## Ch 23 -- Property-Based Testing [325-336]

- Properties are invariants of the output stated independently of a specific example; tests pinned to one specific result are fragile [325-326]. **KEY**
- Boundary value analysis is the manual approximation; Hypothesis generates inputs and found a `calories == 0` case the author had not considered [326-327].
- Toolkit: strategies, `assume`, `@example`, the failure database, and shrinking to a minimal reproducer [328-332].
- Stateful testing with `RuleBasedStateMachine` finds sequences of operations that break invariants [333-336].
- Property-based testing supplements example tests; it does not replace them [336].

## Ch 24 -- Mutation Testing [337-348]

- A brittle safety net is worse than none: a test suite that passes after deleting lines of production code proves it checks nothing there [337-339].
- `mutmut` mutates operators, constants, `continue`/`break`, etc.; surviving mutants are holes in the suite; three survived in the example (`<` vs `<=`, `0` vs `1`, `continue` vs `break`) [340-341]. **KEY**
- Fix by applying the mutant, writing the test that fails, reverting; export JUnit/HTML reports [342-343].
- Adopt selectively: only where tests are mature, on buggy or high-churn areas; `--use-coverage` to mutate only covered lines [344-345].
- Fallacy of coverage: 100% line coverage with thirty `assert foo is not None` tests is useless; coverage predicts absence of robustness, not presence; mutation score will be gamed too once it is a metric [345-346]. **AGAINST** coverage targets as a goal.
- Closing: everything in the book is a tool, not a rule; apply critical thought, ask what each practice costs [347].

---

## Ideas that could become a yes/no check on a Python diff

- Public function missing parameter or return annotations (ch 3, p 43-44; ch 6, p 82).
- `Any` introduced in an annotation, especially inside a collection type (ch 5, p 65; ch 6, p 81-82).
- Parameter typed `X = None` without `Optional`/`X | None` (ch 6, p 83).
- Function annotated to return `T` has a `return None` / bare `return` path (ch 3, p 42-43; ch 4, p 50).
- A `Union` with many members, or a `Union` appearing in a generated/added signature (ch 5, p 65; ch 7, p 104).
- `dict[str, Union[...]]` or `dict[str, Any]` used as a record type instead of a dataclass/TypedDict (ch 5, p 65-66; ch 9, p 132).
- `TypedDict` defined for data the code itself constructs rather than parses (ch 5, p 67; ch 9, p 133).
- New `namedtuple` where a dataclass would do (ch 9, p 133).
- Dataclass whose `__post_init__` or methods enforce cross-field rules (invariant in a dataclass) (ch 9, p 134; ch 14, p 210).
- Class with no invariant checks that could be a dataclass; or constructor that stores fields without any validation while the docstring states constraints (ch 10, p 137-140).
- Access to a name-mangled attribute (`obj._Class__x`) from outside the class (ch 10, p 148-149).
- Trivial getter/setter pairs added (ch 10, p 149).
- `@staticmethod`/`@classmethod` that could be a module-level function (ch 10, p 151).
- Class inherits directly from `dict`, `list`, `str` and overrides a method (ch 5, p 71-73).
- Multiple inheritance where the extra bases are not mixins (ch 12, p 175-176).
- Override that raises `NotImplementedError`, adds argument checks at the top, returns early, or omits `super()` (ch 12, p 181).
- `isinstance` chain on concrete classes where a `Protocol` or Union dispatch would fit (ch 13, p 189-192; ch 15, p 219-222).
- `IntEnum`/`IntFlag` introduced (ch 8, p 119-120).
- Enum used for values that are loaded at runtime (ch 8, p 115).
- String or int parameter where the accepted values are a small fixed set (candidate for `Literal`/`Enum`) (ch 4, p 55-56; ch 8, p 113-115).
- `NewType` value constructed outside its designated factory function (ch 4, p 58; ch 20, p 288-291).
- Pydantic model field with coercible type where strict was intended; `@validator` missing for documented cross-field rule (ch 14, p 207-210).
- Mutable default argument (ch 20, p 286).
- `assert` used to guard a code path whose fall-through returns `None` (ch 20, p 286).
- Resource acquired without a context manager, or cleanup after an `assert` in a test (ch 11, p 169-170; ch 21, p 308).
- Test with multiple unrelated assertions, or with arrange blocks much longer than act (ch 21, p 304-305, 310-311).
- Test that only asserts `is not None` / no exception (ch 24, p 346).
- `@pytest.mark.parametrize` with more than four parameters (ch 21, p 310).
- Use of monkeypatching where a dependency could be injected (ch 21, p 307).
- Retry/timeout loop written inline rather than as a decorator (ch 17, p 253-254).
- Same `if/elif` chain over a type duplicated in more than one place (ch 15, p 222-223).
- Unpinned dependency added to requirements (ch 16, p 227-228 sidebar).
- `# type: ignore` added to new code, or without `warn_unused_ignores` configured (ch 7, p 100-101).
- Cyclomatic complexity or indentation depth above a project threshold (ch 20, p 292-295).

## Ideas that are mindset or process rather than a check

- Code is asynchronous communication with a maintainer you will never meet; encode intent, not just behaviour (ch 1).
- Types are a vocabulary; build domain types so readers reason in domain concepts (ch 8).
- Make illegal states unrepresentable before writing defensive code (ch 4).
- Choose the type by the relationship it models: value set -> Enum, independent bundle -> dataclass, invariant -> class (Part II, ch 10 fig 10-1).
- Reach for composition and protocols before inheritance; inheritance is a behavioural contract, not code reuse (ch 12, 13).
- Validate at the boundary once, then trust the type inside (ch 14).
- Typecheck adoption is an investment curve: find pain, target strategically, lean on tooling, reach break-even early (ch 7).
- Keep the typechecker fast and visible or people stop running it (ch 6).
- Design interfaces from the caller's side first (TDD, README-driven, usability tests) (ch 11).
- Document invariants where the code is, with the business reason (ch 10).
- Separate policy from mechanism; mechanisms are what you reuse (ch 17).
- Dependencies are liabilities; point them at the owner of the knowledge; high fan-in must be stable (ch 16).
- DRY only what changes for the same reason (ch 16).
- Extension points cost; add them where the shotgun-surgery smell appears, not speculatively (ch 15).
- Write a test strategy as questions; weigh value against cost and skip low-value tests (ch 21).
- Acceptance tests validate the right product; write them with the customer in Gherkin (ch 22).
- Think in properties, not examples; let a generator find the boundary you forgot (ch 23).
- Measure the suite with mutants, not coverage; any metric becomes a target and gets gamed (ch 24).
- Stack many small defences (Swiss cheese); no single tool is the net (ch 20).
- Everything in the book is a tool to be weighed, never a rule to be enforced blindly (ch 24 closing).
