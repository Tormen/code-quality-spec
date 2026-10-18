# Sweigart, Beyond the Basic Stuff with Python -- working notes

Page numbers in brackets are the book's printed page numbers. The PDF page is the printed page plus 28 (printed 233 = PDF 261).

## Introduction [xxi-xxv]

- Audience: people who finished a beginner tutorial and are stuck in the "desert of despair" between tutorials and professional practice; the book is meant to replace what one would otherwise learn piecemeal [xxi-xxii].
- Scope stated up front: readability and clean code, plus the professional toolchain (command line, formatter, linter, version control), big O and OOP design; chapters can be read out of order [xxii-xxiv].
- Part III's stated purpose is as much about when NOT to use OOP as how; the author says developers overuse classes because they believe everyone does [xxiv].
- Further reading named: Python Crash Course, Impractical Python Projects, Serious Python, Effective Python, Python Cookbook, Fluent Python; PyCon videos [xxv].
- (d) Introductory.

## Chapter 1 -- Dealing with Errors and Asking for Help [3-15]

- How to read a traceback: frames listed oldest first, the last frame is where Python noticed the problem, which is not necessarily where the bug is (missing parenthesis reported on the next line) [4-6].
- Search the error message, quoted, with the word python; strip the parts specific to your code (variable names, your types) from the search [7-8].
- (a) Use a linter (Pyflakes named) in the editor; static analysis catches typos and undefined names before running; the author calls linting effectively required for modern development [8-9, 15].
- Asking for help: an etiquette list -- ask directly, right forum, specific headline, say what the code should do, full error text, complete code, a minimal complete reproducible example, properly formatted (pastebin/gist, not screenshots), what was tried, OS and versions [9-14].
- Stack Overflow is an answer archive, hence strict; reddit learnpython as a gentler alternative [12].
- (d) Introductory for an experienced developer, entirely.

## Chapter 2 -- Environment Setup and the Command Line [17-42]

- Filesystem basics, pathlib with the / operator for portable paths, home and current working directory, absolute vs relative paths [18-21].
- Programs vs processes; the command line and why to learn it (setup needs it, faster, scriptable) [21-23].
- Command-line tour: running programs, arguments and options, python -c, py.exe launcher, subprocess.run for running commands from Python, tab completion, history [23-28].
- Side box worth noting: short command names are right for the command line because commands are typed more than read -- the opposite of the rule for identifiers in source code [32].
- Common commands cross-referenced Windows/Unix: glob wildcards, cd, dir/ls, find, cp, mv, del/rm, mkdir, rmdir, where/which, clear [28-35].
- Environment variables, PATH and its search order, adding to PATH per session and permanently (.bashrc/.zshrc) [35-39]; launching scripts without a terminal (bat file, .command file, shebang + chmod) [39-42].
- (d) Introductory tutorial; nothing here is a code-quality rule.

## Chapter 3 -- Code Formatting with Black [45-58]

- (a) Formatting is readability, and readability is what makes maintenance possible; its real value is ending arguments between collaborators, like agreeing which side of the road to drive on [45-46].
- PEP 8 is the reference style guide but its own authors say consistency within a project beats obedience to any single rule; the author follows Black because it is a compromise he can live with, not because he likes all of it [46-47].
- Horizontal spacing rules, each tied to a reading argument: spaces not tabs (tabs render variably, mixing is a TabError), four spaces per level; one space around operators so a slice plus does not read as an addition; no space before a comma, one after; no spaces around attribute dots; no space before call or index brackets so name and call read as one thing; no padding inside brackets; two spaces before an inline comment [47-50].
- (c) The author advises AGAINST end-of-line comments generally: they make lines too long [51].
- Vertical spacing: two blank lines between top-level defs/classes, one between methods (Black enforces); blank lines inside a function group conceptually distinct steps and are a judgement Black cannot make; Django EmailValidator as the example [51-52].
- (c) Against several statements per line with semicolons and against one-line if bodies; one import per line (diff-friendly); imports grouped stdlib / third-party / local -- Black does not touch imports [52-53].
- Black usage: pip install, run on file or folder, -l for line length (author prefers 120 over the default 88, 80 is a punch-card relic; whichever, one limit per project), -S to keep quote style, --diff to preview, fmt: off/on to protect hand-aligned blocks such as a column of constants [54-57].
- Closing distinction: tools make syntactic decisions, humans make semantic ones (names) [58].
- (d) Tutorial material for an experienced developer except the explicit reasons behind each rule and the two positions marked (c).

## Chapter 4 -- Choosing Understandable Names [59-67]

