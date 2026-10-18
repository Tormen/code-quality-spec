# Effective Python, 3rd ed. (Slatkin, 2025) -- working notes

All 670 PDF pages were rendered and the notes checked against them (two readers, 2026-10-18).

Source: the book itself, 3rd edition, 670 PDF pages (read in full).
Page numbers below are the book's own (PDF page = book page + 27; the PDF has 670 pages, the book's numbered text runs to p. 626 plus index). Covers
Python up to 3.13; the preface says 35 of the 125 items are new in this
edition and that for some items the author's advice has reversed since the
2nd edition. Markers used: **[KEY]** = author stresses it as central;
**[CHANGED]** = new or reversed advice vs earlier editions / vs what the
author says most people do; **[CONTRARIAN]** = unusual against common Python
practice; **AGAINST:** = what the item explicitly argues against.

## Chapter 1: Pythonic Thinking (pp. 1-40)

- Item 1 (p. 1): Be sure which interpreter and which Python 3 version actually run your code (the `python` alias is unreliable); Python 2 is dead and out of scope. Read release notes to keep up.
- Item 2 (p. 3): Follow PEP 8 -- whitespace, naming, expression idioms (truthiness instead of length checks, inline `is not`), import placement and grouping -- because a shared style lowers the cost of reading and changing code. Delegate it to `black` and `pylint` rather than remembering it. AGAINST: `if len(x) == 0`, `if not a is b`, relative imports without the explicit dot, single-line compound statements, backslash continuations.
- Item 3 (p. 6): Python only catches syntax and literal errors before running; unbound names, bad arity, wrong types, division by zero all surface at runtime. So lean on linters/type checkers (flake8, typing), runtime assertions and tests instead of expecting the interpreter to protect you.
- Item 4 (p. 8): When a one-liner needs `or`-tricks, indexing and casts to express a default (the query-string example), neither a conditional expression nor a spread-out `if` rescues it -- the `if` version is even easier to copy-paste wrongly; split into intermediate variables and, as soon as the same logic is needed two or three times, a small named helper. The author's rule: what you gain in readability always outweighs brevity, and DRY applies to expressions too. AGAINST: `x = d.get(k, [""])[0] or 0` style boolean-default expressions.
- Item 5 (p. 11): Assign tuple parts to names by unpacking instead of indexing `[0]`, `[1]`: less visual noise, fewer lines, and it also does in-place swaps (the right side is built into a temporary tuple first) and `for` loop targets together with `enumerate`. Works on any iterable at any nesting depth, but the author explicitly does not recommend deeply nested patterns; unpacking does not work inside an assignment expression.
- Item 6 (p. 16): Always parenthesise one-element tuples, on the left or the right of `=`. A stray trailing comma (left over from editing a call or a literal) silently turns a function's result into a tuple; an unparenthesised `1,` cannot be dropped into a list literal without changing meaning; and on the left side `(a,), = ...`, `(a,) = ...` and `a, = ...` all run but yield different results. Formatters and static analysers only sometimes make it visible. **[CONTRARIAN]** even though bare `x = 1,` is legal.
- Item 7 (p. 19): A conditional expression is fine for one short assignment or call argument. A full `if` statement is better when you may later add a debug print or an `elif` branch; a helper function gives the one-liner back and is reusable. Avoid the expression when it must wrap (a formatter will spread it over more lines than the `if` anyway) or when it sits unparenthesised beside other operators -- unlike the walrus it needs no parentheses, so ambiguity is legal. Python's order (value-if-true first) differs from C's ternary, so a function in the true branch is never called when the test is false. When in doubt, the normal `if`. AGAINST: `and`/`or` chains to emulate a ternary (confusing, and wrong when the true branch is a falsy value).
- Item 8 (p. 24): Use the walrus `:=` (3.8+) where a value is fetched, tested and then used only inside that branch -- defining it on the line above makes it look more important than it is, as if the `else` branch needed it too -- and likewise when a variable is assigned under a condition and used shortly after, in `if/elif` chains that re-fetch, and for the loop-and-a-half `while True ... break`. Parenthesise only when it is a sub-expression (`(n := f()) >= 4`); otherwise leave the parentheses off to reduce noise.
- Item 9 (p. 30): Use `match` for destructuring heterogeneous nested data (tuples, dicts, class instances with guards and or-patterns), not as a switch replacement for simple equality tests -- there a plain `if` is clearer and `match` has the capture-pattern trap (a bare name in `case` binds instead of comparing; dotted names like enum members compare). **[CHANGED]** new item (3.10 feature). AGAINST: `match` on constants as if it were `switch`.

## Chapter 2: Strings and Slicing (pp. 41-76)

- Item 10 (p. 41): Keep `bytes` and `str` apart: decode at the input edge, work in `str`, encode at the output edge; write `to_str`/`to_bytes` helpers; open binary files with `rb`/`wb` and pass `encoding=` explicitly because the platform default varies.
- Item 11 (p. 47): Format with f-strings. C-style `%` is fragile to reordering, noisy for small value tweaks and repeats values; `str.format` fixes little of that. Learn the format-spec mini-language, but treat `str.format` as a historical artifact. AGAINST: `%` formatting, `str.format`. **[CONTRARIAN]** in dismissing `str.format` entirely.
- Item 12 (p. 58): `print`/`str` hide type (`5` vs `'5'`); when debugging use `repr` (or `!r` / `%r`) and give your own classes a `__repr__` that reconstructs the object; add `__str__` only when a different human-facing rendering is needed.
- Item 13 (p. 62): Adjacent string literals concatenate silently; inside list/tuple literals and multi-positional-argument calls always use an explicit `+`, because a missing or extra comma changes meaning invisibly. Implicit concatenation is acceptable for a single positional argument or keyword arguments. **[CONTRARIAN]** (most style guides allow implicit concatenation freely).
- Item 14 (p. 67): Slicing basics: omit `0` start and `len` end, negative indexes are fine, out-of-range slices are forgiving, slices copy, slice assignment can resize, `a[:] = ...` replaces contents in place.
- Item 15 (p. 70): Do not combine start, end and stride in one slice; prefer positive strides with no bounds, and split into two steps (or `itertools.islice`) otherwise. Negative strides on UTF-8 bytes also break. AGAINST: `x[-2:2:-2]`-style triple slices.
- Item 16 (p. 72): Split a sequence with a starred catch-all (`first, *rest = ...`) instead of index/slice pairs that must be kept in sync; the star always yields a list, so beware exhausting a big iterator into memory.

## Chapter 3: Loops and Iterators (pp. 77-108)

