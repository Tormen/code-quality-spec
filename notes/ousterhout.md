# Ousterhout, A Philosophy of Software Design (2nd ed., 2021) -- working notes

Source: the book itself, 2nd edition, 191 PDF pages (read in full).
Page numbers in brackets are the BOOK's printed page numbers (PDF page = printed page + 12; the front matter is roman-numbered).
Everything below is my own restatement; nothing is copied from the book.

Markers used:
- **[KEY]** -- an idea the author himself treats as central (repeated, bolded, or in his closing summary).
- **[CONTRARIAN]** -- advice that runs against common practice or common teaching.
- **[AGAINST]** -- something the author argues against by name (a book, a school, a practice).

---

## Preface [vii-x]

- The author's diagnosis: problem decomposition is the central skill of programming, yet nobody teaches it; the field has not moved much past Parnas's 1971 modules paper. [vii]
- He believes design is teachable and built the book out of a Stanford course (CS 190) in which students write a sizeable system and get repeated design reviews -- the book is a distillation of what those reviews kept finding. [viii]
- Framing: the whole book is an opinion piece with one goal, less complexity; a reader who finds a principle does not reduce complexity in their case is told to drop it. [ix]
- The terms "deep" and "shallow" came from a colleague and replaced the earlier "thick"/"thin". [ix]

## Chapter 1 -- Introduction (It's All About Complexity) [1-4]

- Software has no physical limits; the limit is how much the people working on it can hold in their heads. Complexity accumulates as a system grows and is the real enemy. [1]
- Two levers against it: make code simpler and more obvious, or hide complexity behind modules so one person only faces a slice of it. [2]
- Design is continuous: waterfall fails for software because nobody can foresee a large system; incremental development is right, but that means redesign never stops and a developer must always be looking for design improvements. [2-3]
- **[KEY]** The book's method is red flags: learn to recognise the symptom in code, then try alternatives until the symptom disappears. Reading other people's code (reviews) is the best place to practise. [3-4]
- Every principle has a "taking it too far" limit; several chapters carry a section with that title. [4]

## Chapter 2 -- The Nature of Complexity [5-11]

- **[KEY]** Working definition: complexity is whatever in a system's structure makes it hard to understand or change. Not size, not feature count -- difficulty of work. [5-6]
- Complexity is weighted by how often a part is touched; a horrible corner nobody visits costs little. Isolation is almost as good as elimination. [6]
- Complexity is judged by readers, not the writer: if others find it complicated, it is. [6]
- Three symptoms: a small change touching many places (change amplification), a developer having to know a lot to make a change (cognitive load), and not knowing what must be changed or looked at (unknown unknowns). The last is the worst. Example: the web-site banner colour, first duplicated per page, then centralised, then with a derived emphasis colour that nobody knows depends on it. [7-9]
- **[CONTRARIAN]** Fewer lines is not simpler; a longer design that lowers cognitive load is the simpler one. [7-8]
- The goal that opposes the symptoms is an "obvious" system: a quick first guess about how to change it is right. [9]
- Two root causes: dependencies (code that cannot be understood or changed alone) and obscurity (important information not visible -- a vague name, missing units, an unseen coupling). Heavy documentation needs are themselves a smell of a design problem. [9-10]
- **[KEY]** Complexity is incremental: no single kludge hurts, thousands do, so the only defence is zero tolerance. [11]

## Chapter 3 -- Working Code Isn't Enough (Strategic vs. Tactical Programming) [13-18]

- Tactical programming optimises for the current feature or fix and accepts "a little" complexity each time; that is exactly how systems rot. The "tactical tornado" is the prolific colleague management loves and everyone else cleans up after. [13-14]
- **[KEY]** Strategic programming: the primary deliverable is a good design that also happens to work, not working code. [14-15]
- Investment mindset: spend roughly a tenth to a fifth of development time on design, both proactively (try alternatives, document) and reactively (fix a design flaw when you meet it rather than patching around it). The payoff curve crosses within months, not years. The author admits he has no hard data for the exact figures. [15-17]
- Technical debt framed as borrowing that is never fully repaid. [16]
- Startups: the "we will clean up when rich" rationalisation; Facebook ("move fast and break things") versus Google and VMware as counterexamples; good engineers are attracted by clean code bases. [17-18]
- The slippery slope: deferring design work "until after this crunch" becomes permanent. [18]