- Naming is a semantic decision no formatter can make; invest in it for anything that is not throwaway code [59-60].
- Casing: snake_case, camelCase, PascalCase; PEP 8's conventions listed (lowercase modules, PascalCase classes, UPPER constants, snake functions/variables, self/cls, underscore for private). (b) The author openly deviates: he uses camelCase for variables and functions throughout, arguing consistency matters more than which style [60-61].
- Length: err toward too long, because code is read more than written. Too-short names: one or two letters, abbreviations, single vague words; the accepted exceptions are i/j/k loop indices and x/y coordinates. Side box: do not drop letters (memcpy-style); unpronounceable means unreadable; a short phrase such as number_of_trials is fine [61-62].
- Scope sets descriptiveness: a short name suits a local in a short function; a global in a large program needs qualification [63].
- Too-long names: redundant prefixes (catWeight inside Cat), Hungarian notation (strName) is obsolete; but is_/has_ prefixes for booleans and unit suffixes (weight_kg) carry real information -- Mars Climate Orbiter as the cautionary tale [63-64].
- Sequential numeric suffixes (payment1, payment2) signal a missing list or a missing parameter; if the variants genuinely differ, name the difference [64].
- Searchability as a test for a name: a name that produces false hits on Ctrl-F (num, a, email) is too generic [64].
- (c) Against jokes, puns, cultural references: gooseDownload renamed to increaseDownloadSpeed; write for non-native speakers, polite, direct, humourless [64-65].
- Never shadow built-ins (list, set, all, any, id, input, max, min, open, str, sum, type, ...) and never name a module like an installed third-party one (pyperclip.py) [65-66].
- Worst names: data, var, temp, and combinations thereof [66].

## Chapter 5 -- Finding Code Smells [69-85]

- A smell is a prompt to investigate, not a verdict; preventing a bug is cheaper than finding it [69-70].
- Duplicate code: deduplicate into a function or loop, parameterising the parts that differ; the author tolerates one or two copies and starts acting at three or four, and notes that deduplicated code is sometimes harder to read than the copies [70-71].
- Magic numbers: name them as UPPER constants; separate constants for separate meanings even when the value coincides (cards in a deck vs weeks in a year); string magic values too, so a typo becomes a NameError instead of a silent miss (the 'nrth' direction example) [71-73].
- Commented-out code and dead code (unreachable branches, never-called functions) mislead readers; delete and rely on version control. Stubs (pass or raise NotImplementedError) are the sanctioned exception, and the raise form is safer because an accidental call fails loudly [74-75].
- Print debugging is a cycle of rerunning; use a debugger or the logging module, whose output is clearly marked as diagnostic rather than mixed with normal output [75-76].
- Numeric-suffix variables (password1/password2, x1/y1/x2/y2): rename to distinct names or collect into a list; a digit that is part of a proper name (IPv6) is not the smell [76].
- (b) Classes that should be functions or modules: a class with one method or only static methods is Java habit; modules already group functions; Diederich's "Stop Writing Classes" [77].
- Nested comprehensions and comprehensions with several for clauses: expand into loops; even experienced readers struggle with them [77-79].
- Empty except with pass hides errors and is worse than a crash because bad data flows on; error messages are for users: say what happened and what to do, not which function failed; a program that does not handle its possible exceptions is unfinished [79-80].
- (a)/(b) The five myths the author rejects as bad advice: single return at the end (a FORTRAN relic that produces convoluted if/else); at most one try per function; flag arguments are bad (only when the flag selects two unrelated code paths; sorted(reverse=) is fine); global variables are bad (limit them, constants are fine, small programs may use them); comments are unnecessary (bad comments are worse than none, but too few is the common failure) [80-84].
- Closing: best practice is not an objective measure; smells are things to consider [85].

## Chapter 6 -- Writing Pythonic Code [87-105]

- Zen of Python walked through aphorism by aphorism in the author's own reading: readable over clever, explicit over obscure language features, flat over nested hierarchies (deep dotted paths are a smell), sparse over dense one-liners, errors must not pass silently (returning None or error codes instead of raising is the way they do), one obvious way, now is better than never but a wrong answer fast is worse than waiting, namespaces for conflict avoidance only [88-91].
- Significant indentation defended: other languages indent anyway; Python only removes the brace-placement war [91-92].
- Idioms, each with the unpythonic counterpart: enumerate instead of range(len()) [92-93]; with instead of open/close because an exception skips the close [93-94]; is None instead of == None (== can be overloaded); but never is True / is False, write if x: / if not x: [94-95].
- Raw strings when there are many backslashes [95]; f-strings over % and format(); (c) the author discourages str.format() as convoluted; keep % or format() only for pre-3.6 code [96-97].
- (b) Shallow copy: the author does not recommend the [:] idiom in his own code and prefers copy.copy() for readability [97-98].
- Dictionaries: get() with a default instead of an in-check, setdefault() instead of check-then-assign, defaultdict when every key needs a default; a dict lookup as a switch replacement is allowed but may hurt readability [98-101].
- Conditional expressions: called ugly on purpose by Guido; introduced to kill the buggy and/or pseudo-ternary (falsy valueIfTrue bug); acceptable, never nested [101-102].
- Chained comparisons (42 < x < 99), chained assignment and chained ==, and x in (a, b, c) for one-of-many checks; the tuple form is also slightly faster [103-104].
- (d) Most of the idioms are known to an experienced developer; the two positions marked (b)/(c) are the author-specific content.