- Item 17 (p. 77): Loop with `enumerate(seq, start)` instead of `range(len(seq))` plus indexing.
- Item 18 (p. 79): Iterate related sequences together with `zip`; remember it stops at the shortest input -- pass `strict=True` (3.10+) when lengths must agree, or use `zip_longest`. **[CHANGED]** `strict=` is the new recommendation.
- Item 19 (p. 82): Never use `else` on `for`/`while`; its meaning (runs when no `break`, also on empty loops) is the opposite of what readers assume. Write a helper that returns early or uses a flag. **[CONTRARIAN]** vs people who like the search idiom.
- Item 20 (p. 85): Do not read a `for` loop variable after the loop: it is undefined when the loop body never ran. Comprehensions and `except` variables do not leak this way.
- Item 21 (p. 87): A function that iterates its argument more than once silently gets nothing the second time from an iterator. Either take a container (and detect iterators with `iter(x) is x` or `isinstance(x, Iterator)` and raise `TypeError`), or accept a factory; define containers via `__iter__` as a generator.
- Item 22 (p. 92): Do not add/remove items of a dict, set or list while iterating it -- behaviour is inconsistent (error, infinite loop, or silently fine). Iterate a copy, or stage changes in a side container and merge afterwards (then look in both during the loop). **[CHANGED]** new item.
- Item 23 (p. 98): Feed `any`/`all` a generator expression or generator, never a list comprehension, so they short-circuit and do no wasted work; they return real booleans unlike `and`/`or`. **[CHANGED]** new item.
- Item 24 (p. 102): Reach for `itertools` (chain, repeat, cycle, tee, zip_longest, islice, takewhile, dropwhile, filterfalse, batched, pairwise, accumulate, product, permutations, combinations) before hand-rolling iterator plumbing.

## Chapter 4: Dictionaries (pp. 109-134)

- Item 25 (p. 109): Since 3.7 `dict` iteration order is insertion order and may be relied on (kwargs, `__dict__` too), but dict-like classes implementing `MutableMapping` need not preserve it; defend by not depending on order, by checking `isinstance(x, dict)`, or by annotating `dict` and running a strict type checker.
- Item 26 (p. 117): For missing keys prefer `d.get(k, default)` (with a walrus when the default is costly to build) over `in`-checks or `KeyError` handling, which duplicate the assignment; `setdefault` is badly named and inserts the default object itself, so use it only for cheap defaults -- or move to `defaultdict`. AGAINST: `if k in d: ... else: ...` for counters; `setdefault` as a habit.
- Item 27 (p. 122): When you own the dictionary (internal state), use `collections.defaultdict` rather than `setdefault`; it avoids allocating a throwaway default on every call and reads clearly.
- Item 28 (p. 124): When the default depends on the key (e.g. open a file named by the key), neither `setdefault` nor `defaultdict` fits; subclass `dict` and implement `__missing__` to build, store and return the value.
- Item 29 (p. 127): Once bookkeeping becomes dicts-of-dicts or tuples longer than two, replace it with small classes (a frozen dataclass for the leaf, composing classes upward); the line count roughly doubles but readability and extensibility win. AGAINST: nested built-in containers more than one level deep, ever-growing tuples.

## Chapter 5: Functions (pp. 135-172)

- Item 30 (p. 135): Every argument is a reference (immutables merely look like pass-by-value), and an alias `b = a` is the same object, so a callee can append to a caller's list, rewrite a dict or assign attributes on a user-defined object. Rule for authors: never modify a mutable argument unless the function name, parameter names or docs say so. Rule for callers: pass a copy (`[:]`, `dict.copy()`), add helpers that produce defensive copies, or lean on immutable objects and pure functions. **[CHANGED]** new item.
- Item 31 (p. 138): Returning a tuple is fine while the caller unpacks at most three names (a starred catch-all counts as one). Beyond that two things go wrong: same-typed values get swapped silently at the call site, and the unpacking line gets so long that every PEP 8 wrapping of it hurts readability. Return a lightweight class (a `@dataclass`) instead -- clearer and easier to refactor. AGAINST: unpacking four or more return values.
- Item 32 (p. 142): Do not signal failure by returning `None` -- callers write `if not result` and confuse `None` with 0 or an empty string. A `(success, value)` tuple is no better, since callers discard the flag with `_`. Raise instead (e.g. convert `ZeroDivisionError` into a `ValueError` that says the inputs were bad); the caller then uses the result in `else` without a check. Document the exception in the docstring's `Raises:` -- Python's typing deliberately has no checked exceptions -- and annotate the return as never-`None`. AGAINST: `None` returns, `(success, value)` tuples.
- Item 33 (p. 145): Name lookup walks local, enclosing, module, builtin scopes, but assignment to an unknown name defines a new local -- so a closure that sets a flag in its parent silently sets its own copy (the "scoping bug", intended to keep function locals from polluting the module). `nonlocal` opts a name into the enclosing scope (never the module level; that is `global`), but the author warns against it beyond simple functions, as with globals: the side effects are hard to follow when the statement and the assignments are far apart. Once state grows, wrap it in a small class with `__call__` (`Sorter`), longer but easier to reason about and extend. AGAINST: `nonlocal` in long functions.
- Item 34 (p. 150): `*args` removes noise when callers pass a small, known number of literals or names (no more empty-list placeholders); `*seq` splats an existing sequence in. Two costs: the arguments are always materialised into a tuple, so `f(*generator)` can exhaust memory; and a positional parameter added in front later shifts every old call silently (the old message lands in the new slot without an error). Extend such functions with keyword-only arguments, and type annotations help catch the shift.
- Item 35 (p. 153): Keyword arguments clarify call sites, give defaults for optional behaviour, and allow extending a signature without migrating callers; always pass optional arguments by keyword, never positionally.
- Item 36 (p. 157): Default values are evaluated once at definition time, so a mutable or dynamic default (`{}`, `datetime.now()`) is shared across calls. Use `None`, document the real default in the docstring, and build it inside the body; works with `X | None` annotations.
- Item 37 (p. 161): Put `*` before boolean/optional flags so callers must name them, and `/` after implementation-named parameters so callers cannot couple to those names; parameters between may go either way. **[CHANGED]** positional-only `/` is 3.8+.
- Item 38 (p. 166): A hand-written decorator hides the wrapped function's name, docstring, module and pickling identity; always apply `functools.wraps` to the inner wrapper.
- Item 39 (p. 169): To pin arguments, `functools.partial` beats a `lambda`: shorter, exposes `.func/.args/.keywords` for debugging, handles keywords; `lambda` remains right only when argument ORDER must change. **[CHANGED]** new item.

## Chapter 6: Comprehensions and Generators (pp. 173-199)