## Chapter 4 -- Modules Should Be Deep [19-28]

- Modular design: split into parts (classes, subsystems, services, even single methods) so a developer needs the implementation of only one plus the interfaces of the others. Dependencies cannot be removed, only minimised and made obvious. [19-20]
- An interface has a formal part (signatures the compiler checks) and an informal part (behaviour, ordering constraints, side effects) that only prose can express; the informal part is usually larger. [20-21]
- An abstraction is a simplified view that omits unimportant detail; it fails by including the unimportant (more load) or by omitting the important (a "false abstraction" -- example: a file system that hid when data reaches disk). [21-22]
- **[KEY]** Depth: picture a module as a rectangle, functionality as area, interface as the top edge; the best modules have a lot of area under a short edge. Examples: the five Unix file-I/O calls hiding a huge implementation; a garbage collector, which removes an interface entirely. [23-25]
- Shallow module red flag: interface about as complex as what it hides. Examples: a linked-list class; a one-line student method wrapping a map insert, whose documentation would be longer than its body. [25-26]
- **[CONTRARIAN] [AGAINST]** "Classitis": the taught doctrine that classes and methods should be small (split anything over N lines) breeds many shallow pieces whose interfaces add up to system-level complexity. Java's file reading needing three stacked stream objects, with buffering opt-in, is the showcase. [26-27]
- **[KEY]** Design the interface so the common case is trivial; rare needs get a separate mechanism nobody else has to see. [27]

## Chapter 5 -- Information Hiding (and Leakage) [29-38]

- **[KEY]** Information hiding (credited to Parnas): each module owns a few design decisions that do not show in its interface; this both shrinks the interface and localises future change. [29-30]
- Making fields private is not hiding if getters and setters expose them anyway. Partial hiding (a detail needed only by a few callers, reachable through a separate method) still counts. [30]
- Leakage red flag: one decision known to several modules, through the interface or -- worse, because invisible -- through a shared assumption like a file format. Fix by merging the affected classes or by extracting a class that owns just that knowledge, provided its interface really abstracts it away. [30-31]
- Temporal decomposition red flag: structuring code by the order things happen (read, modify, write as three classes) rather than by knowledge; the read and write steps both know the format. Decompose by what must be known, not by when. [31-32]
- HTTP server project examples: students split reading a request from parsing it, but one cannot find the end of a request without parsing headers, so both classes knew the format -- merging them made a deeper class; returning the internal parameter map exposed the representation and made callers do the lookup, versus typed per-name accessors; forcing callers to supply the protocol version or date in a response instead of defaulting them. [33-36]
- **[KEY]** Making a class somewhat larger often improves hiding: it gathers everything about one capability and lets one call replace several ordered ones. [34]
- Overexposure red flag: using a common feature forces learning rare ones. Good defaults are partial information hiding; a module should do the right thing unasked. [36]
- Hiding applies inside a class too: private methods that each own one thing, instance variables touched in as few places as possible. [37]
- Limit: information genuinely needed outside (e.g. a tuning parameter users must set) must be exposed; the aim is to minimise what is needed outside, e.g. by auto-tuning instead. [37]

## Chapter 6 -- General-Purpose Modules are Deeper [39-49]

