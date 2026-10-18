# Contieri, Clean Code Cookbook -- working notes

Source: Maximiliano Contieri, Clean Code Cookbook (O'Reilly, Sept 2023, 1st ed.). PDF has 431 pages; book pagination runs i-xvii then 1-409. Page numbers below are the BOOK's page numbers (PDF page = book page + 20). Notes are my own paraphrase; nothing is quoted.

## Front matter (p. xi-xvii)

- Foreword (Carlos Ferro): the recipes matter less than the discussion each one opens; human readers remain the audience even in the age of AI-generated code.
- Preface: 25 chapters, each starting from principles; the ONE guiding rule is a 1:1 mapping between real-world entities and the design, from which everything else is derived. Language-agnostic, code is pseudocode, readability wins over performance whenever they conflict. Author used AI assistants to translate examples into 25+ languages.

## Chapter 1 -- Clean Code (p. 1-5)

Framing, no recipes. Key positions:
- A smell is a hint, not a verdict; recipes are heuristics and the cost of applying them must be weighed each time.
- Distinguishes SAFE refactorings (behaviour-preserving, IDE-automatable) from SEMANTIC refactorings that change behaviour on purpose; the latter need behavioural test coverage and must never be mixed with a feature or a fix.
- Readability beats performance; optimise only measured bottlenecks (Pareto).
- Target is mostly backend code with business rules; AI code generators mostly produce anemic code, so clean code matters more, not less.
- Vocabulary is deliberately loose (method/function, attribute/property, protocol/interface, argument/collaborator are used interchangeably).
- Talks about OBJECTS, not classes: classes are an accidental mechanism for making objects; what matters is which real-world thing an object stands for.

## Chapter 2 -- Setting Up the Axioms (p. 7-15) -- CENTRAL

The book's foundation. Software is a SIMULATOR; the author's acronym MAPPER: a Model that is Abstract, Partial, Programmable, Explanatory and about Reality.
- Model: a lens on one aspect of reality whose purpose is prediction.
- Abstract: defined by contracts and behaviour, not by how things are done.
- Partial: model only the slice that matters -- most overdesign recipes trace back to violating this letter.
- Explanatory: declarative enough that a reader can follow what it does (contrast with opaque ML models).
- Reality: the real world is the final arbiter of what belongs in the model.
- The ONE design principle (2.8): every domain entity corresponds to exactly one object in the model and vice versa (a BIJECTION). Four violations illustrate it: one object for several real things (a bare number standing for metres and inches -- Mars Climate Orbiter); two objects for one real thing (Jane Doe as judge and as athlete); an entity modelled as a data bag rather than a behaving object (a wallet); and a model that accepts what reality rejects (a Date that silently turns November 31 into December 1, violating fail fast).
- Sapir-Whorf aside: thinking of objects as data holders shapes the model into an anemic one; the author also insists on the word defect rather than bug.
- Essential vs accidental (Brooks, via Aristotle) is used throughout: an object's ESSENCE is fixed at birth and must not mutate; only accidental aspects may change. This single idea drives the anemic-model, mutability, setter and if chapters.

## Chapter 3 -- Anemic Models (p. 17-36)

Intro: objects that are bags of attributes with getters and setters break encapsulation and invite procedural code; the book wants rich objects with behaviour.

- Recipe 3.1 (p. 18): public attributes manipulated from outside -> make every attribute private and expose behaviour, because external manipulation is duplicated all over the system and the object cannot protect itself; noted as a semantic (unsafe) refactoring.
- Recipe 3.2 (p. 19): an object whose essential attributes can be changed after creation (date.setMonth) -> set the essence in the constructor and freeze it, because changing the essence makes it a different real-world thing and ripples into every dependent object; use an immutable date and a protocol like defer that returns a new one.
- Recipe 3.3 (p. 21): setters -> remove them, pass essential values to the constructor, change objects only through methods whose job is a business action (tell, don't ask), because setXXX has no real-world counterpart and scatters invariant checks.
- Recipe 3.4 (p. 23): code wizards and generators that emit attribute-plus-accessor classes (today: AI assistants) -> write explicit classes and find the missing abstraction for the repeated part, because generated anemic code duplicates and cannot be debugged.
- Recipe 3.5 (p. 25): automatic properties (get; set;) -> hand-written private attribute with constructor and real behaviour, because the language feature makes anemic objects the path of least resistance. CONTRARIAN: getters and setters are called bad industry practice outright.
- Recipe 3.6 (p. 26): DTOs mirroring domain objects -> transfer real objects, or plain arrays/dictionaries for truly anemic data, with proxies and null objects to cut the reference graph, because DTOs duplicate structure, carry inconsistent data and pollute the namespace. CONTRARIAN versus layered-architecture practice; the author concedes DTOs are an established tool to be used with care.
- Recipe 3.7 (p. 29): empty constructors producing incomplete objects -> one complete constructor taking all essential arguments, because an object must be valid from inception (Plato's essential immutability); stateless objects and persistence frameworks that demand an empty constructor are the exceptions.
- Recipe 3.8 (p. 30): getters (getWidth, getData returning the internal list) -> domain-named behaviour (width, area) and never a reference to an internal collection, because getXXX is implementation talk, couples callers to representation and returning internals breaks encapsulation and Demeter; a getter that coincides with a real responsibility (a window's colour) is fine under a domain name.
- Recipe 3.9 (p. 33): code reaching into other objects' properties (a distance calculator reading point.x) -> protect the properties and expose behaviour so the representation (cartesian vs polar) can change, because coupling to protocol is cheaper than coupling to data.
- Recipe 3.10 (p. 35): properties assigned on an object without being declared -> declare every attribute explicitly, because dynamic properties hide typos, defeat type safety and collide silently; compiler options can forbid them.

## Chapter 4 -- Primitive Obsession (p. 37-51)

Intro: the data-first schooling of the 80s/90s (ERDs) taught engineers to think in attributes; the book wants behaviour first and small cohesive objects.

- Recipe 4.1 (p. 38): big objects whose fields are all primitives (a person's name as a String) -> find the small concept hiding behind the primitive (Name, a five-letter Wordle word) and give it its own object, because the primitive has responsibilities the concept does not and vice versa; the performance objection is dismissed as premature.
- Recipe 4.2 (p. 39): primitives passed around as ints and strings (port numbers, URIs as strings) -> small validated objects (Port, URI, Path), because duplicated manipulation and missing validation are what/how confusion; the author admits the industry is lazy here.
- Recipe 4.3 (p. 41): associative arrays standing for real things (a coordinate as a two-key map) -> real objects that validate themselves at creation (Latitude between -90 and 90), because arrays are for prototyping and objects are for serious work.
- Recipe 4.4 (p. 43): heavy string parsing, regex splitting and substring work -> the objects the strings stand for (School with a Location), because the manipulation is accidental and the real protocol is missing; benchmark before keeping the string version.
- Recipe 4.5 (p. 44): timestamps used only for ordering -> a central sequence issuer, because two timestamps can collide and sequencing is the essential need; timestamps only when the domain really has them. UNUSUAL.
- Recipe 4.6 (p. 45): validating a subset of a type everywhere (emails among strings, ages among numbers) -> an object for the subset that refuses invalid values at birth, because the subset exists in the domain and enforcement belongs in one place (fail fast).
- Recipe 4.7 (p. 46): string validation inside an unrelated class (Address validating an email) -> a dedicated EmailAddress that is valid by construction, because it restores single responsibility and DRY; the efficiency objection is premature optimisation.
- Recipe 4.8 (p. 49): objects designed from their attributes (a person with name and job before any need) -> start from behaviour and add attributes only when behaviour demands them (TDD as discovery tool), because attribute-first models are coupled and over-built (YAGNI).
- Recipe 4.9 (p. 50): from and to dates passed as a pair with no invariant -> an Interval object that rejects a start after its end and owns elapsedDays, because the invariant otherwise lives nowhere and the computation is duplicated.

## Chapter 5 -- Mutability (p. 53-67)

Intro: reverse the burden of proof: objects are immutable unless proven otherwise, and may change only in accidental aspects, never in their essence. Three corollaries: complete at creation (5.3), no setters (3.3), no getters unless the real world has them (3.8). The Date class of every mainstream language is given as the cautionary example.

- Recipe 5.1 (p. 55): values that never change declared as mutable variables -> declare constant by default, mutable only when needed, because scope and mutability declared explicitly make intent visible; mutation testing confirms a value really is constant.
- Recipe 5.2 (p. 56): a variable assigned once and never changed -> promote it to a constant or a named function, because the mutability declaration should match the domain and a linter can find single-assignment variables.
- Recipe 5.3 (p. 58): setters that change an essential attribute (setMonth) -> delete them, because the essence cannot change in the real world and allowing it ripples through every holder of the reference; a semantic refactor needing tests.
- Recipe 5.4 (p. 59): const arrays that still accept push -> treat const as a reference guarantee only and build new arrays (spread) instead of mutating, because constant is not immutable and the language will not tell you.
- Recipe 5.5 (p. 61): lazy initialisation (the or-equals idiom, null-then-create) -> initialise essentials in the constructor; for genuinely expensive resources use a proxy or provider, because lazy init is a premature optimisation that adds nulls, races and often a singleton.
- Recipe 5.6 (p. 63): constants whose nested contents can be modified -> deep-freeze, or better, an object with no setters that can be replaced in tests, because a mutable constant violates least surprise.
- Recipe 5.7 (p. 65): functions touching global state or external resources -> pure functions that work on their arguments and return results, because side effects couple, break reentrancy and surprise; linters warn on global access.
- Recipe 5.8 (p. 66): using a variable before its declaration (hoisting) -> declare, preferably as const, at the top of the scope, because hoisting is a compiler convenience that makes debugging a guessing game.

## Chapter 6 -- Declarative Code (p. 69-87)

Intro: say what, not how; modern VMs make low-level hand-optimisation unnecessary, so the remaining job is readable, high-level code.

- Recipe 6.1 (p. 70): one variable (total) reused for different purposes in consecutive blocks -> narrow each use to its own scope by extracting methods, because reuse comes from copy-paste, confuses debugging and blocks extraction tools.
- Recipe 6.2 (p. 71): long methods whose blocks are separated by blank lines -> each blank-line-delimited chunk becomes a named method, because the blank line already marks a unit of behaviour; linters can warn on blank lines inside methods.
- Recipe 6.3 (p. 72): methods carrying versions in their names (findMatch_new, _old, _20200229) -> one method, history in version control, because the name is not the place for time.
- Recipe 6.4 (p. 73): negatively named predicates negated again (not isNotFinished) -> positive names, because double negation misdirects the reader; a linter regex on not-prefixed names helps.
- Recipe 6.5 (p. 74): behaviour in the wrong object (a graphics editor defining pi; add as a free operation on two numbers) -> ask a domain person whose responsibility it is and move it there (RealConstants, Number), because responsibilities in strange places duplicate.
- Recipe 6.6 (p. 76): index-based loops -> foreach, iterators and higher-order collection operations, because indices break encapsulation and are accidental unless the domain really maps items to natural numbers.
- Recipe 6.7 (p. 77): a design decision recorded as a comment (set memory before running) -> a method whose name carries the reason (increaseMemoryToAvoidFalsePositives), because comments rot and do not compile; a test is better still when one can be written.
- Recipe 6.8 (p. 77): literal numbers in formulas (299792) -> named constants or parameters, because the source of the number is lost and it cannot be swapped in tests; linters detect numeric literals.
- Recipe 6.9 (p. 78): a business rule written in terms of implementation detail (if stepWork has pending tasks) -> name the rule (canMoveOn) and hide the mechanism under it, because the what survives change and the how does not; indirection cost is negligible on a modern VM.
- Recipe 6.10 (p. 80): one opaque regular expression -> compose it from small named parts, and keep regexes for string validation only, because a regex is unreadable and untestable by parts; objects for anything beyond validation.
- Recipe 6.11 (p. 81): constant on the left of a comparison (Yoda style) -> variable left, expected value right, because that is how people read and the assignment-typo defence is a compiler's job. CONTRARIAN to a widespread C-era convention.
- Recipe 6.12 (p. 81): jokey or offensive names (eradicateAndMurderAllCustomers) -> plain professional names, because humour costs readability and reputation; a forbidden-word list can be automated.
- Recipe 6.13 (p. 82): nested callbacks (pyramid of doom) -> promises and async/await written as a sequence, because nesting hides the order of operations and the error path.
- Recipe 6.14 (p. 84): vague error texts and dialogs (Cancel? Yes/No) -> messages stating consequence and the available actions, naming the business rule (between 1 and 100, not out of bounds); and never a valid-looking value (balance 0) in place of an error.
- Recipe 6.15 (p. 86): language-level magic corrections (an invalid date silently normalised, number plus string, negating a number) -> make them fail, because a model that accepts what the real world rejects breaks the bijection and fail fast.

## Chapter 7 -- Naming (p. 89-110)

Intro: names are for humans; a generic or wrong name is a defect waiting to happen.
- Recipe 7.1 (p. 89): abbreviated names (fmt, YVC) -> spell the concept out in full, because an abbreviation maps one token to several real-world concepts and the reader pays the decoding cost every time; single letters are fine only in math where the formal context is tiny.
- Recipe 7.2 (p. 91): a class called Helper/Util holding unrelated static services -> name it for what it really is and split it into one object per responsibility (or a stateless object per service), because a helper has no real-world counterpart and is a grab bag by construction.
- Recipe 7.3 (p. 94): variables prefixed my -> name the role the object plays (salesWindow, not myWindow), because the prefix carries no information about context.
- Recipe 7.4 (p. 95): variables called result/theResult -> name them after the thing they hold (as a fallback, the name of the last call), because a generic noun forces the reader to trace the assignment; cites the Boy Scout rule against leave-it-alone attitudes.
- Recipe 7.5 (p. 97): a variable named after its type (regex, bool) -> name it for its role, because the type is an accidental implementation detail and the role is what the model needs; a linter can flag names equal to class or type names.
- Recipe 7.6 (p. 98): over-long redundant names -> shorten by dropping repeated context, but never with invented abbreviations; real-world acronyms (URL, SSN) are fine because they are unambiguous in their domain.
- Recipe 7.7 (p. 99): pseudo-abstract names (Collection, Composite, Array, Abstract-, Base-, Manager) -> use the concrete domain word (Schedule, Portfolio, Journal), because abstractions come late, after many concrete cases, and vague words hide which concept is meant.
- Recipe 7.8 (p. 100): typos in identifiers -> fix them with a spell checker, because they hurt search and, worse, polymorphism depends on exactly equal method names.
- Recipe 7.9 (p. 100): attributes prefixed with the owning class name (empName inside Employee) -> drop the prefix, because attributes are always read in their class context; a linter can flag the redundancy.
- Recipe 7.10 (p. 101): Hungarian-style letter prefixes (IEngine, ACar) -> plain concept names, because the prefix leaks whether it is an interface or abstract, which is implementation, not domain.
- Recipe 7.11 (p. 102): wrapper variants of the same action (sort/doSort/basicSort) -> remove the wrapper methods; if layering is needed, use decorator objects, because the chain of wrappers hides the real entry point and couples methods.
- Recipe 7.12 (p. 104): plural class names (Users) -> singular, because a class stands for one concept and the plural is a collection of them.
- Recipe 7.13 (p. 104): the word collection in a name -> name the content (customers), because the container type is accidental; also notes that empty and non-empty collections are polymorphic and so avoid nulls and ifs.
- Recipe 7.14 (p. 105): classes suffixed Impl (and interfaces prefixed I) -> name the real concept; if both exist give both real names, because AddressImpl exists nowhere in the world.
- Recipe 7.15 (p. 106): arguments named by position (first, second) -> name them by role (minuend, subtrahend; expected, actual), because role names carry meaning far from the definition.
- Recipe 7.16 (p. 107): parameter names repeating the class name -> drop the repetition, because parameters are local and contextual; repeating the class name hints at construction from properties instead of behaviour.
- Recipe 7.17 (p. 108): a project or team prefix on every class (WEBBExoplanet) -> remove it, because ownership prefixes add no meaning and hurt search.
- Recipe 7.18 (p. 110): variables named data -> a domain, role-suggesting name, because data is everywhere and names everything, and the word nudges towards anemic treatment.

## Chapter 8 -- Comments (p. 111-121)

Intro: comments are a hangover from assembly-era distance between intent and code; today a comment usually marks a failure to name things; keep them only for important design decisions.

- Recipe 8.1 (p. 111): commented-out code -> delete it and rely on version control, because it is dead text that rots and nobody maintains; hard to detect automatically.
- Recipe 8.2 (p. 113): comments that no longer match the code -> delete them (or replace with a test), because comments diverge silently and mislead; exception: critical design decisions on performance or security that cannot be expressed in code.
- Recipe 8.3 (p. 114): hacking a condition with a literal true/false to skip or force a branch while debugging -> remove the dead condition and force the scenario with a test instead, because the hack gets forgotten and ships.
- Recipe 8.4 (p. 116): a trivial comment on a getter -> remove both the comment and, ideally, the getter, because trivial functions document themselves.
- Recipe 8.5 (p. 117): a comment describing what a block does -> extract the block and turn the comment into the function name, because names are maintained with the code and comments are not; a comment-to-code ratio can be monitored by a linter.
- Recipe 8.6 (p. 118): section comments inside a method body (stage 1, stage 2) -> extract each section into a method named after its comment, because a comment inside a body is a sign that the method is several actions.
- Recipe 8.7 (p. 120): a comment specifying behaviour and edge cases -> rename the function for the what, write one test per case stated in the comment, delete the comment, because tests are executable documentation and comments are not; private methods are the exception (test them indirectly or extract them).

## Chapter 9 -- Standards (p. 123-132)

- Recipe 9.1 (p. 123): mixed conventions across one codebase -> adopt one standard for the organisation and enforce it automatically before merge, because reading code written many ways taxes everyone and consistency enables collective ownership; which standard matters less than having one.
- Recipe 9.2 (p. 126): tabs and spaces mixed -> pick one and enforce it, because consistency, not the choice, is the point; in indentation-significant languages it is semantics.
- Recipe 9.3 (p. 127): camelCase, snake_case and MACRO_CASE mixed -> choose one per language and enforce by linter; exception: match a foreign client's convention when talking to its code.
- Recipe 9.4 (p. 128): identifiers in a natural language other than English, or mixed -> English throughout including business terms, because mixing breaks polymorphism (add vs agregar), adds load, and English is the lingua franca of every language's primitives.
- Recipe 9.5 (p. 130): similar functions with parameters in different orders -> keep one order everywhere, or use named arguments, because swapped arguments go unnoticed.
- Recipe 9.6 (p. 131): something out of place noticed while changing nearby code -> fix it (Boy Scout rule), because left messes invite more; needs test coverage and team consensus.

## Chapter 10 -- Complexity (p. 133-148)

Intro: a senior's main skill is keeping accidental complexity minimal.

- Recipe 10.1 (p. 133): duplicated behaviour (not merely duplicated text) -> find the missing abstraction and move the behaviour there, because defects multiply with copies and duplication signals an absent concept; linters find textual repeats but not similar patterns.
- Recipe 10.2 (p. 135): global settings and feature toggles steering behaviour -> inject polymorphic strategy objects and retire toggles once mature, because each boolean doubles the test space and settings are global coupling; CONTRARIAN: configurability is called a customer's dream and an engineer's nightmare; short-lived toggles in CI/CD are tolerated.
- Recipe 10.3 (p. 137): state stored as a mutable attribute changed by setters -> model state as membership in a collection (pendingOrders, confirmedOrders), because state is accidental to the object and set membership matches the real world; author admits this is counterintuitive and warns against overdesign (a widget's colour is a counterexample).
- Recipe 10.4 (p. 139): clever one-letter, trick-laden code -> plain readable code with full names, after covering it with tests, because readability beats micro-cleverness; exception: proven low-level hot spots.
- Recipe 10.5 (p. 141): awaiting independent asynchronous tasks one after another -> wait for all at once, because imposing an order that the business rule does not require is accidental.
- Recipe 10.6 (p. 142): long call chains (a.b().c().d()) -> talk only to direct collaborators and give them higher-level messages (dog.walk instead of iterating the dog's feet), because every link in the chain is coupling and a change anywhere breaks the caller (Demeter, tell-don't-ask).
- Recipe 10.7 (p. 143): a long algorithmic method -> reify it as a method object: invocation becomes an object, temporaries become attributes, then split; because the pieces become testable and reusable; Beck's method object.
- Recipe 10.8 (p. 145): JavaScript's new Array(n) constructor -> use the literal syntax, because the constructor's meaning depends on argument count and violates least surprise.
- Recipe 10.9 (p. 147): short-lived objects that only forward to another (a Driver that just calls car.drive) -> remove the intermediary, because indirection without business value is accidental complexity.

## Chapter 11 -- Bloaters (p. 149-162)

- Recipe 11.1 (p. 149): methods with too many lines -> extract parts (8-10 lines is enough for most), because long methods have low cohesion, high coupling and are hard to test; every linter can measure it.
- Recipe 11.2 (p. 151): more than about three arguments -> group related ones into a small object (PrintSetup) that enforces its own consistency on creation, because the grouping reveals a missing concept and primitives should be avoided; linters warn on count.
- Recipe 11.3 (p. 152): many variables alive at once -> narrow scopes by extracting methods, because a polluted scope hides unused variables and confuses debugging.
- Recipe 11.4 (p. 154): parentheses beyond what precedence needs -> remove them, because they break left-to-right reading; a trade-off, some grouping aids a complex formula.
- Recipe 11.5 (p. 155): a class with too many methods -> split into cohesive classes named after real concepts, because a protocol dumped into the first convenient class is incohesive; linters count methods.
- Recipe 11.6 (p. 157): a class with many attributes -> cluster attributes by the methods that use them and extract an object per cluster, because bloated objects know too much and are merge-conflict magnets; linters count attributes.
- Recipe 11.7 (p. 158): a long import list -> break the dependencies, because the list is a direct measure of coupling; threshold enforceable by linter.
- Recipe 11.8 (p. 159): functions that do two things (and in the name) -> split unless atomicity is required, because two tasks in one scope couple and resist testing; the name is a heuristic with false positives.
- Recipe 11.9 (p. 161): an interface whose implementors throw not-supported for some methods -> split the interface (interface segregation), because clients should not depend on protocol they do not use.

## Chapter 12 -- YAGNI (p. 163-172)

- Recipe 12.1 (p. 163): unused code kept just in case -> delete it, because nobody maintains code that does not run and git remembers it; coverage finds it, but beware metaprogramming.
- Recipe 12.2 (p. 165): diagrams as the documentation of behaviour -> let code and tests be the living documentation, because diagrams show structure (accidental) and go stale, while tests cannot lie; high-level pictures for human communication are fine. CONTRARIAN: forbid code annotations and CASE-style design artefacts.
- Recipe 12.3 (p. 167): an abstract class with a single subclass -> collapse it until real second cases appear, because generalising ahead of evidence is speculation; compile-time detectable.
- Recipe 12.4 (p. 168): an interface with a single realisation -> drop it until a second one exists, because premature protocols are overengineering; exceptions: framework protocols, dependency inversion contracts, and interfaces needed for test doubles.
- Recipe 12.5 (p. 170): classes named after the pattern they implement (FileTreeComposite, PermutationSorterStrategy) -> name them after the domain thing and remove the pattern machinery where it adds nothing, because the pattern is implementation and the name should be essential.
- Recipe 12.6 (p. 170): a hand-rolled collection class with no behaviour beyond the standard one -> use the language's standard collection, because an abstraction that adds no behaviour is waste; the author notes this appears to contradict his modelling rule and resolves it with the P (partial) of MAPPER: model only what matters.

## Chapter 13 -- Fail Fast (p. 173-183)

Intro: a silent failure is a lost chance to find the root cause.

- Recipe 13.1 (p. 173): one variable reused for unrelated values across a function -> separate variables with the smallest scope, because reuse blocks extraction and saves no memory on a modern VM.
- Recipe 13.2 (p. 175): objects that can be built or mutated into invalid states -> check preconditions and invariants in the constructor and keep assertions on in production unless proven too costly, because corruption discovered late is far harder to debug (design by contract).
- Recipe 13.3 (p. 177): a function that accepts many argument shapes and sorts them out with ifs -> accept one shape under one contract, because magic casting hides errors and violates fail fast.
- Recipe 13.4 (p. 178): a default branch in a switch doing something plausible -> make default throw, because default means cases nobody has thought of yet, and failing beats guessing; a linter can flag default without an exception.
- Recipe 13.5 (p. 180): removing from a collection while iterating it -> iterate a copy or use the language's filtering primitive, because the breakage shows up far from the loop and copying small collections is cheap.
- Recipe 13.6 (p. 181): a hash override without an equality override (or vice versa) -> define both consistently, because equal hash does not imply equal object and collections will lie; linters check this pair.
- Recipe 13.7 (p. 183): refactoring and changing behaviour in one step -> separate the two, run tests between, because mixed changes hide defects from review and create merge conflicts.

## Chapter 14 -- Ifs (p. 185-215)

Intro: ifs, switches and early returns are the goto of structured code; most are tied to accidental decisions and break open/closed. Central distinction: an ESSENTIAL if mirrors a rule people state as an if in the domain (age under 18) and stays; an ACCIDENTAL if branches on an implementation artefact (a rating string) and should become polymorphism.

- Recipe 14.1 (p. 186): accidental ifs on type-like strings or codes -> create a small hierarchy per condition, move each branch body into its class, replace the if with one polymorphic call; because new cases then arrive as new classes instead of new branches. Rule of thumb for not over-abstracting: build abstractions inside one domain (movie and rating), not across domains (movie and age); null checks are always accidental.
- Recipe 14.2 (p. 192): boolean flags with vague names (flag, found) -> name them for the event they record (atLeastOneElementWasFound), because a flag says what happened and the reader should not have to reconstruct it.
- Recipe 14.3 (p. 193): boolean parameters and attributes that steer behaviour -> replace with polymorphic objects (a LoginStrategy instead of useLogin), because every boolean breeds an if and breaks open/closed; a boolean that exists in the domain may stay.
- Recipe 14.4 (p. 195): switch/case/elseif ladders -> polymorphic objects chosen by registration or strategy, because each new case otherwise edits the central method; author explicitly refuses to ban ifs outright and suggests a ratio warning instead.
- Recipe 14.5 (p. 197): a hardcoded chain of equality tests mapping codes to values -> a lookup collection, because tables are data and testable while ladders are not.
- Recipe 14.6 (p. 198): full (non-short-circuit) boolean evaluation where the second operand is invalid when the first fails -> short-circuit operators, because evaluating an undefined second term is a defect; do not misuse short-circuit as a control structure (14.9).
- Recipe 14.7 (p. 199): an if with an implicit else (fall-through return) -> make the remaining cases explicit and let the last branch fail fast, because the implicit path hides unforeseen inputs; author notes this recipe is contested.
- Recipe 14.8 (p. 200): nested boolean checks returning true/false at the bottom -> return the boolean formula directly, because a stair of ifs obscures a rule a domain expert could read as one expression.
- Recipe 14.9 (p. 202): a && sideEffect() used as a compact if -> write the if, because boolean operators are for conditions, not control flow, and this is cleverness.
- Recipe 14.10 (p. 203): deeply nested if/else arrows -> flatten by extraction and by removing accidental ifs, because nesting depth is unreadable and untestable; linters measure depth.
- Recipe 14.11 (p. 205): functions returning an explicit true/false after an if -> return the business condition itself, and beware returning booleans at all since each one needs an if downstream; UNUSUAL stance that most booleans do not exist in the domain.
- Recipe 14.12 (p. 207): comparing against a boolean constant (x == true) -> use the value directly, because in truthy languages the comparison invokes casting surprises; the bash example shows a non-empty string tested as true.
- Recipe 14.13 (p. 208): long multi-statement ternaries -> extract each arm to a function so the ternary reads as a formula, or use polymorphism, because ternaries are expressions, not blocks.
- Recipe 14.14 (p. 209): methods doing the same action under different names (arraySort, listSort) -> one name under a shared protocol, because polymorphism needs identical signatures; names must follow concept, not accidental type.
- Recipe 14.15 (p. 211): the same attribute comparison repeated across callers -> move the comparison into one method on the owning object, because a changed rule (case sensitivity) then changes once; tell-don't-ask.
- Recipe 14.16 (p. 212): magic business conditions hardcoded inline (special customer by name) -> extract into an intention-revealing method on the right object, or into configuration when it is genuinely a setting; TDD legitimately starts hardcoded, then generalises when evidence arrives.
- Recipe 14.17 (p. 213): boolean sub-expressions that are always true/false (leftover debugging) -> remove them, because they are either dead or a hidden bug.
- Recipe 14.18 (p. 214): nested ternaries -> early-return ifs, a lookup map or polymorphism, because nesting is the problem whatever the syntax.

## Chapter 15 -- Null (p. 217-230)

Intro: null is a flag carrying several meanings at once (absent, undefined, error) and is therefore the least cohesive object in any system; it breaks the one-to-one mapping to the domain. Author argues AGAINST null outright.

- Recipe 15.1 (p. 217): null used for absence -> a null object with the same protocol (NullCoupon.discount returns the subtotal), because callers then need no checks and cannot forget one; cites Hoare's regret.
- Recipe 15.2 (p. 220): optional chaining, nullish coalescing, Elvis operators -> remove them by removing the nulls they paper over, because they make null tolerable instead of absent; CONTRARIAN versus common idiom (good: no nulls; bad: optional chaining; ugly: untreated nulls).
- Recipe 15.3 (p. 223): an attribute that may be missing -> model it as a collection with zero or one element, because empty and non-empty collections are polymorphic and iterate without checks; cardinality can be enforced.
- Recipe 15.4 (p. 224): a NullSomething subclass for every class -> instantiate a real object with neutral values (empty strings, zero) where one exists, because the pattern-driven hierarchy is overdesign and inheritance is not the only route to polymorphism; the null object must not be global or a singleton.
- Recipe 15.5 (p. 227): a sentinel value for unknown data (0,0 coordinates, Null Island) -> an explicit UnknownLocation polymorphic with real locations, because sentinels collide with valid data and silently mislead.

## Chapter 16 -- Premature Optimization (p. 231-247)

Intro: optimisations add layers between model and domain and must be justified by measured evidence; leave accidental optimisation to tools and AI assistants.

- Recipe 16.1 (p. 232): numeric ids inside domain objects -> reference objects directly and keep ids only at the system boundary (API, database), using opaque keys there, because ids do not exist in the domain and leak persistence into the model. CONTRARIAN for most ORM-centred practice.
- Recipe 16.2 (p. 235): caching or other speculation without a benchmark -> remove it and optimise only with real-scenario evidence, because premature optimisation couples and obscures; prefer the readable version even if a synthetic loop says otherwise.
- Recipe 16.3 (p. 236): bitwise tricks (double tilde for truncation) -> the readable library call, because integer and boolean domains are distinct and the trick must be justified in review.
- Recipe 16.4 (p. 237): generalising from one or two similar functions into an abstraction -> keep them separate until the sameness is proven essential, because duplication can be accidental and premature abstraction is a bijection violation.
- Recipe 16.5 (p. 238): data-structure tricks for speed without a real-use benchmark -> write the readable version, benchmark with real data, then attack the measured hot 20 percent; CONTRARIAN aside: avoid languages built around performance (Go, Rust, C++) for business code.
- Recipe 16.6 (p. 240): code kept for a possible future use (anchor boats) -> delete it, because it is dead code with coupling; mutation testing shows what is really exercised.
- Recipe 16.7 (p. 241): a cache inside a domain object -> move it outside behind the same protocol, and only with evidence, because caches break determinism and invalidation is underestimated; model it after a real-world metaphor if you must.
- Recipe 16.8 (p. 243): callback names describing the action to take (handlePageChange) -> name events after what happened (onItemSelected), because the emitter should not know what the listener does.
- Recipe 16.9 (p. 244): database queries in a constructor -> constructors only build valid objects; persistence lives elsewhere, because side effects in construction couple domain to storage and kill testability.
- Recipe 16.10 (p. 245): resource release logic in destructors -> rely on the collector and explicit close protocols, and have the destructor merely complain if something is still open, because destructor code leaks and couples; exceptions: real-time and very low-level code.

## Chapter 17 -- Coupling (p. 249-279)

- Recipe 17.1 (p. 249): hidden assumptions such as units (the Mars Climate Orbiter) -> make them explicit objects (Measure with Unit), because an unstated contract is one that fails without warning.
- Recipe 17.2 (p. 251): singletons -> contextual unique objects passed in, because singletons are global coupling, untestable, not thread-safe and do not exist in the domain (a table of about twenty problems); ban getInstance by linter.
- Recipe 17.3 (p. 253): a god object with many responsibilities (also a constants dump) -> split by responsibility, because it violates single responsibility and attracts merge conflicts; method or constant counts can be thresholds.
- Recipe 17.4 (p. 256): one class changed for unrelated reasons -> split so each class has one reason to change, because divergent change marks mixed responsibilities.
- Recipe 17.5 (p. 257): 9999, -1 or MAXINT as an invalid marker -> an exception or a polymorphic special object, because a valid domain value cannot also mean invalid.
- Recipe 17.6 (p. 259): one requirement change touching many places -> consolidate the duplicated rule in one method, because the scatter reveals copy-paste or misplaced responsibility.
- Recipe 17.7 (p. 261): optional parameters with defaults -> explicit arguments, named parameters where available, because a default is a hidden coupling and a hidden if. UNUSUAL: optional arguments themselves treated as a smell.
- Recipe 17.8 (p. 263): a method using another object's data more than its own -> move the behaviour to the object that owns the data, because feature envy marks a misplaced responsibility.
- Recipe 17.9 (p. 264): a class that only forwards to another -> remove it, because empty indirection is complexity.
- Recipe 17.10 (p. 266): a defaulted parameter before a required one -> move defaults to the end (or remove them), because the signature becomes error-prone; compilers and linters check this.
- Recipe 17.11 (p. 267): small changes with wide effects (a Time class that also asks the OS for now) -> decouple with tests first, then isolate the varying part, because ripple effect is coupling made visible.
- Recipe 17.12 (p. 268): persistence, serialisation, display, logging, ids on a business object -> move each accidental concern to its own object, because a car should not know how to save itself.
- Recipe 17.13 (p. 270): validation rules in the UI -> validate in backend domain objects and return messages to clients, because UI rules are duplicated, bypassable and untestable; duplicate to the frontend only with evidence and automatically.
- Recipe 17.14 (p. 273): depending on concrete global classes -> depend on interfaces or traits, because interfaces change less and can be replaced in tests.
- Recipe 17.15 (p. 275): the same primitives always travelling together (from, to) -> reify them as one object (TimeInterval) that validates itself, because the clump is a missing concept.
- Recipe 17.16 (p. 277): two classes deeply entangled -> move behaviour so each talks to its own data, because intimacy means misassigned responsibilities; collaboration graphs can reveal it.
- Recipe 17.17 (p. 278): distinguishing objects the domain treats as interchangeable (a person in a queue simulation) -> model them as fungible, because identity that does not matter in reality is overdesign.

## Chapter 18 -- Globals (p. 281-288)

- Recipe 18.1 (p. 281): global functions callable from anywhere -> wrap them in a context object and narrow scope, because they are untraceable coupling.
- Recipe 18.2 (p. 282): static methods on classes -> instance methods on an object with that responsibility, because a class's single job is to create instances, and statics are globals you cannot substitute in tests. UNUSUAL: a blanket ban on statics beyond constructors.
- Recipe 18.3 (p. 284): goto -> structured loops and exceptions, because it has been known harmful for fifty years and still exists in Go, PHP, Perl, C#.
- Recipe 18.4 (p. 285): classes used as global entry points -> namespaced, specialised objects (a method object instead of a static formatter), because class names pollute the namespace and invite statics and singletons.
- Recipe 18.5 (p. 287): new Date() or now() called directly -> an explicit injected time source, because the current time is a global dependency that tests cannot control, and Date/Time classes should only create immutable values.

## Chapter 19 -- Hierarchies (p. 289-309)

Intro: inheritance is widely misused for code reuse; composition is dynamic and testable; hierarchies are for shared behaviour only.

- Recipe 19.1 (p. 289): deep inheritance used for reuse -> flatten by finding the protocol and composing (a Server delegating to a ChargingMethod), because deep trees are fragile, incohesive and break substitutability; depth of inheritance tree is a standard metric.
- Recipe 19.2 (p. 292): finding a method means bouncing up and down the hierarchy (yo-yo) -> compact it with interfaces and delegation, because reuse through small subclass differences lowers cohesion.
- Recipe 19.3 (p. 293): is-a subclassing for reuse (Square extends Rectangle) -> composition, subclass only on behaves-as-a, because the classic is-a violates Liskov; more than three levels is a smell.
- Recipe 19.4 (p. 295): inheritance justified by is-a from data modelling -> think in protocol: does it behave as the parent, because a real number cannot do what a complex number does, so mathematical is-a does not translate.
- Recipe 19.5 (p. 297): nested or inner classes -> promote them to top-level classes under a namespace, because nested classes map to nothing in the domain and are hard to test and reuse.
- Recipe 19.6 (p. 299): subclasses with abbreviated names that only make sense inside the hierarchy (North) -> fully qualified names, or namespaces where the language has them, because a global class name must stand alone.
- Recipe 19.7 (p. 300): concrete classes with subclasses -> make leaves final and parents abstract, because overriding a concrete class breaks substitutability; move shared protocol up into an abstract parent.
- Recipe 19.8 (p. 301): classes left neither abstract nor final -> mark every leaf final and every non-leaf abstract, because then the compiler enforces that no concrete class subclasses another; the author claims there is no valid case for two concrete classes in a parent-child relation.
- Recipe 19.9 (p. 303): classes with no behaviour (empty exceptions, middle-of-hierarchy classes, subclasses that only return different constants) -> replace with instances carrying the differing data, because a class is a unit of behaviour and different data is not different behaviour; linters flag empty classes.
- Recipe 19.10 (p. 304): abstractions invented before seeing enough concrete cases (Song split into ClassicalSong and PopSong, then the hybrid) -> keep concrete, generalise only from evidence, and name abstractions after naming their concrete members, because premature (Aristotelian) classification locks in a wrong first impression.
- Recipe 19.11 (p. 306): protected attributes -> make them private and share behaviour by composition or traits, because protected data is usually a sign of subclassing for reuse and of a Liskov violation.
- Recipe 19.12 (p. 308): empty method bodies left as placeholders (a mock processor that silently does nothing) -> throw a not-yet-implemented error or implement for real, because silent no-ops violate fail fast; only review catches it since empty bodies are sometimes legitimate.

## Chapter 20 -- Testing (p. 311-331)

Intro: tests are the living specification; the chapter is about tests that lie (weak, erratic, open-box) as much as about missing ones.

- Recipe 20.1 (p. 312): wanting to test a private method -> do not open it up or use reflection; if trivial leave it, if complex extract it into a method object with its own tests, because that keeps encapsulation and gives the computation a home (never a helper or a static).
- Recipe 20.2 (p. 313): assertions with only the framework's default failure message -> add a declarative description explaining the expectation (and ideally the diff), because the message is where the design intent belongs and it replaces comments.
- Recipe 20.3 (p. 315): assertTrue on a comparison -> the specific assertion (assertEquals with expected first), because the framework can then show the actual difference instead of two booleans.
- Recipe 20.4 (p. 316): mocking business objects -> use the real objects and mock only accidental externals (payment gateways, databases, APIs), because business mocks build a parallel fake system and give false confidence; architectural, not lintable.
- Recipe 20.5 (p. 318): vague assertions (area is not zero) -> assert the exact expected value, because weak tests create a false sense of coverage; mutation testing exposes them.
- Recipe 20.6 (p. 319): nondeterministic tests (depending on set ordering, network, external databases) -> remove every dependency the test does not control, because erratic tests destroy trust in the suite; detectable from run statistics.
- Recipe 20.7 (p. 321): exact equality assertions on floats -> compare with a tolerance, or avoid floats altogether, because rounding makes equal computations differ; a check on assertEquals can refuse float operands.
- Recipe 20.8 (p. 322): placeholder test data (xxxxx, gibberish names) -> real domain examples, a fresh one per test, because fake data breaks the mapping to the domain, hides typos and makes tests unreadable; anonymise where regulation forbids real data.
- Recipe 20.9 (p. 324): methods added to a class only so a test can peek inside (a getter for the secret word) -> inject the uncontrolled collaborator (a word randomiser) and test behaviour through the public protocol, because test-only accessors are coupling and open-box tests break on refactoring.
- Recipe 20.10 (p. 326): setup and assertions carrying data irrelevant to the case -> strip to what the assertion needs (setup, exercise, assert), because noise hides the point of the test.
- Recipe 20.11 (p. 328): merge requests without tests for the change -> every change ships with its covering test, because the test is the living specification and the first customer of the code; exception: harness in a separate repository.
- Recipe 20.12 (p. 329): tests asserting against a fixed future date -> remove the date condition and assert the current rule, because a calendar-dependent test will break the pipeline on a day nobody expects.
- Recipe 20.13 (p. 330): starting a new language with a console Hello World -> start with a failing test, because printing to a global console is untestable and sets the wrong habit; UNUSUAL pedagogical stance.

## Chapter 21 -- Technical Debt (p. 333-339)

- Recipe 21.1 (p. 334): ifs on the production environment name -> model environments as polymorphic objects and inject them, because environment ifs are untestable and fail only in production.
- Recipe 21.2 (p. 335): a defect tracker as the engineering backlog of known bugs -> reproduce, cover with a test, fix now, because a tracked defect is debt accruing interest and inability to fix quickly is a process smell; customer-facing trackers are fine. CONTRARIAN.
- Recipe 21.3 (p. 337): warnings or strict mode disabled, especially in production -> enable all warnings and assertions everywhere, because a tolerated warning is where the next failure hides (broken windows).
- Recipe 21.4 (p. 338): TODO and FIXME markers -> do the work now, or in TDD write the failing test instead, because deferred notes are debt and interest; linters count them.

## Chapter 22 -- Exceptions (p. 341-352)

Intro: exceptions separate the happy path from the error path; the author dismisses Go's return-code design as premature optimisation.

- Recipe 22.1 (p. 341): empty catch blocks -> handle or at least log explicitly; if ignoring is intended, say so in code, because swallowing errors is the old on-error-resume-next and hides root causes; linters flag it.
- Recipe 22.2 (p. 342): one exception class per failure with no behaviour difference -> one exception with a description, new classes only when behaviour differs, because empty exception classes are anemic classes polluting the namespace; code/description fields are data, not behaviour. UNUSUAL versus the common one-class-per-error habit.
- Recipe 22.3 (p. 344): exceptions used for expected cases (ending a loop by catching out-of-bounds) -> ordinary control flow, because exceptions are for contract violations and reading them as flow is a goto in disguise.
- Recipe 22.4 (p. 346): nested try/catch -> extract the error-handling policy into its own method or object, because inner handlers bury the happy path.
- Recipe 22.5 (p. 347): status codes returned to your own callers -> raise exceptions, keep codes only at external boundaries (REST), because codes force ifs at every call site and go stale; generic exceptions first, specific ones only when handled differently.
- Recipe 22.6 (p. 349): nested conditions each throwing deeper in (exception arrow code) -> flat guard clauses throwing early, because exceptional code should be shorter than normal code.
- Recipe 22.7 (p. 350): stack traces shown to end users -> a top-level handler that logs and shows a business message, because leaking internals is a security and UX fault.
- Recipe 22.8 (p. 351): wide try blocks covering code that cannot fail -> narrow the try to the statements that can, throw early and catch late, because a broad handler masks which statement failed; mutation testing helps narrow it.

## Chapter 23 -- Metaprogramming (p. 353-362)

Intro: metaprogramming feels like magic and goes through the same hype curve as design patterns, ending in learning to avoid it.

- Recipe 23.1 (p. 354): reflection, dynamic method names, subclass discovery for dispatch -> direct declarative references and dependency inversion (a parsing provider instead of scanning Parser subclasses), because meta-entities do not exist in the domain and dark references defeat search, refactoring and coverage; exception: orthogonal non-business concerns (persistence, serialisation, rendering, tests).
- Recipe 23.2 (p. 357): closures and anonymous functions everywhere -> reify non-trivial ones as named objects (a sorting strategy with a comparator), because lambdas are hard to find, debug, reuse and test; fine for small code blocks and promises.
- Recipe 23.3 (p. 359): preprocessor directives for environment differences -> runtime objects (an environment object with polymorphic behaviour), because compile-time branching is unreadable and undebuggable, and Stroustrup himself regrets the C preprocessor.
- Recipe 23.4 (p. 361): attributes and methods generated at runtime from configuration files -> declare them by hand (or decorate), because generated members are undebuggable, unsearchable and a security hole if the configuration is tainted; ban the generating calls or keep an allow-list.

## Chapter 24 -- Types (p. 363-369)

- Recipe 24.1 (p. 363): checking an argument's class or type (instanceof, typeof, kind) before acting -> send the message and let polymorphism dispatch, because asking who you are instead of what you can do couples to accidental classification; also no checks for undefined, use complete objects and no nulls; the type-check calls are easy to ban by policy.
- Recipe 24.2 (p. 365): relying on truthy and falsy coercion (negating a number, an array, an object) -> booleans only in boolean positions, because coercion hides errors and makes no sense in the domain (what is not-54?); flag single and double negation on non-booleans in review.
- Recipe 24.3 (p. 368): floating point for decimal quantities (0.1 plus 0.2) -> a decimal or fraction type where the language has one, because binary floats misrepresent decimal values and that violates least surprise; hard to detect mechanically.

## Chapter 25 -- Security (p. 371-379)

- Recipe 25.1 (p. 371): unsanitised external input -> validate and clean everything from outside the boundary, plus assertions and invariants on inputs, because injection attacks ride on trusted input; static checks and penetration tests find it.
- Recipe 25.2 (p. 373): sequential ids exposed to the outside -> non-guessable keys (UUIDs) held by a boundary resource object, not by the domain object, because consecutive ids invite scraping and brute force (IDOR), and ids do not belong in the model anyway.
- Recipe 25.3 (p. 375): pulling a package for a trivial function (is-odd) -> write trivial code yourself, depend only on mature packages at pinned versions, because every dependency is coupling, supply-chain risk and architectural weight. Somewhat CONTRARIAN to the reuse-everything trend.
- Recipe 25.4 (p. 376): regular expressions with nested quantifiers -> simpler expressions, timeouts, or plain algorithms, because catastrophic backtracking is a denial-of-service vector (ReDoS) and regexes are hard to read and debug.
- Recipe 25.5 (p. 377): deserialising objects from untrusted sources (pickle) -> treat input as data only, use formats that cannot execute code (JSON), because object deserialisation is remote code execution waiting to happen; linters warn at deserialisation points.

## Back matter (p. 381-409)

Glossary of the terms used (anemic, bijection, essence/accident, fail fast, MAPPER, method object, null object, poltergeist, reification, Yoda condition, and so on), then the index. No new content.

## (a) What the author treats as CENTRAL -- the recurring themes

- The BIJECTION / MAPPER axiom (ch. 2): the model is a partial simulator of reality; each real thing is exactly one object and each object one real thing. Nearly every recipe is justified by pointing at this: nulls, ids, DTOs, helpers, getters, setters, abstract names, Impl suffixes, pattern names, boolean flags all fail because they have no counterpart in the real world. The question the author keeps asking is not "is this clean" but "what in the domain does this stand for".
- ESSENTIAL vs ACCIDENTAL (Brooks): an object's essence is set at birth and never changes; only accidental aspects may vary. This produces: complete constructors (3.7), no setters (3.3, 5.3), immutability by default (ch. 5), state as collection membership (10.3), and the whole essential-vs-accidental if taxonomy of ch. 14.
- BEHAVIOUR over DATA: objects are defined by protocol, never by attributes; attributes arrive only when behaviour needs them (4.8); anemic classes, DTOs, data clumps and primitive obsession are the same disease.
- POLYMORPHISM instead of conditionals: accidental ifs, switches, booleans, type checks, null checks, environment checks and feature flags are all replaced by objects answering the same message (14.1, 14.3, 14.4, 15.1, 21.1, 24.1).
- FAIL FAST: invalid objects must not exist (13.2, 4.6), defaults throw (13.4), magic corrections are refused (6.15), empty catch blocks and empty placeholders are defects (22.1, 19.12).
- SMALL OBJECTS and reification: find the missing concept and give it a class (4.1, 4.2, 4.6, 4.9, 10.7, 17.15, 23.2). The counterweight is Partial: do not model what does not matter (12.6, 17.17, 19.10).
- READABILITY over PERFORMANCE unless measured (ch. 16, 10.4, 16.5); the industry's defaults are inherited from scarcity-era hardware.
- TESTS as the only honest documentation; comments and diagrams rot (8.7, 12.2, 20.11).

## (b) UNUSUAL or CONTRARIAN advice versus common practice

- Getters and setters are bad practice as such, not merely overused (3.5, 3.8, ch. 5 corollaries); even getXXX naming is wrong, the domain word is the method name.
- DTOs should be removed in favour of real objects, proxies and null objects (3.6).
- Null must not exist; even optional chaining and nullish coalescing are smells because they make null livable (15.1, 15.2); absence is modelled as a null object or a zero-or-one collection (15.3).
- Numeric ids inside domain objects are a smell; references, not ids, and opaque keys only at the boundary (16.1, 25.2).
- Static methods are forbidden outside constructors; classes are not namespaces for functions (18.2, 18.4).
- No concrete class may subclass another concrete class: every class is final or abstract (19.7, 19.8); protected attributes are a smell (19.11); nested classes are a smell (19.5).
- Object state belongs in collections, not in a status attribute (10.3).
- Optional/default parameters are a coupling smell (17.7).
- Boolean return values and boolean parameters are suspect in general, because every boolean breeds an if (14.3, 14.11).
- Yoda conditions are wrong, not a defensive virtue (6.11).
- One exception class per failure is anemic overdesign; one class with a message unless behaviour differs (22.2).
- Closures and lambdas beyond trivial size should become named objects (23.2).
- Timestamps should not be used for ordering (4.5); lazy initialisation is a smell (5.5); caches do not belong in domain objects (16.7).
- Business mocks are forbidden; mock only external accidental systems (20.4).
- The first program in a new language should be a failing test, not Hello World (20.13).
- Known-defect trackers as an engineering backlog are debt; fix now (21.2).
- Configuration, settings and feature toggles are a smell to be removed once mature (10.2).
- Diagrams and code annotations as documentation are rejected (12.2); so are versioned method names, TODOs (21.4), and most comments (ch. 8).
- Languages optimised for performance (Go, Rust, C++) are discouraged for business code (16.5); Go's error-return style is called premature optimisation (ch. 22 intro).
- Trivial dependencies should be written by hand, not imported (25.3).

## (c) What the author argues AGAINST

- Treating objects as data holders (anemic models, ERD-driven design, automatic properties, code generators and AI assistants that emit accessors).
- Null in all its forms, sentinels standing for invalid (9999, -1, Null Island), and status codes returned to internal callers.
- Inheritance for code reuse, deep hierarchies, is-a reasoning from data modelling, premature abstraction and premature classification.
- Globals of every kind: singletons, static methods, global functions, global time (now), global settings, god objects, environment ifs, preprocessor directives.
- Metaprogramming, reflection and dynamic member generation in business code.
- Premature optimisation, cleverness, bitwise tricks, micro-benchmark-driven design.
- Comments as a substitute for names and tests; commented-out code; logical-constant debugging hacks.
- Pattern-name-driven design (classes named after Strategy or Composite) and design-pattern cargo cult, singletons chief among them.
- Mocking the domain, weak or erratic tests, test-only accessors, fixed-date tests, placeholder test data.
- Language magic: truthy coercion, silent date normalisation, hoisting, new Array semantics, const that is not immutable.
- Writing code in any natural language but English, mixed case conventions, abbreviations, ownership prefixes, Hungarian-style I/A/Impl affixes.

## Recipes a linter or type checker can enforce mechanically

(The author himself flags most of these as linter-detectable; the tool in parentheses is my mapping.)

- Naming: 7.1 partially (banned-abbreviation list), 7.3 (prefix my), 7.4 (result/theResult), 7.5 (name equals a type), 7.7 (words abstract/base/helper/manager in names), 7.8 (code spell checker, cspell/codespell), 7.9 (attribute carries class-name prefix), 7.10 (I-/A- prefixes), 7.11 (do/basic prefixes), 7.12 (plural class names, needs an inflector), 7.13 (word collection), 7.14 (Impl), 7.16 (parameter repeats class name), 7.17 (project prefix list), 7.18 (identifier data), 6.3 (version suffixes), 6.4 (regex on not-prefixed names), 6.12 (word list), 9.3 (case convention: ESLint/pylint/ruff naming rules), 9.4 (non-English words via dictionary).
- Formatting and standards: 9.1, 9.2 (prettier/black/editorconfig/gofmt), 6.2 (blank lines inside functions: some linters), 11.4 (redundant parentheses: ESLint no-extra-parens, pylint).
- Size thresholds: 11.1 (method length), 11.2 (parameter count: ESLint max-params, pylint too-many-arguments), 11.3 (locals count: pylint too-many-locals), 11.5 (method count), 11.6 (attribute count: pylint too-many-instance-attributes), 11.7 (import count), 14.10 (nesting depth: ESLint max-depth, complexity), 19.1/19.3 (depth of inheritance tree: pylint/SonarQube), 17.3 (class size).
- Mutability and scope: 5.1/5.2 (prefer-const in ESLint; single-assignment detection), 5.4/5.6 (Object.freeze lint rules, readonly in TypeScript), 5.8 (no-use-before-define, strict mode), 13.1 and 6.1 (variable reused with different meaning: partially, via no-param-reassign and type checkers when types differ), 3.10 (pyright strict, TypeScript noImplicitAny, PHP declare strict / Python slots).
- Dead and suspicious code: 8.1 (commented-out code: eslint-plugin, pylint), 8.3 and 14.17 (constant conditions: ESLint no-constant-condition, no-constant-binary-expression), 12.1 and 16.6 (unused code: coverage, vulture, ts-unused-exports), 21.4 (TODO/FIXME counters), 21.3 (strict mode and warnings-as-errors flags), 22.1 (empty catch: ESLint no-empty, pylint), 19.12 (empty method body: partially, false positives), 19.9 (empty class).
- Conditionals: 14.4 (switch count, no-switch rules), 14.6 (bitwise vs logical operators: no-bitwise), 14.9 (no-unused-expressions catches a && b statements), 14.12 (no-unneeded-ternary, comparison with boolean literal: ESLint no-unneeded-ternary, SonarQube), 14.13/14.18 (no-nested-ternary), 14.7 (consistent-return), 13.4 (default-case with throw: partially).
- Types and values: 13.6 (equals/hashCode pair: Java compilers, SpotBugs), 24.1 (ban instanceof/typeof/kind-of calls by rule), 24.2 (strict boolean expressions: TypeScript ESLint strict-boolean-expressions, pylint), 24.3 (partially: ban float in money modules), 20.7 (assertEquals on floats: custom rule), 6.8 (magic numbers: no-magic-numbers), 6.11 (yoda rule in ESLint, set to never).
- Globals and structure: 17.2 (ban getInstance), 18.2 (ban static except constructors: custom rule), 18.3 (goto: language level), 18.5 (ban new Date()/now outside one time source: no-restricted-syntax), 10.8 (no-array-constructor), 15.2 (ban optional chaining and nullish coalescing by syntax rule), 17.10 (default before required parameter: compiler or default-param-last), 12.3/12.4 (single-subclass abstract class, single-implementation interface: IDE inspections), 19.7/19.8 (final-or-abstract check: custom compile rule), 19.11 (protected attribute lint), 19.5 (inner class lint), 23.1/23.4 (ban reflection APIs, eval, setattr), 25.4 (ReDoS detectors such as safe-regex), 25.5 (ban pickle/unserialize on input: bandit, semgrep), 25.1 (taint analysis: semgrep, CodeQL), 25.3 (dependency count and trivial-package allowlists), 16.3 (no-bitwise), 20.3 (assertTrue on a comparison: custom rule), 20.12 (date literal in tests: custom rule), 20.6 partially (flaky-test statistics in CI).

## Recipes that need judgement and could be a yes/no check on a diff

- 3.1/3.8/3.9: does any new public attribute or getXXX expose representation that a behaviour method could hide?
- 3.3/5.3: does the diff add a setter that changes an essential attribute?
- 3.6: does the diff add a class that only mirrors another class's fields?
- 3.7: does any new constructor create an object that is not yet valid?
- 4.1/4.2/4.6/4.7: is a new domain concept passed around as a primitive or a validated string?
- 4.8: is a new attribute added before any behaviour needs it?
- 4.9/17.15: do two or more values always travel together without a wrapping object?
- 5.7: does a new function change state outside its arguments or receiver?
- 6.5/17.8: is new behaviour placed in the object that owns the data it uses?
- 6.7/8.5/8.6/8.7: does a new comment say something a name or a test could say?
- 6.9: does a business rule read in terms of implementation detail rather than domain words?
- 6.14/22.7: does a new error message name the business rule and the action, and never leak internals to the end user?
- 7.2/7.7: does a new class have a name that exists in the domain, not Helper/Manager/Base?
- 7.15: are new parameters named by role rather than position?
- 9.5: do sibling functions in the diff take their parameters in the same order?
- 9.6: did the author clean something adjacent, or leave a known mess?
- 10.1/16.4: is the duplication in the diff essential (same concept) or accidental (looks alike)?
- 10.2/14.16: does the diff add a configuration switch where a polymorphic object would do?
- 10.3: is a new status attribute really state that belongs in a collection?
- 10.4/16.2/16.5/16.7: is any optimisation in the diff backed by a measurement?
- 10.6: does a new call chain reach past direct collaborators?
- 10.7: is a long algorithm a candidate for its own object?
- 10.9/17.9: does a new class only forward to another?
- 11.8: does a new function do two things (name contains and)?
- 11.9: does a new interface force implementors to throw not-supported?
- 12.3/12.4/12.5/19.10: is an abstraction, interface or pattern introduced with only one concrete case?
- 12.6: does a hand-made collection class add behaviour beyond the standard one?
- 13.2: are preconditions and invariants checked where the object is created?
- 13.3: does a new function accept several argument shapes?
- 13.7: does the diff mix a refactoring with a behaviour change?
- 14.1/14.3/14.4: is each new if essential (a domain rule) or accidental (a type/flag/null check)?
- 14.2: is each new boolean flag named for the event it records?
- 14.5: could a ladder of equality tests be a lookup table?
- 14.8/14.11: does a function return a boolean that will only be consumed by another if?
- 14.14: do two new methods do the same thing under different names?
- 14.15: is a comparison repeated across callers that the owning object should perform?
- 15.1/15.3/15.4/15.5: does the diff introduce a null, an optional, or a sentinel where a polymorphic object would do?
- 16.1/25.2: does a domain object hold an id or key?
- 16.8: is a new event named after what happened rather than what the handler does?
- 16.9: does a constructor perform persistence or network work?
- 16.10: does a destructor hold cleanup logic?
- 17.1: does the diff rely on an unstated unit, format or assumption?
- 17.4/17.6: does one requirement change touch several unrelated places?
- 17.7: does a new parameter carry a default value?
- 17.11: does a small change ripple widely (a sign of hidden coupling)?
- 17.12: does a business object gain serialisation, persistence, display or logging code?
- 17.13: is a validation rule added only in the UI?
- 17.14: does a new dependency point at a concrete global class where an interface exists?
- 17.16: do two classes in the diff reach into each other's internals?
- 17.17: does the diff give identity to objects the domain treats as interchangeable?
- 18.1/18.4: does the diff add a free function or use a class as a global entry point?
- 19.2/19.3/19.4: is a new subclass a behaves-as-a relation or reuse by inheritance?
- 19.6: is a new class name meaningful outside its hierarchy?
- 20.1: does the diff open a private method only so a test can reach it?
- 20.2/20.5: do new assertions carry a description and an exact expected value?
- 20.4: does a new test mock a business object?
- 20.8/20.10: does the new test use real domain data and only the data the assertion needs?
- 20.9: does the diff add a method whose only caller is a test?
- 20.11: does every behaviour change in the diff come with a test?
- 21.1: does the diff branch on an environment name?
- 21.2: does the diff log a known defect instead of fixing it?
- 22.2: is a new exception class justified by different handling?
- 22.3: is an exception used for an expected case?
- 22.4/22.6/22.8: is error handling flat, early, and narrow around the statement that can fail?
- 22.5: does an internal API return a status code?
- 23.1/23.2/23.3: does the diff use reflection, a non-trivial lambda, or a preprocessor branch in business code?
- 24.3: does new money or measurement code use binary floats?
- 25.1: is every new external input validated at the boundary?
- 25.3: is a newly added dependency mature and genuinely needed?

## Recipes that duplicate well-known refactoring catalogues (Fowler) with nothing added

6.1, 6.8, 7.4, 7.15, 8.1, 8.5, 8.6, 10.1, 10.6, 10.7, 10.9, 11.1, 11.2, 11.3, 11.5, 11.6, 11.8, 13.1, 14.4, 14.5, 14.8, 14.10, 14.11, 15.1, 17.3, 17.4, 17.6, 17.8, 17.9, 17.15, 17.16, 19.1, 19.2, 19.3, 19.9, 22.3, 22.5.
(10.7 is Beck's method object rather than Fowler's; 14.1 and 14.3 are Fowler's replace-conditional-with-polymorphism but the author adds the essential/accidental test, so they are not listed.)