- Item 40 (p. 173): A list/dict/set comprehension reads better than `map`/`filter` because it needs no `lambda` (the one exception the author grants: `map` with an existing single-argument function), filters inline with `if`, and the `dict(map(...filter(...)))` equivalent must be split over several lines. The one thing `map`/`filter` buy is that they return lazy iterators while a list comprehension materialises everything -- and generator expressions (Item 44) give that too. AGAINST: `map`, `filter`.
- Item 41 (p. 176): At most two control sub-expressions per comprehension -- two loops (flattening a matrix, or mirroring a two-level input), two conditions (adjacent `if`s are an implicit `and`), or one of each. A third loop forces line-wrapping and is no shorter than nested `for` statements; a condition per loop level is "extremely difficult to read", worst in a dict comprehension that already carries key and value. Beyond two, write normal `if`/`for` statements and a helper (often a generator). AGAINST: nested conditional comprehensions.
- Item 42 (p. 178): When a comprehension (list, dict, set or generator expression) repeats the same computation in its value and its condition, the two copies drift apart (the book's example changed one `8` to a `4`) and cost double; put a walrus in the condition and reuse the name in the value. Do not put the walrus in the value expression: the condition is evaluated first, so the name is not yet bound (`NameError`). Walrus names leak into the enclosing scope like `for` statement variables, whereas comprehension loop variables do not.
- Item 43 (p. 182): A function that accumulates results with `append` and returns the list has two problems: the `result.append(...)` bulk buries the value being produced (roughly half the characters are plumbing), and every result must fit in memory before anything is returned. A generator yields each value where it is found, reads better, and its working memory is bounded by one input unit (one line of a file), so it handles arbitrarily large input; the caller wraps it in `list()` when a list is really needed. Caveat: the returned iterator is stateful and single-use.
- Item 44 (p. 184): A list comprehension allocates one output per input, which can crash on a huge file or never finish on a socket; a generator expression (`(...)`) evaluates to an iterator at once, makes no progress until `next`, and holds little memory. Generator expressions compose -- feed one iterator into the `for` of the next and each step pulls through the chain -- and such chains run fast, so they are the author's tool for streaming large input. Same caveat: stateful, iterate only once.
- Item 45 (p. 186): Compose generators with `yield from` rather than nested `for ... yield` loops; it is clearer and a little faster.
- Item 46 (p. 188): Do not use the generator `send()` method to push data in -- it is unintuitive and interacts badly with `yield from` (spurious `None`s). Pass an input iterator as an argument and call `next()` on it. **[CONTRARIAN]** rejects a language feature outright. AGAINST: `send()`.
- Item 47 (p. 195): Likewise avoid the generator `throw()` method; the exception-driven control flow is hard to follow. Model state transitions with a small class (e.g. a timer with `tick`/`reset`/`__bool__`). AGAINST: `throw()`.

## Chapter 7: Classes and Interfaces (pp. 201-264)

- Item 48 (p. 201): For a hook or callback a plain function is enough; when the hook must hold state, prefer a tiny class with `__call__` over a closure with `nonlocal`, because the class makes the purpose visible.
- Item 49 (p. 205): A long `if isinstance(...)/elif` chain over node types should become a class hierarchy where each type implements the method; dispatch happens at runtime and new types slot in without editing one giant function. AGAINST: `isinstance` dispatch chains. **[CHANGED]** new item.
- Item 50 (p. 210): The counter-point to 49: when many independent behaviours operate on the same simple data, OOP spreads each behaviour across every class file and tangles dependencies; `functools.singledispatch` lets each behaviour live in its own module and register per type. Pick by how independent the systems are; mixing is fine. **[CHANGED]** new item; **[CONTRARIAN]** against class-centric organisation.
- Item 51 (p. 217): Use `@dataclass` for data-holding classes: it removes `__init__`/`__repr__`/`__eq__`/ordering boilerplate, supports `kw_only=True`, `field(default_factory=...)` for mutable defaults, `asdict`/`astuple`, and type annotations feed static checkers. Know the manual equivalents so you can leave dataclasses when they no longer fit. **[CHANGED]** new item, flagged as very valuable.
- Item 52 (p. 230): Python has one constructor; use `@classmethod` alternative constructors (taking `cls`) so generic orchestration code can build any subclass without knowing it. **[KEY]** for factory-style designs.
- Item 53 (p. 235): Always initialise parents with zero-argument `super().__init__()`; calling `Parent.__init__(self)` directly breaks under multiple inheritance (order) and diamonds (double init). MRO is C3; pass arguments to `super` only to reach a specific class's implementation. AGAINST: explicit parent `__init__` calls.
- Item 54 (p. 240): Avoid general multiple inheritance; when you want shared behaviour, write mix-ins: classes with methods only, no `__init__` or instance attributes, overridable via a hook method, composable with each other.
- Item 55 (p. 245): Prefer public attributes; `__private` name mangling is trivially bypassed and makes subclassing brittle when the hierarchy changes. Use single-underscore protected names with a comment on intent; reserve `__` for avoiding name clashes with subclasses you do not control. **[CONTRARIAN]** vs encapsulation habits from other languages.
- Item 56 (p. 250): Prefer `@dataclass(frozen=True)` for immutable value objects: it gives `__eq__`, `__hash__` (usable as dict keys/set members), `dataclasses.replace()` for copies with changes, and static checkers flag mutation. A note positions `namedtuple` as acceptable only for genuinely sequential data. **[CHANGED]** new item.
- Item 57 (p. 260): Subclassing `list`/`dict` is fine for simple extensions; for a container that is not a built-in subclass, inherit from `collections.abc` (`Sequence`, `MutableMapping`, ...) which enforces the required dunder methods and fills in the rest (`index`, `count`, ...).

## Chapter 8: Metaclasses and Attributes (pp. 265-317)

- Item 58 (p. 265): Never write `get_x`/`set_x` methods; start with public attributes, and move to `@property` with a setter only when assignment needs validation, derived updates or immutability. Properties must be fast and free of surprising side effects (no I/O, no mutating unrelated state in a getter). AGAINST: Java-style accessors.
- Item 59 (p. 270): `@property` lets you turn a plain attribute into a computed one without touching call sites -- a migration tool for a better data model. If you keep piling properties on, refactor the class instead.
- Item 60 (p. 274): When the same validation applies to several attributes or classes, write a descriptor (`__get__`/`__set__`) rather than repeated properties; use `__set_name__` to store per-instance state on the instance itself so nothing leaks memory (not a dict keyed by instance).
- Item 61 (p. 279): `__getattr__` runs only for missing attributes (good for lazy loading once), `__getattribute__` and `__setattr__` run on every access/assignment (hooks for validation/persistence). Inside them, always go through `super()` to avoid infinite recursion; raise `AttributeError` for truly missing names.
- Item 62 (p. 285): To validate a class at definition time, use `__init_subclass__` (always calling `super().__init_subclass__()`) rather than a metaclass: shorter, composable across multiple inheritance, and avoids metaclass conflicts.
- Item 63 (p. 293): Same for class registration (reverse lookup from a name to a class, e.g. deserialisation): `__init_subclass__` registers automatically so a subclass can never be forgotten. AGAINST: manual `register(...)` calls after each class.
- Item 64 (p. 299): A descriptor that needs to know the attribute name it was assigned to should implement `__set_name__` instead of relying on a metaclass or a redundant string argument.

- Item 65 (p. 303): Class bodies are evaluated in order and `cls.__dict__` preserves that order, so a base class's `__init_subclass__` can derive an ordered field list (e.g. CSV column positions) from the attributes a subclass declares -- with descriptors doing conversion, or a marker decorator picking out workflow steps. Avoids repeating field names in a parallel string tuple. **[CHANGED]** new item.
- Item 66 (p. 310): To change every method/attribute of a class (e.g. wrap all in tracing), use a class decorator -- a function taking and returning the class -- not a metaclass: metaclasses conflict when a base already has one and cannot be stacked; decorators compose freely.

## Chapter 9: Concurrency and Parallelism (pp. 319-397)

- Item 67 (p. 320): Drive child processes with `subprocess` (`run` for simple cases, `Popen` for pipelines and parallel children); pass `timeout=` to `communicate` so a stuck child is terminated instead of hanging the parent. AGAINST: `os.popen`/`os.exec*`.
- Item 68 (p. 324): Because of the GIL, threads give no CPU speed-up -- the factorisation benchmark runs no faster threaded. Threads are for blocking I/O (system calls release the GIL) and for simple apparent concurrency. A note mentions the experimental free-threaded 3.13 build.
- Item 69 (p. 330): The GIL does not make your data structures safe: `+=` on a shared counter is several bytecodes and gets preempted mid-way. Guard shared mutable state with `threading.Lock` in a `with` block.
- Item 70 (p. 333): For a threaded pipeline use `queue.Queue`: blocking `get` (no busy-wait), `maxsize` for back-pressure, `task_done`/`join` to know when a phase is drained, and `shutdown()` (3.13) to stop workers cleanly. A hand-rolled deque+lock queue gets all four wrong. **[CHANGED]** updated for `Queue.shutdown`.
- Item 71 (p. 344): Recognise the moment a single-threaded program needs fan-out/fan-in (e.g. I/O per cell per generation in Game of Life); Python offers several tools for it and each has trade-offs covered in 72-75.
- Item 72 (p. 349): Do not spawn a fresh `Thread` per unit of work on demand: each costs ~8 MB, startup and context-switch overhead, requires locks, and exceptions raised inside die in the thread with only a stderr trace. AGAINST: thread-per-task fan-out.
- Item 73 (p. 353): A fixed worker pool over `Queue` fixes memory and startup cost but forces heavy refactoring -- extra worker classes, manual exception forwarding, a fixed parallelism number -- and every new I/O point means another pipeline stage.
- Item 74 (p. 361): `ThreadPoolExecutor` gives the pool benefits with little refactoring and propagates exceptions through `Future.result()`, but `max_workers` still caps I/O parallelism; good where no async API exists (blocking file I/O).
- Item 75 (p. 364): For thousands of concurrent I/O operations use coroutines (`async`/`await`, `asyncio.gather`): near-zero per-task cost, no locks (single thread), exceptions debuggable in place, and adding I/O to another function means adding keywords rather than restructuring. **[KEY]** the recommended end state for I/O concurrency.
- Item 76 (p. 368): Porting threaded blocking I/O to asyncio is mostly mechanical: every sync construct (`for`, `with`, generators, comprehensions, context managers, `iter`/`next`) has an async twin; the socket layer gets replaced by `asyncio` streams. Gaps remain (no async `itertools`, no async `yield from`).
- Item 77 (p. 381): Migrate incrementally, not big-bang: top-down (`async def` entry point, wrap blocking calls in `run_in_executor`, push coroutines downward) or bottom-up (async leaf versions, sync wrappers via `run_until_complete`, delete wrappers as callers convert). `TaskGroup` (3.11) for fan-in. Some leaves are not worth porting. **[CHANGED]** new item.
- Item 78 (p. 389): Any blocking system call inside a coroutine (even `open`/`write`/thread start) stalls the whole event loop; detect it with `asyncio.run(..., debug=True)`; for clean code, wrap such I/O in a helper thread class that exposes coroutine-friendly methods via `run_coroutine_threadsafe` and its own loop. **[CHANGED]** new item.
- Item 79 (p. 393): For CPU parallelism swap `ThreadPoolExecutor` (which is even slower than serial on CPU work, because of the GIL plus pool overhead) for `ProcessPoolExecutor` -- one changed line, 3.3x faster on the gcd benchmark. Under the hood each item is pickled, sent over a local socket to a child interpreter, computed, pickled back and merged, so it pays off only for isolated (no shared state) and high-leverage (little data in, much computation) functions. The author's progression: thread pool first, then process pool, and the rest of `multiprocessing` (shared memory, cross-process locks, queues, proxies) only when everything else is exhausted -- it is harder to reason about than threads and adds sockets. AGAINST: raw `multiprocessing` APIs.

## Chapter 10: Robustness (pp. 399-446)

- Item 80 (p. 399): Use each clause of `try/except/else/finally` for its role: `finally` for cleanup that must run whether or not the `try` raised (and it also runs when an exception is raised in `else`); `except` for the exceptions you expect from the `try`; `else` for the success-path code, which keeps the `try` body minimal and makes it visually clear that exceptions raised there propagate rather than being caught by the handler above. Acquire the resource (`open`) before the `try`, so a failure to acquire does not run the cleanup.

- Item 81 (p. 404): `raise` reports expected failure conditions to callers; those exceptions are part of the function's interface like its arguments and return value, so they are documented and covered by tests. `assert` states an assumption the implementation relies on; its failure means a bug, its message (the second operand) is a debugging aid for the programmer, and callers must never catch `AssertionError` or `Exception` around it. Same validation can be written both ways (`Rating` raises, `RatingInternal` asserts because validation happened elsewhere): externally facing APIs raise, internal code asserts -- and assertions must stay enabled (Item 90). **[CHANGED]** new item.
- Item 82 (p. 408): `with` replaces the repetitive `acquire; try: ... finally: release` and makes a forgotten release impossible. For your own setup/teardown, `@contextlib.contextmanager` on a generator (set up, `try: yield` the resource, `finally:` restore) is far less code than a class with `__enter__`/`__exit__`; exceptions from the block re-raise at the `yield`. Yield a value to supply the `as` target, which lets the block work on the resource directly, highlights the critical section, and decouples creating the context from acting in it (change the logger name in one place).
- Item 83 (p. 412): Put exactly one source of expected exceptions inside a `try`; everything else goes in `else` or a separate `try`, otherwise a second failure site is silently swallowed by a handler written for the first.
- Item 84 (p. 414): Unlike `for` loop variables, the `except ... as e` name is gone once the block ends -- also inside the `finally` of the same statement (`NameError`). To log the outcome of each branch, assign to a second variable in every branch, and initialise it before the `try`: otherwise an exception type no `except` covers makes `finally` raise `NameError` chained onto the real error. Another case of Python scoping variables inconsistently (comprehension variables, walrus leaks, `for` variables each differ). **[CHANGED]** new item.
- Item 85 (p. 416): Catching `Exception` is legitimate to insulate the rest of a program from one part (a scheduled report must not crash the point-of-sale system around it), but it also swallows real bugs: a typo in a function name raises `NameError` at runtime, which inherits from `Exception` and is reported as a transient failure forever. Mitigation: a broad handler always prints or logs both `type(e)` and `e`, so someone reading the console can tell a bug from a hiccup.
- Item 86 (p. 419): `KeyboardInterrupt`, `SystemExit`, `GeneratorExit` (and possibly more in future) derive from `BaseException`, not `Exception`: Python uses them as control-flow mechanisms, not error reports, and the runtime relies on them passing through to the entry point, so `except Exception` lets Ctrl-C terminate a loop correctly. Do cleanup with `try/finally` or `with`, which handle both branches of the hierarchy for free, instead of `except BaseException`; where you must catch one (ask "terminate?" on Ctrl-C), end with a bare `raise` so the traceback is unmodified. Trap shown: a logging decorator whose `finally` reads a variable set only in `except Exception` crashes with `UnboundLocalError` on `SystemExit`; the fix there is to catch `BaseException`, with care.
- Item 87 (p. 424): In servers or anywhere exceptions are caught centrally, `repr(e)` is not enough; use the `traceback` module (`print_tb`, `extract_tb`) to log frames, or to serialise structured error records. **[CHANGED]** new item.
- Item 88 (p. 428): An exception raised inside an `except` block gets the one being handled attached as `__context__` automatically, so nested handlers (cache miss -> server miss -> API error) print a three-deep chain that confuses more than it helps. `raise X from e` sets `__cause__` and `__suppress_context__`, so the default printer shows only the cause you chose -- the way to convert a third-party exception into your module's own (Item 121) while still pointing at the real origin; `from None` hides the cause entirely. Only the built-in printer honours this: code that walks `traceback.extract_tb` itself must follow `__cause__`, then `__context__` unless suppressed, to reconstruct the chain. **[CHANGED]** new item.
- Item 89 (p. 436): In a normal function `finally` runs before the caller gets the value; in a generator it runs only after exhaustion (`StopIteration`) -- after the last item was consumed -- and if the consumer stops early (a `break`), not until the garbage collector throws `GeneratorExit` into it, which may be never. That cleanup then runs on the GC's stack, not the caller's: an exception raised there is printed to stderr as "Exception ignored" and the program continues, so neither `finally` nor handlers in a generator can be relied on to report errors or release a lock in time (deadlock risk). Therefore acquire files and mutexes outside, in a `with` around the loop, and pass the handle in; the generator then owns nothing that needs cleaning up. The author calls `GeneratorExit` a deliberate trade-off (no leaks from abandoned generators) that you must plan for. **[CHANGED]** new item; **[CONTRARIAN]** vs the common `with open(...)` inside a generator.
- Item 90 (p. 442): `assert` is sugar for `if __debug__: ... raise AssertionError`; the only way to make `__debug__` False is the `-O` flag at startup (it cannot be assigned at runtime), and that skips every assertion. Never do it: frameworks and libraries now depend on their assertions running at startup and runtime, the gain is small, real speed comes from profiling and native code (Items 92, 94), and even passing assertions narrow a bug report by ruling things out. A truly expensive check gets your own `enable_debug` switch, not `__debug__`. Use assertions liberally. **[CONTRARIAN]**; **[CHANGED]** new item.
- Item 91 (p. 445): `eval` runs one expression string and returns its value; `exec` runs a block and returns `None`, so results come back through the globals/locals dicts you pass. Finding either in ordinary application code is a red flag that something is seriously wrong: connected to any input channel they hand an attacker code execution. Even plug-in architectures have better options (dynamic imports, Item 98; `getattr`/`setattr`, metaclasses, descriptors). The one legitimate home is developer tooling -- debugger, notebook, REPL, benchmark harness, code generator. **[CHANGED]** new item.

## Chapter 11: Performance (pp. 447-491)

- Item 92 (p. 448): Intuition about Python speed is unreliable (string handling and generators are fast, attribute access and function calls slow), so measure first and spend effort where Amdahl's law says it pays. Use `cProfile` (the pure-Python `profile` skews results), `Profile.runcall` on a test callable, `pstats.Stats` sorted by cumulative time; when a shared utility dominates, `print_callers`/`print_callees` show who is responsible. Note: profile the code, not the network or disk behind it, and warm caches first. Worked example: swapping a linear insertion scan for `bisect` gave ~40x.

- Item 93 (p. 453): After profiling (and before reaching for another language), compare candidate implementations of one narrow behaviour with `timeit` microbenchmarks, a scientific rather than whole-program approach. Pass `number` explicitly and large enough to beat system noise (timeit already disables GC), put scaffolding in `setup` so it is not timed, pass `globals=globals()` to reach your names, and normalise to time per iteration -- and per inner-loop item for kernel functions -- so numbers are comparable and trackable for regressions. `python -m timeit` picks the count itself and reports the best of five. Examples: set membership ~1000x faster than list; for keys expected to be present, `try/except KeyError` beats `get`, which beats `in`. **[CHANGED]** new item.
- Item 94 (p. 458): A full rewrite is legitimate when you need tail latency without GC pauses, fast startup beyond what precompilation and lazy imports give, libraries bound to another language (native GUI), unusual targets (supercomputers, microcontrollers), a single installable executable, or when PyPy, process pools and Dask are all exhausted. Before that, profile, fix algorithms and data structures (orders of magnitude for little effort), and then accelerate only the hot kernel functions, whose clear interfaces are natural seams: `ctypes` (no build step) or the C extension API in the standard library; NumPy, Numba (JIT, no build), Cython, mypyc (from annotations, AOT), CFFI, SWIG in the ecosystem. Porting costs: short Python becomes verbose, and equivalence needs extensive tests. **[CHANGED]** new item.
- Item 95 (p. 462): `ctypes` loads any library with the C calling convention (C, C++, Rust) from a path, no build integration; set `restype`/`argtypes` explicitly rather than wrapping in `CFUNCTYPE`, and `cast` arrays to pointers. Advantages over a C extension: pointers are freed with the Python object, the GIL is released during the call, and compilation stays in whatever build you already have. Downsides: only C-expressible types (no iterators, no duck typing), conversions copy data at the boundary and can eat the gain, and a wrong type corrupts memory with cryptic crashes (`faulthandler` helps). So wrap every import in a Python function that does the type mapping and asserts, and write unit tests against the raw symbols first -- they catch a library whose signature changed under you. **[CHANGED]** new item.
- Item 96 (p. 467): A C extension module talks to the Python API directly (object model, duck-typing protocols, reference counting), built with a minimal `setup.py` and tested from Python. A plain port of the `ctypes` example is about four times the C code and still only accepts lists of floats -- if that is as far as you go, it is not worth it. The payoff comes from using the protocols: `PyObject_GetIter`/`PyIter_Next` accept any iterable, `PyNumber_Multiply`/`PyNumber_Add` accept any numeric type (`Decimal`), so the module is both fast and Pythonic -- "Python's holy grail" -- at the price of manual reference counting and error propagation that are hard to get right. **[CHANGED]** new item.
- Item 97 (p. 475): Startup time matters because users see it (CLI tools run repeatedly, cold starts in servers), and CPython spends it compiling source to bytecode and then running every imported module's top level. Bytecode is cached in `__pycache__/*.pyc`; measurements on Django: cold 791 ms, second run 225 ms -- but deleting the `.pyc` files still gave 613 ms, because the OS file cache held the sources, and `.pyc` with a purged file cache gave 382 ms. Best case is both: precompile with `python -m compileall` before deploying (pip does it on install) and keep the files in memory (a RAM disk is worth considering). Shipping bytecode only (`compileall -b`, delete `.py`) is possible but no faster, so only do it for storage reasons. **[CHANGED]** new item.
- Item 98 (p. 478): A CLI with subcommands that imports every module at the top (PEP 8 style) pays every dependency's initialisation on every run -- the fast `adjust` command took as long as the slow `enhance`. `python -X importtime` prints self and cumulative load time per module and names the culprit. Move the `import` inside the branch, function or request handler that needs it; a web app then pays the cost on the first request for that feature only. A repeated `import` of a loaded module costs ~50 ns (about 20 additions; ten times a double-checked global, but no boilerplate) -- fine once per request, not in a kernel's inner loop. **[CONTRARIAN]** vs PEP 8's imports-at-top rule, deliberately. **[CHANGED]** new item.
- Item 99 (p. 485): It is easy to misuse the I/O tools and conclude Python is too slow even for I/O-bound work. Slicing a 20 MB chunk out of `bytes` copies it (~5 ms, capping a media server at ~200 clients per CPU); a `memoryview` exposes the buffer protocol, and slicing it yields another view without copying (250 ns -- the server is then bound by the socket, not the CPU). Receiving: `recv` + re-joining the cache copies again (33 ms per MB); `bytes` is immutable, but a `memoryview` over a `bytearray` can be assigned into, and `socket.recv_into`/`readinto` write straight into that slice (33 us per MB). **[CHANGED]** new item.

## Chapter 12: Data Structures and Algorithms (pp. 493-532)

- Item 100 (p. 493): Objects usually need several orderings, so a natural `__lt__` rarely makes sense; pass `key=` (an attribute, an index, or a transform such as `lower`). For several criteria return a tuple from `key` -- tuples compare element by element -- and negate numeric fields to flip one direction, since `reverse=` flips all of them. Only when a field cannot be negated (strings) use the stability of `sort`: several passes, lowest-priority key first; the author recommends that only if absolutely necessary because the tuple key is simpler to read.
- Item 101 (p. 499): `list.sort` is in place, cheaper and faster; `sorted` works on any iterable and leaves the input untouched -- arguably more Pythonic because it never surprises a caller by mutating. **[CHANGED]** new item.
- Item 102 (p. 501): Searching a sorted list with `index` or a scan is linear; `bisect_left` is logarithmic and works on any sequence type, giving orders of magnitude speed-ups.

- Item 103 (p. 504): `list.pop(0)` is linear, so a list used as a FIFO degrades quadratically with length; `collections.deque` gives constant-time `append`/`popleft`. Measure first if unsure.
- Item 104 (p. 509): For priority ordering, sort-after-every-insert and `list.remove` scale superlinearly; `heapq` (`heappush`/`heappop`/`heapify`) is logarithmic. Items need a natural order (`__lt__` + `functools.total_ordering`); handle cancellations by flagging and skipping rather than removing.
- Item 105 (p. 519): The `time` module's zone handling is platform-dependent and unreliable; use `datetime` with `zoneinfo`, keep everything in UTC internally, and convert to local only at the presentation edge. AGAINST: `time.strptime` with `%Z` across zones.
- Item 106 (p. 523): For money or anything where rounding matters, use `Decimal` built from strings (not floats), with `quantize` and an explicit rounding mode; `Fraction` for exact rationals.
- Item 107 (p. 526): `pickle` is only for trusted channels (it is code execution by design; JSON is for untrusted). To survive class evolution, register with `copyreg`: constructor defaults for new fields, a version number for removed fields, and a stable unpickle function name so classes can be renamed.

## Chapter 13: Testing and Debugging (pp. 533-574)

- Item 108 (p. 533): Write tests as `unittest.TestCase` subclasses with `test_`-prefixed methods; use `assertEqual`/`assertRaises` etc. instead of bare `assert` because they print both values; use `subTest` for data-driven cases; custom helpers must not start with `test`. pytest is fine once you outgrow it.
- Item 109 (p. 541): Prefer integration tests over unit tests in Python: because nothing checks that components fit together before runtime, tests that exercise real collaborators give more confidence than mock-heavy unit tests; add unit tests only where edge cases cluster. **[CONTRARIAN]** vs the unit-test-first orthodoxy; **[CHANGED]** new item.
- Item 110 (p. 547): Use `setUp`/`tearDown` for per-test isolation (temp directories) and `setUpModule`/`tearDownModule` for expensive shared harnesses such as a database.

- Item 111 (p. 550): When a dependency is too slow or hard to stand up, use `unittest.mock.Mock(spec=...)` so typos fail loudly; verify both the result and the calls made (`assert_called_once_with`, `ANY`, `call`); inject via keyword-only parameters or `patch`/`patch.multiple`; C-level attributes like `datetime.now` cannot be patched directly, so route them through a helper. Prefer under-specifying with `ANY` to brittle over-specification.
- Item 112 (p. 559): Mock boilerplate is a design signal: wrap a dependency's functions in one class so a single `Mock(spec=Class)` covers it, and add explicit seams (a module-level getter) for injecting fakes in end-to-end tests.
- Item 113 (p. 563): Floats differ by order of operations and architecture; test them with `assertAlmostEqual`/`assertNotAlmostEqual` (`places` or `delta`), or `math.isclose`, never `assertEqual`.
- Item 114 (p. 565): `breakpoint()` drops into pdb anywhere (conditionally too); learn `where/up/down`, `step/next/return/continue/quit`; post-mortem via `python -m pdb -c continue` or `pdb.pm()`.
- Item 115 (p. 570): `gc.get_objects` tells you what exists, not where it came from; `tracemalloc` snapshots compared by line or traceback find the allocation site of leaks; Memray is named as the community step up.

## Chapter 14: Collaboration (pp. 575-626; index pp. 627-641)

- Item 116 (p. 575): PyPI via `python -m pip` is where community modules live; mind licences; pair with venv.
- Item 117 (p. 576): Always work inside a `venv` so projects cannot conflict on transitive dependencies; reproduce with `pip freeze` / `pip install -r requirements.txt`; never move a venv, recreate it; Python's own version is not in the requirements file.
- Item 118 (p. 582): Every module, class and public function gets a docstring: one-sentence first line, then details; functions document arguments, return, raised exceptions, generator/coroutine behaviour and default values -- but omit type information already in annotations, so it lives in one place. Follow PEP 257.
- Item 119 (p. 588): Packages give namespaces (import by full module path or alias with `as` to avoid clashes) and, for external consumers, a stable API via `__all__` re-exported in `__init__.py`; within one team `__all__` is usually unnecessary. AGAINST: `import *` in application code.
- Item 120 (p. 593): Module-scope `if` statements can swap implementations per deployment environment (a `TESTING` constant on `__main__`, `sys.platform`, `os.environ`); move really complex configuration into config files (`configparser`).
- Item 121 (p. 595): Each module/API defines a root `Error(Exception)` and raises only subclasses: callers can catch everything the module meant to raise, anything else escaping is a bug in the module, and intermediate root classes allow adding specific exceptions later without breaking callers. AGAINST: raising bare `ValueError` from an API.
- Item 122 (p. 600): Break circular imports first by refactoring the shared data to the bottom of the dependency tree; otherwise prefer dynamic imports inside functions (simplest, small cost) or an import/configure/run split; do not solve it by reordering imports. AGAINST: import reordering.

- Item 123 (p. 605): When an API changes and callers cannot migrate in lockstep, emit `DeprecationWarning` via `warnings.warn` with a `stacklevel` that points at the caller; a `require(name, value, default)` helper keeps it short. Tests run with `-W error` to catch deprecated usage; production routes warnings into `logging` (`captureWarnings`) instead of crashing; the warnings themselves are unit-tested with `catch_warnings(record=True)`.
- Item 124 (p. 613): Annotate with `typing` and run a strict checker (mypy `--strict` in the book) to catch wrong argument types, missing `self`, missing `return`, `None` leaking out of an `X | None`. Practical rules: write code and tests first, annotate afterwards where valuable; prioritise API boundaries and the most error-prone code; do not chase 100 % coverage; run the checker in CI with its config in the repo; run it incrementally as you annotate. Forward references need string annotations; exceptions are not part of the type system. The author explicitly says small-to-medium programs, ad-hoc code, legacy codebases and prototypes may not be worth annotating at all. **[CONTRARIAN]** vs strict-everywhere typing policies.
- Item 125 (p. 621): Zip-based deployment (`zipimport`, `zipapp`) costs nothing in startup time, but real packages break: data files looked up beside the source are missing (few projects use `pkgutil.get_data`) and native extension modules cannot load from a zip. Use Pex/Shiv or PyInstaller instead. AGAINST: `zipapp` for anything with real dependencies. **[CHANGED]** new item.

## Cross-cutting observations

- Recurring moves: "start simple, migrate when it hurts" (public attribute -> property -> descriptor; dict -> defaultdict -> `__missing__`; tuple -> dataclass; function -> class with `__call__`; thread -> pool -> executor -> coroutine; `__init_subclass__`/class decorator before metaclass).
- Recurring enemies: silent wrong answers (trailing comma tuples, implicit string concatenation, `zip` truncation, `pop(0)` scaling, swallowed generator `finally`, `None` returns), and language features the author treats as traps (`for/else`, `send`/`throw`, `-O`, `eval`, metaclasses, `import *`, `setdefault`, `str.format`, `%`).
- Author's own explicit "most important" markers are rare; he marks importance through chapter intros: dataclasses (ch. 7), coroutines for I/O concurrency (ch. 9), integration tests (ch. 13), and measurement before optimisation (ch. 11).

## Items a linter or type checker can enforce mechanically

- 2 -- PEP 8: ruff E/W/N rules, `black`/`ruff format`; `if len(x) == 0` is PLC1802 (ruff `len-test`), `not a is b` is E714, relative imports SIM/TID rules, `import *` is F403.
- 3, 124 -- static analysis: pyright strict / mypy `--strict`.
- 6 -- single-element tuple without parens: pyright and ruff do not flag `x = 1,` directly; flake8-commas / ruff COM818 (trailing comma on bare tuple) catches it.
- 9 -- capture-pattern trap in `match`: pyright reports an irrefutable pattern not last; ruff has no rule.
- 10 -- missing `encoding=` on `open`: ruff PLW1514 (`unspecified-encoding`).
- 11 -- `%` and `str.format`: ruff UP031/UP032 (pyupgrade) rewrite to f-strings.
- 13 -- implicit string concatenation inside collections: ruff ISC001/ISC002/ISC003 (flake8-implicit-str-concat).
- 15 -- slice with start, end and stride: no ruff rule; trivially grep-able (`[a:b:c]` with three parts).
- 17 -- `range(len(x))` loop: ruff C0200/PLC0200 (pylint `consider-using-enumerate`); SIM113.
- 18 -- `zip` without `strict=`: ruff B905 (`zip-without-explicit-strict`).
- 19 -- `for/while ... else`: ruff PLW0120 (`useless-else-on-loop`) only catches the degenerate case; a ban needs a custom check (AST walk for `orelse` on loops).
- 20 -- loop variable read after loop: ruff PLW2901 flags redefined loop vars; "undefined if loop never ran" is pyright `reportPossiblyUnbound`.
- 22 -- mutating a dict while iterating: ruff PLE4703 (`modified-iterating-set`), B909 (`loop-iterator-mutation`).
- 23 -- list comprehension inside `any`/`all`: ruff C419 (`unnecessary-comprehension-in-call`).
- 26, 27 -- `setdefault`/`in`-check patterns: ruff SIM401 (`if-else-block-instead-of-dict-get`), C4 rules partially; `defaultdict` suggestion is pylint R1735-ish only.
- 32 -- returning `None` for failure: pyright strict flags inconsistent return types (`reportReturnType`); ruff RET501/RET502/RET503.
- 36 -- mutable default argument: ruff B006 (`mutable-argument-default`), B008 (function call in default).
- 37 -- keyword-only booleans: ruff FBT001/FBT002 (flake8-boolean-trap).
- 38 -- decorator without `functools.wraps`: ruff B019-adjacent; pylint has no rule; flake8-bugbear does not; a small custom AST check (inner `def` returned from a decorator without `@wraps`).
- 40 -- `map`/`filter` with `lambda`: ruff C417 (`unnecessary-map`), PLW0108 (`unnecessary-lambda`).
- 41 -- more than two clauses in a comprehension: no built-in rule; ruff C901/PLR1702 complexity rules approximate; custom AST check counts `generators` and `ifs`.
- 45 -- `for x in it: yield x`: ruff UP028 (`yield-in-for-loop`).
- 51, 56 -- dataclass misuse: ruff RUF008/RUF009 (mutable default in dataclass, function call in dataclass default).
- 53 -- `Parent.__init__(self)` instead of `super()`: ruff UP008 (`super-call-with-parameters`); pylint W0233/W0231 (non-parent-init / super-init-not-called).
- 55 -- `__private` names: pylint has no rule; a grep for `self\.__[a-z]` is enough.
- 58 -- getter/setter methods: no ruff rule; pylint has none; grep for `def get_`/`def set_` pairs.
- 62, 63, 66 -- metaclass use: grep `metaclass=`; no linter rule bans them.
- 69 -- unlocked shared state: not mechanically checkable in general; ruff has no rule.
- 76/78 -- blocking calls in `async def`: ruff ASYNC101/ASYNC102/ASYNC110/ASYNC230/ASYNC251 (flake8-async: open/sleep/subprocess in async functions).
- 80, 83 -- too much in a `try` body: ruff TRY300 (`try-consider-else`), TRY301 (`raise-within-try`), PLR1702; ruff SIM105.
- 81 -- `assert` for input validation: ruff S101 flags all asserts; B011 (`assert False`); the raise/assert split needs human review.
- 82 -- `try/finally` that could be a context manager: ruff SIM115 (`open` without `with`); general case is human.
- 84 -- exception variable used after `except`: pyright `reportPossiblyUnbound`; pyflakes F821.
- 85 -- bare/broad `except Exception` without logging: ruff BLE001 (`blind-except`), E722, S110 (`try-except-pass`), TRY203 (useless re-raise).
- 86 -- catching `BaseException`: ruff BLE001 covers it; pylint W0718/W0706.
- 88 -- `raise X` inside `except` without `from`: ruff B904 (`raise-without-from-inside-except`), TRY200.
- 89 -- `with`/`yield` inside a generator that owns a resource: no ruff rule; custom AST check (a generator function whose `yield` sits inside a `with` or `try/finally`).
- 90 -- `-O` / `__debug__` dependence: not a linter check; a CI assertion that the interpreter was not run with `-O`.
- 91 -- `eval`/`exec`: ruff S307 (`suspicious-eval-usage`), S102 (`exec-builtin`), PGH001.
- 98 -- imports inside functions: ruff PLC0415 (`import-outside-top-level`) flags them; this item wants them in specific places, so the rule needs an allow-list rather than a ban.
- 101 -- `sorted()` on a list where `sort()` was intended, or vice versa: not checkable; it is a design choice.
- 105 -- `time.strptime`/`time.localtime` for zone work: ruff DTZ001-DTZ012 (flake8-datetimez: naive datetime calls); `time` module use is a grep.
- 106 -- `Decimal(float)`: no ruff rule; grep for `Decimal(` with a float literal is possible.
- 107 -- `pickle` on untrusted input: ruff S301 (`suspicious-pickle-usage`), S403.
- 108 -- bare `assert` in tests and helper methods named `test_`: ruff PT009 (`pytest-unittest-assertion`) goes the other way (pytest style); pylint has none; the book's advice conflicts with pytest-style projects.
- 111 -- `Mock()` without `spec`: no ruff rule; grep for `Mock(` without `spec=`/`autospec=`.
- 113 -- `assertEqual` on floats: ruff PLR2004 is unrelated; pytest-style `==` on floats has no rule; grep for float literals in equality asserts.
- 117 -- venv use: `pip` refuses installs outside a venv with `PIP_REQUIRE_VIRTUALENV=1`.
- 118 -- missing docstrings: ruff D100-D107 (pydocstyle), D2xx/D4xx formatting; "omit type info already in annotations" is human.
- 119 -- `import *`: ruff F403/F405; missing `__all__` is ruff PLE0605/PLE0604 only for malformed ones.
- 121 -- raising built-in exception types from an API: ruff TRY002 (`raise-vanilla-class`), TRY003 (long messages), TRY004 (`type-check-without-type-error`).
- 122 -- circular imports: pylint R0401 (`cyclic-import`); ruff has none; `import-linter` contracts.
- 123 -- `warnings.warn` without `stacklevel`: ruff B028 (`no-explicit-stacklevel`).
- 124 -- missing annotations: ruff ANN001-ANN401 (flake8-annotations); pyright strict `reportMissingParameterType`, `reportUnknown*`.

## Items that need human/agent judgement and could be a yes/no check on a diff

- 4 -- Does any one-line expression combine `or`/indexing/casts to express a default that deserves a named helper?
- 5, 16 -- Is a tuple/sequence consumed with `[0]`/`[1]` indexes where unpacking (plain or starred) would name the parts?
- 7 -- Does a conditional expression wrap a line, nest, or sit unparenthesised beside other operators?
- 8, 42 -- Is a value fetched, tested and then used only inside the branch without a walrus (or with the walrus in the wrong place of a comprehension)?
- 9 -- Is `match` used as a `switch` on constants, or is a destructuring `if`-chain that should be a `match`?
- 10 -- Does any function mix `bytes` and `str` or decode/encode away from the I/O edge?
- 12 -- Does the diff add a class without a `__repr__` that reconstructs it, or debug-print with `str` where `repr` was needed?
- 14, 15 -- Is any slice written with redundant 0/len bounds, or with start+end+stride together?
- 21 -- Does a new function iterate its argument more than once without guarding against a one-shot iterator?
- 24 -- Does hand-rolled iterator plumbing duplicate something in `itertools`?
- 25 -- Does code rely on dict iteration order for an object that may be a non-`dict` mapping?
- 28 -- Is a key-dependent default built with `setdefault`/`defaultdict` where `__missing__` fits?
- 29 -- Is a dict-of-dicts, dict-of-tuples, or tuple longer than two carrying structured state that wants a dataclass?
- 30 -- Does a function mutate an argument without its name/docstring saying so?
- 31 -- Does any function return more than three values by tuple unpacking?
- 32 -- Does any function return `None` (or a success flag) to signal failure instead of raising?
- 33, 48 -- Is `nonlocal` used in a non-trivial closure where a small class with `__call__` would be clearer?
- 34, 35 -- Does a new positional parameter land after `*args`, or are optional arguments passed positionally at call sites?
- 37 -- Are implementation-named parameters left positional (no `/`) and boolean flags left non-keyword-only (no `*`)?
- 39 -- Is a `lambda` used to pin arguments where `functools.partial` would do?
- 41 -- Does a comprehension carry more than two control clauses?
- 43, 44 -- Does a function build a list by `append` and return it where a generator would stream; is a large intermediate materialised with `[...]` instead of `(...)`?
- 46, 47 -- Does anything call a generator's `send()` or `throw()`?
- 49, 50 -- Is a new `isinstance` dispatch chain added where polymorphism or `singledispatch` fits; or is behaviour spread across classes that would be clearer as a dispatch function?
- 51, 56 -- Is a hand-written data class (manual `__init__`/`__repr__`/`__eq__`) added where `@dataclass` (frozen for value objects) fits?
- 52 -- Does generic code instantiate a concrete class by name where a `@classmethod` constructor would allow substitution?
- 54 -- Does new multiple inheritance carry state or `__init__` in the extra bases (not a mix-in)?
- 55 -- Does the diff introduce `__double_underscore` attributes?
- 57 -- Is a custom container built without inheriting from `collections.abc`?
- 58, 59 -- Does the diff add `get_x`/`set_x` methods, or a property with I/O or side effects in the getter?
- 60, 64 -- Is the same validation repeated across properties where a descriptor with `__set_name__` would do once?
- 61 -- Does a `__getattr__`/`__getattribute__`/`__setattr__` access `self.` attributes without `super()`?
- 62, 63, 65, 66 -- Is a metaclass introduced where `__init_subclass__` or a class decorator would do?
- 67 -- Does subprocess use lack a `timeout`?
- 68, 72, 73, 74, 75, 79 -- Is a thread started for CPU work, a `Thread` created per task, or a `Queue`+worker pipeline hand-built where an executor or `asyncio` fits? Is `multiprocessing` used beyond `ProcessPoolExecutor`?
- 69 -- Is shared mutable state touched from threads without a lock?
- 70 -- Is a producer-consumer queue hand-rolled from a `deque` and a lock?
- 76, 77, 78 -- Does a coroutine call blocking I/O directly; does a migration to asyncio jump both ends at once instead of top-down or bottom-up?
- 80, 83 -- Does a `try` body contain more than the one call expected to raise; is success-path code in `try` instead of `else`?
- 81 -- Is `assert` used for a caller-facing condition, or `raise` for an internal invariant?
- 82 -- Is the same setup/teardown written as try/finally more than once where a `@contextmanager` fits?
- 84 -- Is the `except ... as e` name used after the block?
- 85, 86 -- Is `Exception`/`BaseException` caught without logging type and value, or without re-raising `BaseException`?
- 87 -- Does central error handling log only `repr(e)` rather than the traceback?
- 88 -- Does a re-raise inside `except` lack `from e` / `from None`?
- 89 -- Does a generator open a file/lock inside itself and rely on `finally` for cleanup?
- 90 -- Does any deploy/CI command pass `-O`?
- 91 -- Does application code call `eval`/`exec`?
- 95 -- Is a `ctypes` symbol called without a Python wrapper that maps the types, or without a unit test against the raw symbol?
- 100 -- Is a multi-key sort done with several `sort` calls where a tuple key suffices?
- 101 -- Does code call `.sort()` on a list it does not own (a caller's argument)?
- 102, 103, 104 -- Is a sorted list searched linearly, a list used as a FIFO with `pop(0)`, or a priority queue kept by re-sorting?
- 105 -- Is time-zone work done with the `time` module, or is non-UTC time stored internally?
- 106 -- Is money computed in `float`, or `Decimal` built from a float?
- 107 -- Is `pickle` used on data from outside the process, or without `copyreg` for a class that will evolve?
- 108, 110, 113 -- Do new tests use bare `assert` instead of `assertX` helpers, share state without `setUp`, or compare floats exactly?
- 109 -- Does the diff add mock-heavy unit tests where one integration test would cover the collaboration?
- 111, 112 -- Is a `Mock` created without `spec`; does mock setup repeat across tests, signalling a dependency to encapsulate?
- 118 -- Do new public functions/classes/modules have docstrings that cover args, return, raises, and omit types already annotated?
- 119 -- Is `import *` used in application code; does a public package re-export its API from `__init__`?
- 120 -- Is environment switching done by module-scope `if` on a constant, or sprawled through runtime checks?
- 121 -- Does a module raise built-in exceptions from its API instead of subclasses of its own root `Error`?
- 122 -- Is a circular import "fixed" by reordering imports?
- 123 -- Is a breaking API change made without a `DeprecationWarning` transition?
- 124 -- Are new API-boundary functions annotated; is the type checker run in CI?
- 125 -- Is the program bundled with `zipapp`/`zipimport`?

## Items that are mindset, process, or performance tuning rather than a check

1, 3 (as a stance), 24, 68, 71, 72, 73, 74, 75, 77, 79, 92, 93, 94, 95, 96, 97, 98, 99, 102, 103, 104, 109 (as a policy), 114, 115, 116, 117, 120, 124 (the adoption strategy), 125.