- **[KEY]** The author's most changed opinion: over-specialisation may be the single biggest source of complexity; general interfaces are simpler and deeper, and this held in student projects even when the class was used in only one way. [39-40]
- **[CONTRARIAN]** Against the incremental "build only what you need now and generalise later" habit: build "somewhat general-purpose" -- functionality for today's needs, interface not tied to them. [40]
- Text-editor storage example: special methods per UI feature (backspace, delete, delete-selection) tied the text class to the UI and multiplied shallow methods; two general primitives (insert text at position, delete a range) plus a position-walking helper do everything, with slightly more caller code that is more obvious, and the same class serves a search-and-replace tool. [41-43]
- The specialised backspace method was a false abstraction: UI developers needed to know exactly which characters go, so hiding it behind a name only caused obscurity. [43-44]
- Three self-check questions: what is the smallest interface covering all current uses (fewer methods without more arguments); is a method used in only one place (then it is probably too specific); is the API easy for today's need (if lots of glue is needed, it is too general -- e.g. single-character insert/delete). [44]
- Specialisation goes up (application-level features live in the top layers) or down (device drivers implement a general block interface below the OS core). [45]
- Undo example: a general history of undoable actions with fences for grouping, with text-, selection- and cursor-specific actions implemented elsewhere; three cleanly separated concerns. [45-48]
- Special cases in method bodies are the same disease: design the normal case so the edge case needs no branch -- e.g. a selection that always exists but may be empty, so copy/delete need no "no selection" check. [48-49]

## Chapter 7 -- Different Layer, Different Abstraction [51-60]

- Each layer should present a different abstraction (file system: byte array over block cache over drivers; TCP: reliable stream over lossy packets); two adjacent layers with the same abstraction signal a bad split. [51]
- Pass-through method red flag: a method whose body is a call with the same signature; 13 of 15 methods in a student's document class were such. They add interface without function and couple the signatures. Fixes: let callers reach the lower class directly, redistribute, or merge. [52-53]
- Same signature is fine when each method adds function: a dispatcher choosing among handlers; several implementations of one interface. [53-54]
- **[CONTRARIAN]** Decorators (wrappers) are usually shallow boilerplate; before writing one ask whether the feature belongs in the wrapped class, in the use case, in an existing decorator, or stands alone. Java's buffered stream again. A wrapper is justified mainly to adapt an unmodifiable foreign interface. [55-56]
- Interface should differ from implementation: a text class stored as lines but exposing character ranges is deep precisely because of that difference; exposing getLine/putLine made every caller split and join lines. [56]
- Pass-through variables: a certificate threaded through every call level. Options: a shared object, a global (kills multiple instances), or -- the author's usual answer -- a context object holding all per-instance global state, passed in constructors and kept as a field. He admits contexts have most of the downsides of globals and that he has nothing better. [57-59]
- Closing principle: any piece of design infrastructure must remove more complexity than it adds, or it should not exist. [59-60]

## Chapter 8 -- Pull Complexity Downwards [61-64]

- **[KEY]** When some complexity is unavoidable, the module should absorb it rather than push it to its users: a simple interface matters more than a simple implementation, because a module has more users than implementers. [61]
- Throwing an exception or adding a config knob is the developer's easy way out that multiplies the work across every caller or every administrator. [61]
- Text class: a character-oriented interface over line storage pulls the line splitting down into one place. [62]
- **[CONTRARIAN]** Configuration parameters are mostly a way of exporting unsolved problems; often the system can compute a better value than any user (a retry interval derived from measured response times, which also adapts). Before adding one, ask whether users can really pick a better value; if a parameter stays, give it a sensible default. [62-63]
- Limit: pull complexity down only when it is related to the class's purpose, simplifies things elsewhere, and simplifies the interface; putting backspace into the text class was pulling the wrong thing down. [63-64]

## Chapter 9 -- Better Together Or Better Apart? [65-76]

- Splitting is not free: more parts to track, more interfaces, management code, physical separation of related code, and duplication. Combine when pieces share information, are used together (both ways), belong to one conceptual category, or cannot be understood apart. [65-66]
- HTTP read+parse merged because they shared knowledge and the merged interface was simpler, with buffering-by-default as the second example of a simpler combined interface. [66-67]
- Duplication red flag: extract a method when the snippet is long and the signature stays simple; otherwise restructure so the snippet runs once -- the error-cleanup example where a goto to a single logging label replaced four copies of a LOG call (goto defended for escaping nested code). [67-70]
- Special-general mixture red flag: a general mechanism carrying special-case code for one client. [68, 71]
- Cursor and selection kept apart: a merged object was harder to use and implement; a small Position type served both. [70-72]
- A separate logging class with one-line methods, each called from exactly one place, was pure overhead: inline the log statements. [72-73]
- **[CONTRARIAN]** Method length by itself is not a reason to split; split only when it yields a cleaner abstraction -- best by extracting a self-contained subtask, rarely by splitting into two caller-visible halves, never into pieces that must be read together (conjoined methods red flag). Methods of hundreds of lines with a simple interface are fine. [73-75]
- **[AGAINST]** Robert Martin's Clean Code rule that functions should be a handful of lines: beyond a few dozen lines further shrinking buys little and costs depth; depth beats length. [76]

