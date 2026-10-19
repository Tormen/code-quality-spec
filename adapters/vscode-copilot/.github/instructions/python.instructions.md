---
applyTo: "**/*.py"
---

# Python

<!-- rendered by tools/render-adapters from SPEC.md 4f15993456b9; do not edit here -- edit the spec and re-render -->

## Python

Static typing is enforced by the type checker in strict mode (layer 3), and
the mechanical style checks are a linter's job, not a memory's. Four
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
- **composed** -- inheritance only for a behavioural contract the subclass
  keeps (invariants held, preconditions not strengthened, postconditions
  not weakened); a structural need is a `Protocol`; mixins only, otherwise
  single inheritance; never a subclass of a built-in. A class exists only
  when there is state with an invariant to guard -- otherwise functions in
  a module.
  *Test:* every new subclass "behaves as" its parent; every new class
  guards an invariant.

A failure is raised as the tool's one root exception carrying its code
(see "failure"), chained with `raise ... from e`; `except Exception` exists
at the top of `main` (where it becomes the one-line ERROR and the trace
file) and where a foreign library's failures are turned into that root
exception, nowhere else. A tool with third-party dependencies creates its
own virtual environment on first run and re-executes itself inside it,
saying so in one line.


## Mechanical checks (the linter and the type checker decide these)

ruff: `BLE001` blind except, `FBT001`/`FBT002` positional boolean, `B006` mutable default, `ANN401` `Any`, plus the project's selected rule set