## Chapter 7 -- Programming Jargon [107-131]

- Glossary chapter: language vs interpreter (CPython as reference implementation, Jython, PyPy), garbage collection, literals, keywords (English-only), objects/values/identity, the variable-as-label (not box) metaphor with Ned Batchelder's talk, is vs == [108-113].
- Items, mutable vs immutable (table), in-place mutation vs rebinding, the mutable-list-inside-a-tuple case and the author's PyCascades talk on it [114-117].
- Indexes, keys, hashes (hashable = immutable in practice; same value same hash, identity differs), containers / sequences / mappings, dict insertion order since 3.7, dunder methods, modules vs packages, callables and first-class functions with the callTwice example [117-122].
- Commonly confused pairs: statement vs expression (print in 2 vs 3), block vs clause vs body, variable vs attribute, function vs method, iterable vs iterator (iter/next/StopIteration), syntax vs runtime vs semantic error, parameter vs argument, coercion vs casting (sum of booleans vs count), property vs attribute, bytecode vs machine code, script vs program, library vs framework (inversion of control) vs SDK vs engine vs API [122-130].
- (d) Entirely introductory for an experienced developer; no advice beyond "use the terms precisely".

## Chapter 8 -- Common Python Gotchas [133-151]

- Never add or remove list items while iterating over that list: appending loops forever (sock example), deleting skips the neighbour (yello example); build a new list instead, or a comprehension; modifying items in place is fine; iterating backwards works but is fragile -- Hettinger's answer to "how do I modify a list while looping" is: don't [134-140].
- Side box: a new list costs little because lists hold references; programmer time is worth more than memory [137-138].
- Assignment copies references, never objects, including into function parameters; copy.copy() for a flat copy, copy.deepcopy() for nested containers. (b) The author's general advice is to ALWAYS use deepcopy, since the slowdown rarely matters [140-142].
- Never use a mutable default argument (the sandwich list grows across calls); use None and create inside the function [143-144].
- Building a string by repeated concatenation in a loop creates a new object each time; append to a list and join -- ten times faster at 100 000 iterations, irrelevant at 100; do not avoid concatenation obsessively [144-146].
- sort() is ASCII-betical; use key=str.lower for alphabetical; Timsort trivia [146-147].
- Floating point is IEEE 754 and inexact (0.1+0.1+0.1, 2**53+1); use integers in the smallest unit or decimal.Decimal built from a string; precision is configurable [147-149].
- Never chain != (a != b != c does not mean all three differ) [149-150]; a single-item tuple needs its trailing comma [150].
- (d) Known to an experienced developer, but the "always deepcopy" stance is the author's own.

## Chapter 9 -- Esoteric Python Oddities [153-166]

- Framed as curiosities one is unlikely to meet; the educational value is understanding the interpreter [153].
- Preallocated small integers (-5..256) make 256 is 256 true and 257 is 257 false across statements; string interning likewise; never rely on either -- is is for None only [154-156].
- --x and +x are stacked unary operators, not increment/decrement; x++ is a syntax error [156-157].
- all([]) is True (vacuous truth); think "no item is falsy" [157-158].
- bool is a subclass of int, so True+True == 2 and 'hello'[True] works; unreadable, never do it; Python 2 let you rebind True [158-159].
- Mixing chained operators of different kinds (== and in) follows the a op b and b op c expansion and surprises [159-160]; import antigravity Easter egg; webbrowser module [160].
- (d) Entirely trivia for an experienced developer; the only advice is negative (do not rely on interning, do not use bools as ints).

## Chapter 10 -- Writing Effective Functions [161-179]