## Chapter 10 -- Define Errors Out Of Existence [77-90]

- Exception paths are intrinsically harder (interrupted flow, inconsistent state to unwind, secondary failures), rarely exercised, hard to test, verbose in the language (the Java try/catch pile for reading serialized tweets), and a cited study found most catastrophic distributed-system failures came from bad error handling. [77-80]
- **[CONTRARIAN]** Over-detection is a mistake: programmers are taught more checks are better, but every thrown exception is interface the caller must handle, so classes with many exceptions are shallower. The author's own Tcl `unset` erroring on a missing variable is his confessed worst design decision. [80-81]
- **[KEY]** Reduce the number of places exceptions must be handled; the best way is to define the semantics so the "error" is normal behaviour: unset as "ensure the variable does not exist"; Unix delete-while-open (file disappears from the directory, data lives until closed) versus Windows refusing; a substring that clips indices instead of throwing (Python slices). [81-83]
- Counter to "errors catch bugs": the error-ful API adds caller code and thus bugs; simpler software is the best bug reducer. [83]
- Mask exceptions at a low level when higher levels cannot act usefully: TCP retransmission; NFS hanging until the server returns, defended against the common complaint that it should fail. [83-84]
- Aggregate exceptions: one handler high up instead of one per call; the web server catching missing-parameter exceptions at the dispatcher, extended into a general "abort this request" exception family; RAMCloud deliberately promoting rare small errors (corrupt object) into a server crash to reuse one recovery mechanism. Masking belongs low, aggregation high. [84-88]
- Just crash for errors not worth handling (out of memory via a checking allocator wrapper, I/O errors in ordinary programs, internal inconsistencies) -- unless the application's whole value is surviving them. [88-89]
- Limit: a student network module that swallowed every error made robust applications impossible; hide what callers do not need, expose what they do. [89-90]

## Chapter 11 -- Design it Twice [91-93]

- **[KEY]** For any major decision sketch at least two radically different designs before choosing; even when one seems obviously right, the second exposes the first's weaknesses. Text class: line-based versus character-based versus range-based interfaces. [91-92]
- Compare on ease of use for callers first, then simplicity, generality, implementation efficiency; often the winner combines features of the candidates, or the comparison reveals a third option (the range API). [91-92]
- Apply at every level (interface, then implementation, then system structure); the cost is an hour or two per class against days of implementation. [92-93]
- Observation about smart people: used to being right first time, they resist this and underperform on hard problems; needing a second design means the problem is hard, not that you are not smart. [93]

## Chapter 12 -- Why Write Comments? The Four Excuses [95-100]

- **[KEY]** Comments are a design matter, not hygiene: without them the informal half of every interface is invisible, so abstraction is impossible. If callers must read a method's body to use it, there is no abstraction. [95-97]
- The four excuses answered: (1) code is self-documenting -- no, signatures cannot carry rationale, units, conditions, or high-level behaviour, and reading bodies to learn an API does not scale; (2) no time -- comments are an investment and typing is a small share of development; (3) they rot -- not much if kept near the code and non-duplicated (Chapter 16), and reviews catch drift; (4) all comments I have seen are useless -- the one excuse with merit; the fix is learning to write good ones. [96-98]
- Comments capture what was in the designer's head and cannot be encoded; they attack cognitive load and unknown unknowns directly. [98-99]
- **[AGAINST]** Clean Code's view of comments as failures to express oneself in code: the author says comments carry information code cannot, that replacing a comment with a method whose name is a sentence is cryptic and repeats the documentation at every call, and that the attitude makes programmers avoid writing them. [99-100]

## Chapter 13 -- Comments Should Describe Things that Aren't Obvious from the Code [101-120]

- **[KEY]** Guiding rule: a comment adds what the reader cannot get from the code next to it; a reader should understand a module from its declarations and comments alone. [101-102]
- Pick a convention (Javadoc, Doxygen, godoc) and comment every class, every field and every method interface by default; implementation comments are optional, cross-module comments rare but critical. [102-103]
- Comment-repeats-code red flag: one comment per line at the code's own level, or a comment made of the identifier's words; test: could someone who never saw the code write this comment from the code alone? Use different words from the name. Example: padding constant documented with units and which sides. [103-105]
- Comments live at a different level from the code: lower for precision (units, inclusive/exclusive bounds, null meaning, ownership of a resource, invariants) -- vague "current offset" versus a precise definition; describe what a variable represents (nouns), not how it is manipulated. [105-107]
- Higher for intuition: a one-line statement of what a block is trying to do beats a restatement of its conditions; "how we got here" comments explaining why code runs are valuable. The RPC key-hash examples. [107-109]
- Interface comments must be separate from implementation comments; if the interface comment has to describe the implementation, the thing is shallow. Class comment: overall abstraction, what an instance represents, limits (single-threaded). Method comment: behaviour as callers see it, every argument and result precisely, side effects, exceptions, preconditions. The Buffer copy example. [109-111]
- The IndexLookup worked example: a first-draft class comment full of RPC names, private constants and advice to include a header, replaced by a short statement of what an instance is and how its methods are used; an isReady comment rewritten to say what "ready" means and that it must be called for progress. Red flag: implementation detail contaminating interface docs. [112-116]
- Implementation comments: what and why, not how; a line before each major block or loop; document the reason for non-obvious fixes (point at the bug tracker rather than retelling). [116-117]
- Cross-module decisions: put the note where the next change must go (the RAMCloud Status enum listing every place a new status touches); failing an obvious spot, a central designNotes file with short pointers from code, accepting it is far from the code. [117-119]
- Obviousness is judged by a first-time reader; if a reviewer says it is not obvious, it is not -- do not argue, fix the code or the comment. [119-120]

## Chapter 14 -- Choosing Names [121-129]

- Names are documentation and an instance of incremental complexity: one mediocre name is harmless, thousands are not. [121]
- The Sprite file-system bug: one variable `block` used for both disk and file block numbers took six months to find because everyone reading the name assumed the wrong kind; distinct names (or distinct types) would have prevented it. [121-122]
- A name should paint a picture in isolation: precise, unambiguous, two or three words. Vague-name red flag: `getCount` (of what?), `x`/`y` for character positions, `blinkStatus` for a visibility boolean (booleans should read as predicates), `result` in a void method, Linux `socket` versus `sock`. [122-125]
- Too specific is also wrong (`selection` as the argument of a general range delete); `i`/`j` are fine when the loop is short. [125]
- Hard-to-pick-name red flag: trouble naming something usually means it has no clean definition -- maybe it is two things. [125-126]
- Consistency: one name per concept, never reused for anything else, and a scope narrow enough that all instances behave alike; distinguish with prefixes (src/dst); same loop-variable conventions. [126]
- **[CONTRARIAN]** Drop words that add nothing (`fileObject`), drop type prefixes (the author used to include type info and now disowns Hungarian notation), do not repeat the class name in a field. [127]
- **[AGAINST]** The Go naming culture (very short names, same letter for several meanings): the author finds the longer version no harder to read and warns short reused names breed the `block` bug; readability is decided by readers; he agrees with the Go guidance that distance between declaration and use justifies longer names. [127-129]

## Chapter 15 -- Write The Comments First [131-135]

- Delayed comments are bad comments: once the code is "done" the writer is mentally gone, writes the minimum, and merely restates the code; design rationale has faded. [131-132]
- **[CONTRARIAN]** The author's workflow: class interface comment, then method signatures with interface comments and empty bodies, iterate, then field declarations with comments, bodies last; no comment backlog ever exists. [132]
- **[KEY]** Comments as design tool and complexity canary: a method or variable that needs a long comment to be fully described has a bad abstraction (hard-to-describe red flag); comparing interface comment to implementation measures depth. Only complete, clear comments are a valid gauge. [133-134]
- Early comments are the enjoyable part of design; the time argument against them fails because comments are at most a few percent of effort and stable abstractions reduce later rework. [134-135]