- Function names carry a verb and usually a noun; a method may drop the noun its class supplies; prefer the long descriptive name over an acronym (getGreatestCommonDenominator over gcd); do not shadow built-ins [162].
- (a)/(b) Function size: the author lists the benefits of small functions and the costs (more names, more docs, more relationships), then calls the "three or four lines" school madness; the 34-line getPlayerMove is shown against a six-function 56-line split that is harder to follow. His numbers: under 30 lines ideally, never over 200; as short as reasonably possible, not shorter [162-165].
- Parameter count: zero to three is fine, more than five or six is too many; split the function [165].
- Default arguments reduce parameter burden; never a mutable default [165-166].
- * and ** at the call site to unpack lists and dicts; * in a def for variadic positionals, ** for variadic keywords (formMolecule with 118 element parameters as the motivating case); choose one of "single iterable parameter" or "*args" by how callers will use it (sum vs min/max), do not support both unless needed [166-171].
- *args/**kwargs wrapper functions that forward everything (printLower) [171-172].
- Functional programming: side effects defined broadly (globals, files, screen, network, in-place mutation of an argument); deterministic functions are cacheable; pure = deterministic and side-effect free; benefits for testing, reproduction, threading; write pure functions whenever possible, avoiding globals, files, clock and randomness inside [172-174].
- Higher-order functions, lambdas only where a function needs no name (never assign a lambda to a constant, use def) [174-175]; (c) map()/filter() are outdated, comprehensions are faster and clearer [175-176].
- (a) A function returns one data type; returning None as an error signal is the Python form of Hoare's billion-dollar mistake and yields vague NoneType attribute errors far from the cause [177-178].
- (a) Raise exceptions, do not return error codes; str.find returning -1 silently becomes a valid negative index, str.index raises and is therefore preferable; exception class names end in Error when they denote errors [178-179].

## Chapter 11 -- Comments, Docstrings, and Type Hints [181-200]

- Programs are written for people; comments, docstrings and type hints keep code changeable [181-182].
- Multiline comment: a single triple-quoted string beats a run of # lines (contradicted by PEP 8 practice, see (b)) [182]; comment style: own line, complete sentences, same indentation as the code, blank # between paragraphs, one space after #, two spaces before an inline comment, links supplement but never replace a comment [183].
- Inline comments: only for the line they sit on; good uses are variable purpose, units and ranges at the assignment; never the data type [184].
- (a) Comments explain WHY, not what: "multiply by 1.5" is worse than nothing; "time-and-a-half wage rate" is right [184-185].
- Summary comments head a paragraph of code and let a reader skim [185]; lessons-learned comments may be pages long and are gold for maintainers; they are neither API docs nor tutorials [185-186].
- Legal headers short with a pointer to the license file; professional tone always, no venting [186]; codetags: TODO, FIXME, HACK, XXX -- the author recommends TODO only, and an issue tracker for anything serious [187].
- Shebang and the now-unnecessary coding line [187-188].
- Docstrings: triple double quotes, first string in a module (after magic comments) / class / def; requests.sessions as the example; __doc__ and help(); one-line summary, blank line, detail including parameters, return value, side effects; written for programmers, not users; a TODO inside an unfinished docstring; PEP 257 [188-190].
- Type hints: syntax, gradual typing, classes as types, subclasses accepted; (b) the author recommends hinting variables even where inference would do, so that a later change of value type is a deliberate change [190-191].
- Static analysers: Mypy as the popular one, Pyright/Pyre/Pytype named; run it from the editor; type: ignore sparingly -- rewrite instead [192-193].
- Union, Optional, Any: use all three sparingly; the fewer types a name admits, the simpler the code; a function that returns None for an error should raise instead; prefer from typing import X over typing.X [194-195]; container hints via typing.List etc. (pre-3.9 style) [195]; backported comment-style hints only for pre-3.5 code [196].
- (a) Summary stance: the belief that documentation is optional is self-serving; an inscrutable screen of code is the common failure, not over-documentation [197].

## Chapter 12 -- Organizing Your Code Projects with Git [199-223]

- Version control as a scalable undo; one repo per project; no project is too small for it [199-200].
- Cookiecutter (the author's basicpythonproject template) to lay out src/, tests/, docs/, README, LICENSE, .gitignore, tox.ini, pyproject.toml [200-202].
- Install, configure name and email, optional GUI tools (TortoiseGit etc.) as a convenience that does not replace the CLI [202-203].
- File states untracked / committed / modified / staged; git status often, watch "git status" in a second terminal [204-207].
- (b) The author sidesteps the staging area: recommends commit -am to go from modified to committed in one step, and committing immediately after any add/rename/remove, because staging is the main source of beginner confusion [206].
- .gitignore for temp files, bytecode, tool output, generated artifacts and files with secrets; commit the .gitignore itself [209-210].
- Commit messages: specific, not "updated code"; Django's history as the model; amend for a typo [210-211].
- git diff before every commit, difftool for a GUI [211-213].
- Commit granularity: a whole piece of functionality (feature, class, bug fix); never commit syntactically broken code; run the tests first and say in the message if they fail; people commit too rarely rather than too often [213-214].
- Delete and rename only through git rm / git mv so history follows the file [214-216]; log, --oneline, -n, show [216-217].
- Recovery: restore for uncommitted edits, restore --staged to unstage, revert -n for the last N commits (history only grows), checkout <hash> -- <file> for one file [217-220].
- Secrets committed by accident need history rewriting (filter-branch, BFG); prevention is a secrets file listed in .gitignore and read at runtime [220].
- GitHub: remote add, push -u, clone; cloning afresh is the escape hatch (xkcd 1597) [221-223].
- (d) A Git tutorial throughout; the only opinions are the commit-am shortcut, commit granularity and message quality.

## Chapter 13 -- Measuring Performance and Big O Algorithm Analysis [225-245]

- Performance rarely matters for small scripts; measure before optimising [225-226].
- (c) Against clever tricks: the XOR swap is both less readable and, measured with timeit, twice as slow as a temp variable; tuple unpacking is the most readable and the fastest. Readability first, then measure [226-227].
- timeit basics: statement string, setup string, number, globals=globals(); make it work, then make it fast [226-228].
- cProfile for whole functions; the output columns; the RSA cipher example shows pow() eating 28.6 of 28.9 seconds, so optimising readKeyFile would be pointless [228-229].
- Amdahl's law: speeding up the part that dominates runtime pays, speeding up a small part does not [229-230].
- Big O as "how code slows as data grows" (Batchelder); orders O(1) through O(n!) with the bookshelf metaphor; the quick classification: constant and log are fast, n and n log n are fine, quadratic and up are slow [230-233].
- All efficient general sorts are O(n log n); Python's sort is Timsort [233].
- O(n^2) is the order to watch for: in the author's experience the most common real use of big O is noticing an accidental quadratic algorithm where a linear or n-log-n one exists; bookshelf duplicate-check example [233].
- Exponential and factorial orders explained with "photograph every subset / every ordering of the shelf"; traveling salesman as the O(n!) example [233-235].
- Big O describes the worst case; big Omega (best) and big Theta (same best and worst) exist but are rarely used; calling average case "big O" is sloppy but understandable [235].
- Four-step recipe to derive an order: pick n, count steps per line (loops multiply), drop lower orders, drop coefficients; readingList example [237-238].
- Why coefficients are dropped: a 3n^2 function overtakes a 1000n one at n=334 and stays slower; graph of orders [238-239].
- Worked examples: two sequential loops are still O(n); a loop with a fixed count is O(1); nested loops over the data are O(n^2); binary search is O(log n) unless it sorts first, then O(n log n) [239-242].
- Table of orders of built-in operations: list append/index O(1), insert/remove/in O(n), sort O(n log n); dict/set membership O(1) via hashing; converting a list to a set costs O(n) so it does not help a single lookup [242-243].
- Rules of thumb for reading an order at a glance (no data access = O(1), one loop = O(n), nested = O(n^2), halving = log n, sorting = at least n log n) [243].
- AGAINST over-applying big O: a function that sleeps an hour is O(1); big O is not a substitute for profiling; Rob Pike's rule that n is usually small; in mundane programs a profiler tells more than analysis [244].
- Summary names timeit and cProfile and Amdahl's law (covered earlier in the chapter, pages not yet read) [244-245].

## Chapter 14 -- Practice Projects [247-272]

- Two small text games (Tower of Hanoi, Four-in-a-Row) written to the book's own rules: Black-formatted, names per ch. 4, idioms per ch. 6, comments and docstrings per ch. 11, deliberately without classes; the point is explaining WHY the code is written as it is, not how it works [247-248].
- Advice: retype and run a project, then reimplement it from scratch to feel the design trade-offs [248].
- Walkthrough points, Tower of Hanoi: module docstring that help() shows [252-253]; one import per line so version-control diffs are cleaner [253]; constants grouped at the top in upper snake case [253]; no type hints because every type is inferable and a checker would infer them anyway [253]; a long comment documenting the central data structure (a dict of lists used as stacks) with valid and invalid examples [254]; descriptive function names make main() read as an overview [254].
- Prefer `x in (a, b)` to two equality tests joined by or [255]; normalise user input (upper, strip) and always show a prompt symbol [255].
- A function returns one data type: the move function exits itself on QUIT rather than returning a string sometimes and a tuple otherwise [256].
- Hard-coding the six legal tower pairs is more readable than a clever length-and-membership test; magic values are acceptable when the thing they describe (three poles) will not change [256].
- Variables introduced only to give a readable name to an index are worthwhile [256]; order conditions so later ones cannot raise (empty-tower checks before indexing); always handle invalid input [257].
- Functions also exist to organise code into units, not only to remove duplication: getPlayerMove is called once and still deserves to be a function [257].
- format() with positional placeholders preferred over an f-string when the same value appears several times [258]; splitting display into two functions narrows where a display bug can live [258-259]; the `if __name__ == '__main__'` idiom keeps the module importable for tests [259].
- Four-in-a-Row: string constants for X and O so a typo becomes a NameError instead of a silent bug [264]; a comment telling future editors which constants must change together, plus an assert guarding one such coupling [264-265].
- Twice chooses a literal (label tuple, multiline board template) over code that generates it, because the literal is more readable and the size will not change -- acknowledged as a code smell accepted on purpose [265].
- sys.exit() instead of break to make program termination explicit [266]; an elif with a spelled-out condition instead of a bare else, citing explicit over implicit [267]; the dictionary-swap one-liner rejected as less readable than if/elif [267].
- tile1..tile4 variables kept despite the numeric-suffix smell because the count is fixed at four; a smell is a prompt to look again, not an order to change [270].
- (a) Most important in the chapter and stated as the closing thought: readability is a judgement, not a score against a rule list; readability beats a zero-code-smells policy [271-272].
- (d) Introductory for an experienced developer: the code walkthroughs themselves; the value is in the explicit reasoning for each small decision.

## Chapter 15 -- Object-Oriented Programming and Classes [275-292]

- OOP is optional in Python; for small programs classes add bureaucracy rather than organisation; the author points at Jack Diederich's "Stop Writing Classes" talk [275]. (b)/(c) contrarian versus Java-style habits: do not reach for a class by default.
- A class is a form template, objects are filled-in forms; what goes into a class depends on what the program needs, not on the real-world thing (a Car class for a dealership differs from one for a racing game) [276-278].
- WizCoin example class with __init__, value(), weightInGrams() [279-280]; naming: module lowercase, class CapWords [279]; a method that never uses self should be a plain function [281]; __init__ never returns a value [282].
- Privacy exists only by convention (leading underscore); BankAccount ledger example shows how writing to _balance from outside produces inconsistent state, and why respecting the convention keeps the cause of any bug inside the class [282-284].
- (b) Python needs no getter/setter methods; properties cover that (ch. 17) [284].
- type() and __qualname__ for a readable type name in logs [284-285].
- Tic-tac-toe written twice, without and with a class: the signal to introduce a class is several functions all taking the same data structure as their first parameter [285-290].
- Designing classes for the real world is hard: name fields, age versus birthdate, the "falsehoods programmers believe" lists [290-291].
- (d) Introductory: the whole chapter is a from-scratch OOP tutorial; an experienced developer already knows it, except for the explicit "when a class is warranted" rule.

## Chapter 16 -- Object-Oriented Programming and Inheritance [293-313]

- Inheritance is a code-reuse device; the "inheritance is evil" camp is not entirely wrong -- it is easy to overuse, useful in small doses [293].
- Mechanics: subclassing, is-a relationship, overriding, super() -- not every override needs super() [294-299].
- (a) Favour composition over inheritance: use is-a inheritance only when the child truly is a kind of the parent; WizardCustomer should hold a WizCoin, not subclass it, because inherited method names would lie [299-301].
- Downside of inheritance: every parent change reaches every child; Vehicle/LunarRover changeSparkPlug example; the Pythonic patch of assigning None to an inherited method so a wrong call fails fast with TypeError [301-303].
- isinstance() preferred over type() comparison for checks because it honours subclasses; issubclass() [303-304].
- Class methods: the one common use is alternative constructors (fromFile), written with cls so subclasses work; a class method that never uses cls should be a function [304-306].
- (c) Class attributes, static methods: rarely needed; a module-level variable or function is simpler; static methods exist to imitate other languages and add little [306-307]. Only frameworks with deep class families need them; Phillip Eby's "Python Is Not Java" cited [307].
- OOP buzzwords (encapsulation, polymorphism) -- knowing the terms matters less than people claim [307-308].
- When NOT to inherit (quotable rules): a class whose methods never use self or cls becomes functions; a parent with a single child and no parent instances is merged; more than three or four levels means inheritance is being misused [308-309]. Spolsky's "architecture astronauts" cited.
- Multiple inheritance, mixins, MRO with its two rules (child before parent, left to right), super() means "next in the MRO", not "the parent"; favour single inheritance, mixins, or none [309-312].
- (d) Introductory apart from the rules above.

## Chapter 17 -- Pythonic OOP: Properties and Dunder Methods [315-338]

- Properties replace getters/setters: four-step recipe (rename to _x, @property getter, .setter, .deleter); accessor code must touch the backing field, never the property, or it recurses to RecursionError [316-319].
- Setters validate: the WizCoin setters reject non-int and negative values with a module-specific exception; a module defines its own Exception subclass with a docstring so that a ValueError or TypeError escaping the module signals a bug in the module rather than misuse; error messages name the offending type via __class__.__qualname__ [319-320].
- Read-only properties by omitting the setter; crashing on assignment is preferable to silently allowing a change that bites later; read-only property is not a constant [320-321].
- When to use a property versus a method: get/set-named methods are a signal; keep a method when the operation is slow, has side effects, or needs arguments; the Pythonic advantage is starting with plain attributes and converting later without breaking callers [322].
- (a) Strongly recommended for every class: implement __repr__ and __str__; repr via __class__.__qualname__ so subclasses and renames stay correct; use angle brackets when a repr cannot be real code [323-325].
- Security note: repr strings land in logs, so keep passwords and personal data out of them [325].
- Numeric dunder methods: type-check `other` and return NotImplemented (not raise) for unsupported types; raise the module exception for invalid values; never mutate self in a non-in-place operator, return a new object [325-328]. Method names like multiplyBy or convertToInt signal a missing dunder method [328].
- Reflected dunders; a commutative operation delegates to the forward one [328-330]. In-place dunders modify self and return self for mutable objects; without them Python falls back to the forward operator and rebinds, which can surprise [330-332].
- Comparison dunders through one helper taking an operator-module function (a higher-order function) to avoid six copies; only three pairs reflect each other; sort() works once they exist [332-337]. Methods named equals() or isGreaterThan() are a smell [337].
- Further reading recommended: Fluent Python, Effective Python, Hettinger's talks [337-338].
- (d) Mostly introductory for an experienced developer, except the NotImplemented rule, the module-exception convention and the repr/str recommendation.

## Cross-cutting: what the author treats as most important

- Readability over everything, including over cleverness, over performance tricks, and over mechanical rule-following; a code smell is a prompt, not a verdict [69, 85, 226-227, 271-272].
- Tooling as a baseline: a linter in the editor (ch. 1), a formatter (ch. 3), a type checker (ch. 11), version control (ch. 12) -- these are the "professional" layer the book exists to supply.
- Functions: one return type, raise instead of returning None or error codes, pure where possible, as short as reasonable and no shorter (ch. 10).
- Comments explain why; documentation is not optional (ch. 11); __repr__/__str__ on every class (ch. 17).
- Classes only when several functions share the same first parameter; composition over inheritance; no getters/setters, no static methods, no deep hierarchies (ch. 15-17).

## Cross-cutting: unusual or contrarian positions

- camelCase for functions and variables, against PEP 8, on the grounds that consistency beats the choice [60-61].
- A single triple-quoted string for multiline comments rather than several # lines [182].
- Always copy.deepcopy(); copy.copy() instead of the [:] slice idiom [97-98, 142].
- Hint variable types even when the checker would infer them [191].
- Line length 120, not 88 or 79 [55].
- str.format() dismissed, f-strings everywhere [96-97]; map()/filter() called outdated [176].
- git commit -am and committing straight after every add/mv/rm, skipping the staging area as a concept [206].
- Rejects five common rules outright: single exit point, one try per function, no flag arguments, no globals, no comments [80-84].
- Magic values tolerated when the quantity is structurally fixed (three poles, four tiles) [256, 265, 270].

## Cross-cutting: what the author argues against

- Classes written out of habit, Java-style getters/setters, static methods, class attributes, inheritance deeper than three or four levels, multiple inheritance beyond mixins [77, 284, 306-312].
- Very short functions as a doctrine ("three or four lines") and the function explosion it causes [163-165].
- Clever one-liners: XOR swap, nested comprehensions, and/or ternaries, bool-as-int tricks, dict-swap one-liners [77-79, 101-102, 158-159, 226-227, 267].
- Returning None or error codes for failures; empty except blocks; error messages naming internal functions [79-80, 177-179].
- Comments that restate the code, jokes and venting in code, end-of-line comments in general [51, 64-65, 184-186].
- Premature optimisation and applying big O where a profiler is the right tool [226, 244].
- Print debugging instead of a debugger or logging [75-76].

## Introductory chapters an experienced developer already knows

- Fully introductory: 1 (errors and asking for help), 2 (command line), 7 (jargon), 9 (oddities), 12 (Git tutorial), 15 and 16 (OOP mechanics, except the when-to-use rules), 13 first half (timeit/cProfile/big O primer).
- Mostly known, with author-specific positions worth keeping: 3 (Black and the reasons), 6 (idioms), 8 (gotchas), 11 (type hint mechanics), 17 (dunder mechanics).
- Substantive for the write-up: 4 (names), 5 (smells and myths), 10 (functions), 14 (walkthrough of judgement calls), the when-to rules in 15-17.

## Advice a linter or formatter can enforce mechanically

- Whitespace, indentation, blank lines between defs, line length, one statement per line, no one-line if bodies, trailing comma in single-item tuples -- Black (ch. 3), ruff/flake8 E-codes.
- Import grouping and one import per line -- isort, ruff I-rules (Black does not touch imports) [53].
- Spaces not tabs -- Black; TabError at parse time anyway [47].
- Comment spacing: one space after #, two before inline -- pycodestyle E261/E262.
- Shadowing built-ins as names -- flake8-builtins (A001-A003) [65-66, 162].
- Mutable default arguments -- ruff B006 (flake8-bugbear) [143-144].
- Empty except / bare except / except with pass -- ruff E722, S110, BLE001 [79-80].
- == None instead of is None; is True / is False -- ruff E711/E712 [94-95].
- range(len()) instead of enumerate -- ruff C416/SIM113-style rules [92-93].
- open() without with -- ruff SIM115 [93-94].
- % and format() where an f-string would do -- ruff UP031/UP032 [96-97].
- Chained != comparisons -- no standard rule; a trivial AST check [149-150].
- Assigning a lambda to a name -- ruff E731 [175].
- Unused imports/variables, undefined names -- Pyflakes/ruff F-codes (the ch. 1 linter advice).
- Nested comprehensions / several for clauses -- ruff C4-family partially; depth is checkable by AST [77-79].
- Function length and parameter count thresholds (30/200 lines, 3-5 params) -- pylint R0913/R0915, ruff PLR0913/PLR0915 with configured limits [165].
- Missing docstrings on public module/class/function -- ruff D100-D103 (pydocstyle); triple double quotes -- D300 [188-190].
- Type hints present on signatures; Union/Optional/Any usage -- pyright strict / mypy --strict; Any count via ruff ANN401 [190-195].
- Methods that never use self -- pylint R0201 (no-self-use) [281].
- Class with no methods but __init__, or only static methods -- pylint R0903 (too-few-public-methods) approximates [77].
- Numeric-suffix variable names, Hungarian prefixes, single-letter names outside i/j/k/x/y -- regex over identifiers; pylint invalid-name with a pattern [61-64].
- Commented-out code -- ruff ERA001 (eradicate) [74-75].
- print() calls left in -- ruff T201 [75-76].
- Codetags other than TODO -- ruff FIX/TD rules [187].
- Magic numbers -- ruff PLR2004 [71-73].
- String building by += in a loop -- pylint consider-using-join / ruff PERF401-ish [144-146].
- Mutating a list while iterating over it -- ruff B909 (flake8-bugbear) [134-140].
- Missing __repr__/__str__ on a class -- no standard rule; simple AST check [323-325].
- Returning NotImplemented vs raising in dunder arithmetic -- ruff PLE0307-style partial; custom check [325-328].

## Advice that needs judgement and could be a yes/no check on a diff

- Does every changed function return a single type, with None only when it has no meaningful result? [177-178]
- Does any new failure path return a sentinel or error code where it could raise? [178-179]
- Do new comments say why rather than restate the code? [184-185]
- Is each new name pronounceable, specific, searchable, and free of jokes and dropped letters? [61-66]
- Does a new magic number or string get a named constant, unless the quantity is structurally fixed and the text says so? [71-73, 256]
- Is a new class justified by several functions sharing the same data, or is it a module in disguise? [77, 285-290]
- Does a new subclass pass the is-a test, or should it hold the other object instead? [299-301]
- Is a new flag parameter selecting between two unrelated behaviours (split it) or tuning one (fine)? [82]
- Is a new global variable a constant, or mutable state that could be a parameter? [82-83]
- Has copy-pasted code reached its third or fourth copy? [70-71]
- Does a function that grew past about thirty lines still do one named job? [165]
- Does a new parameter push a function past five or six? [165]
- Is a new *args/**kwargs signature there because callers will pass separate values, or hiding a list parameter? [168-169]
- Does the function touch globals, files, clock, randomness or mutate its arguments when it did not need to? [172-174]
- Does the docstring have a summary line, and does it state parameters, return and side effects for programmers? [189-190]
- Does a type: ignore or Any appear where a rewrite would remove it? [193-195]
- Does the commit contain one finished piece of functionality and a message that says what changed? [210-214]
- Does a new setter validate, and does a read-only attribute stay a property without a setter? [319-321]
- Does a new dunder method return a new object rather than mutating self, and NotImplemented for foreign types? [325-328]
- Is a literal table kept as a literal because it is more readable than code that generates it, and is that said? [265]
- Does a comment or assert tell a future editor which constants must change together? [264-265]
- Was the change measured (timeit/cProfile) before anything was optimised? [226-229]

## Advice that is beginner-level or tooling-tutorial rather than a check

1, 2, 7, 8 (most of it), 9, 12, 13 (first half), 15, 16