## Chapter 16 -- Modifying Existing Code [137-142]

- Most design happens during evolution, so the strategic mindset must survive maintenance; "smallest change that works" is tactical. [137-138]
- **[KEY]** After a change, the system should look as if it had been designed with that change in mind from the start; if you are not improving the design you are degrading it. Compromises under deadline are allowed only after asking whether a nearly-as-clean quick path exists, and with cleanup scheduled. [138]
- Keep comments next to the code they describe (method comment in the .c file next to the body, not the header); spread implementation comments to the narrowest enclosing scope; an overview comment at the top may list phases. The further a comment is from code, the more abstract it should be. [139-140]
- **[CONTRARIAN]** Commit messages are the wrong home for design knowledge nobody will look for later; information future developers need goes in the code, the log may carry a copy. [140]
- Document each decision once; elsewhere point to the master comment (a dangling pointer at least announces itself, a stale copy does not). Do not re-explain a callee at the call site; reference external documentation (RFCs, manuals) rather than restating it. [140-141]
- Scan the whole diff before committing to update comments and catch leftover debug code and TODOs. Higher-level comments survive code changes better. [142]

## Chapter 17 -- Consistency [143-146]

- Consistency means similar things look alike and different things look different; it lets readers reuse knowledge and makes pattern-based assumptions safe. Applies to names, style, interfaces with multiple implementations, design patterns, invariants. [143-144]
- Ensure it by writing the conventions down where people will see them, enforcing them with tools in the commit path (the line-ending checker story), nit-picky reviews, and above all by following whatever the surrounding code does. [144-145]
- **[CONTRARIAN]** A better idea is not a sufficient reason to break an existing convention; change one only with new information and when the whole old usage will be converted. [145-146]
- Limit: forcing dissimilar things into one shape (same name for different concepts, a pattern that does not fit) destroys the very trust consistency creates. [146]

## Chapter 18 -- Code Should be Obvious [147-152]

- Obvious code: a quick read gives a correct first guess about behaviour; non-obvious code (red flag) is judged by readers in review, not by the author. [147, 150]
- Helpers: good names, consistency, whitespace that reveals structure (parameter docs separated by blank lines, blank lines between blocks each headed by a comment, spaces inside expressions), and comments where the code cannot be made obvious. [147-149]
- Things that obscure: event-driven dispatch (document when and by whom a handler is called), generic containers like Pair returning two values whose meaning is lost (define a small purpose-named struct), declaring a variable as a supertype of what is allocated, code that defies reader expectations (a main that keeps running in other threads without saying so). [150-152]
- **[KEY]** Design for ease of reading, not ease of writing. [151]
- Obviousness is an information problem: reduce what a reader must know, lean on what they already know (conventions), present the rest in the code. [152]

## Chapter 19 -- Software Trends [153-159]

- Interface inheritance is good (an interface with many implementations is deep); implementation inheritance creates parent-child leakage and often demands knowledge of the whole hierarchy -- prefer composition, and if inheriting, keep parent state private to the parent. OOP mechanisms do not guarantee good design. [153-155]
- **[AGAINST]** Agile's tendency toward feature-sized increments and deferred generality encourages tactical programming; the author accepts incrementalism but insists the unit of increment should be an abstraction, designed whole once needed, not a feature. [155-156]
- Unit tests are endorsed strongly because they make refactoring safe (Tcl's bytecode compiler rewrite shipped with one bug thanks to its suite). [156-157]
- **[AGAINST] [CONTRARIAN]** Test-driven development: focusing on making the next test pass is tactical programming in pure form and leaves no moment for design; the one place he endorses test-first is bug fixing, to prove the test actually triggers the bug. [157]
- Design patterns help when they fit; over-application and forcing a pattern are the risk. [158]
- **[AGAINST]** Getters and setters: they are shallow, they expose implementation, and the Java habit of generating them is an over-application; better not to expose the field at all. [158-159]
- Rule for any new paradigm: ask whether it reduces complexity in large systems. [159]

## Chapter 20 -- Designing for Performance [161-170]

- Neither optimise everything nor ignore performance (death by a thousand cuts); know what is intrinsically expensive (network round trips, disk and flash I/O, allocation, cache misses), learn it by micro-benchmarking, and pick naturally efficient designs when they are equally simple (hash table over ordered map, arrays of structs over arrays of pointers). [161-162]
- Take complexity for speed only with evidence it matters (RAMCloud's kernel bypass); otherwise start simple. Simpler code is generally faster: fewer special cases, fewer layer crossings. [162-163]
- **[KEY]** Measure before and after; intuition about hot spots is unreliable even for experts; back out changes that do not measurably help unless they also simplify. [163-164]
- Design around the critical path: imagine the minimum code for the common case ignoring the current structure, then find a clean design close to it; ideally one test at the top catches all special cases and routes them off the fast path. [164-165]
- RAMCloud Buffer rewrite: the old append path checked six conditions across three shallow layers with near-identical signatures (a pass-through smell); the new one keeps an availableAppendBytes field so one comparison covers all cases; result roughly twice as fast and a fifth less code. [165-170]
- Conclusion: clean design and speed are compatible; simplicity is the key to both. [170]

## Chapter 21 -- Decide What Matters [171-174]

- The thread through the book: separate what matters from what does not, make the former prominent and the latter hidden -- that is what abstraction, naming and performance work all do. [171]
- Find what matters by looking for leverage (one solution or one fact serving many situations, e.g. the general text API, invariants); choosing among alternatives makes importance visible; when unsure, commit to a hypothesis and learn from the outcome. [171-172]
- Minimise what matters (fewer required constructor arguments, defaults, auto-computed parameters, exceptions handled low); emphasise what matters through prominence, repetition and centrality. [172-173]
- Two failure modes: treating too much as important (irrelevant arguments, Java's buffered/unbuffered distinction, shallow classes) and missing something important (hidden information, missing functionality, unknown unknowns). [173]
- Good taste is the name for this discrimination; it applies to technical writing and beyond. [174]

## Chapter 22 -- Conclusion [175-176]

- One subject: complexity, its two causes, the red flags that reveal it, the handful of techniques (deep and general classes, errors defined away, interface docs apart from implementation docs) and the investment mindset. [175]
- Cost is front-loaded and larger while learning; the reward is that design is the fun part and good designers spend more time there and less chasing bugs. [175-176]

## Back matter: the author's own summaries [181-184]

- A sixteen-item list of principles and a fifteen-item list of red flags, each pointing at its page. In my grouping: the mindset items (complexity accrues from small things; working code is not the bar; keep investing; design twice; increments are abstractions; decide what matters); the module-shape items (deep; common case simplest; simple interface over simple implementation; general over special and the two kept apart; different abstraction per layer; complexity pulled down; errors defined away); and the readability items (comments say the non-obvious; design for readers). The red flags are the ones marked per chapter above: shallow module, leakage, temporal decomposition, overexposure, pass-through method, repetition, special-general mixture, conjoined methods, comment repeating code, implementation detail in interface docs, vague name, hard-to-name, hard-to-describe, non-obvious code. [181-184]

---

## Ideas that could become a yes/no check on a code diff

- Does the diff add a method whose body is essentially one call with the same arguments to another method? (Ch. 7, p. 52)
- Does the diff add a class or method whose interface is about as large as its implementation, e.g. a one-line wrapper around a field or map operation? (Ch. 4, p. 25)
- Does the diff add a public getter/setter pair that merely exposes a field? (Ch. 19, p. 158)
- Does the diff thread a new parameter through intermediate functions that never use it? (Ch. 7, p. 57)
- Does the diff put the same knowledge (a format, a constant, a layout) into more than one module? (Ch. 5, p. 31)
- Does the diff add a new configuration parameter without a default, or one whose value the code could compute itself? (Ch. 8, p. 62-63)
- Does the diff add a new exception type or a new throw for a condition that could be made normal behaviour by redefining the operation? (Ch. 10, p. 81)
- Does the diff add several catch blocks that do the same thing where one handler higher up would do? (Ch. 10, p. 84-86)
- Does the diff swallow an error that callers need to know about? (Ch. 10, p. 89)
- Does the diff add a special-case branch that a different representation of the normal case would remove? (Ch. 6, p. 48; Ch. 20, p. 165)
- Does the diff add a method used from exactly one call site that mirrors one UI or caller feature instead of a general primitive? (Ch. 6, p. 44)
- Does the diff return an internal collection or data structure directly from a public method? (Ch. 5, p. 35)
- Does the diff duplicate a non-trivial block of code instead of restructuring so it runs once? (Ch. 9, p. 68)
- Does the diff split a method into pieces that can only be understood by reading both? (Ch. 9, p. 75)
- Does the diff split a method or class purely because of length? (Ch. 9, p. 73-76)
- Does the diff add a decorator/wrapper class where the feature could sit in the wrapped class? (Ch. 7, p. 55)
- Does every new class, public method and field carry an interface comment? (Ch. 13, p. 103)
- Does any new comment restate the identifier's words or the adjacent line? (Ch. 13, p. 104)
- Does any new interface comment describe internals a caller does not need? (Ch. 13, p. 114)
- Does a new method comment state each argument's meaning, bounds, null meaning, side effects, exceptions, preconditions? (Ch. 13, p. 110-111)
- Does a new variable comment say what the value represents rather than how it changes? (Ch. 13, p. 107)
- Does a new interface comment need to be long to be complete? (Ch. 15, p. 133)
- Is a new name generic or ambiguous (`count`, `status`, `result`, `data`, `x`), or does it reuse an existing name for a different concept? (Ch. 14, p. 123-126)
- Is a new boolean named as a predicate? (Ch. 14, p. 124)
- Does a new name carry a redundant type or class word? (Ch. 14, p. 127)
- Does the diff return a generic tuple/pair where a named structure would say what the fields are? (Ch. 18, p. 151)
- Does the diff declare a variable with a broader type than what it allocates? (Ch. 18, p. 151)
- Does the diff introduce a style, naming or structure that differs from the surrounding file's convention? (Ch. 17, p. 145)
- Does the diff change existing comments that describe the code it modified? (Ch. 16, p. 142)
- Does the diff leave design rationale only in the commit message and not in the code? (Ch. 16, p. 140)
- Does the diff put a comment far from the code it describes, or copy the same explanation to several places? (Ch. 16, p. 139-141)
- Does a new event handler or callback document when and by whom it is invoked? (Ch. 18, p. 150)
- Does the diff add implementation inheritance where composition would do? (Ch. 19, p. 154)
- Does a performance change come with before/after measurements? (Ch. 20, p. 163)
- Does the diff add a layer whose abstraction is the same as the layer beneath it? (Ch. 7, p. 51)

## Ideas that are mindset or process rather than a check

- Working code is not the goal; a good design that works is. (Ch. 3)
- Spend a steady fraction of time on design, proactively and when meeting a flaw. (Ch. 3)
- Zero tolerance for "a little" complexity, because it only ever accumulates. (Ch. 2)
- Judge complexity by readers, not by the author; a reviewer's "not obvious" is final. (Ch. 2, 13, 18)
- Sketch two radically different designs before committing to one, at every level. (Ch. 11)
- Write interface comments before bodies and use their length as a depth gauge. (Ch. 15)
- Decompose by knowledge, not by execution order. (Ch. 5)
- Build somewhat general-purpose modules even for a single current use. (Ch. 6)
- Take the implementer's pain to spare users: simple interface over simple implementation. (Ch. 8)
- After each modification, the code should look as if it had been designed for it; refactor rather than patch. (Ch. 16)
- Increments of development are abstractions, not features; resist TDD and feature-by-feature growth. (Ch. 19)
- Enforce conventions with a tool in the commit path and with nit-picky review; do not improve conventions casually. (Ch. 17)
- Learn what is expensive by micro-benchmarking; optimise only measured critical paths. (Ch. 20)
- Decide what matters, minimise it, make it prominent; cultivate taste. (Ch. 21)
- Design is the fun part; invest in the skill, not only in the code. (Ch. 22)
