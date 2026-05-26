# refined-types

First-class refinement types for Python — with native Pydantic v2
integration. A practical projection of Σ-types into a language without
dependent types.

> Status: **0.1.0a1 — first alpha.** Core, predicates, and the Pydantic v2
> adapter are live; Hypothesis strategy registration is a stub and lands
> in a later alpha. Not for production yet.

## What it gives you

A `Refined[T, P]` value is a `T` that has been checked against predicate `P`
at a parse boundary, with that evidence preserved by the type checker.
Downstream code does not re-validate; it cannot accidentally accept an
unrefined `T` either. The discipline is Σ-type-shaped: a smart
constructor is the only way in, the witness is phantom (erased at
runtime, distinct at the type level), and the refinement transports
through function signatures.

## Quickstart

```python
from refined_types import (
    Err, NonEmptyString, Ok, Positive, Refined, parse, try_parse,
)

# 1. Smart-constructor flow — total handling via Result
match parse(Positive, 5):
    case Ok(value=qty):
        ...  # qty: Refined[int, Positive]
    case Err(error=e):
        print(e)  # value -1 failed predicate Positive: x > 0

# 2. Ergonomic flow when failure is a bug — raise on the spot
qty = try_parse(Positive, 5)        # qty: Refined[int, Positive]

# 3. Functions can demand refined inputs
def buy(qty: Refined[int, Positive], item: Refined[str, NonEmptyString]) -> None:
    ...

buy(qty, try_parse(NonEmptyString, "apple"))   # ok
buy(5, "apple")                                # type-checker rejects
#   ^^^ Argument of type "int" cannot be assigned to parameter "qty"
#       of type "Refined[int, Positive]" in function "buy"
```

The last call site is the load-bearing one: `Refined[int, Positive]` and
plain `int` are distinct types under pyright strict and mypy strict in
invariant positions. The library's main promise is that you cannot
silently bypass the predicate by handing a function a raw value — that
is enforced statically, before any code runs.

## Pydantic v2 integration

Optional via `pip install "refined-types[pydantic]"`. Importing the
adapter installs schema-generation hooks; the core stays free of any
pydantic import.

```python
import refined_types.pydantic  # side-effect: install pydantic hooks
from pydantic import BaseModel
from refined_types import Email, NonEmptyString, Positive, Refined

class User(BaseModel):
    name:  Refined[str, NonEmptyString]
    age:   Refined[int, Positive]
    email: Refined[str, Email]

user = User.model_validate({"name": "Ada", "age": 30, "email": "a@b.co"})
# user.age is typed Refined[int, Positive], not int — see tests/test_pydantic_e2e.py
```

The emitted JSON Schema carries the predicate's constraints:

```python
User.model_json_schema()["properties"]["age"]   # {"exclusiveMinimum": 0, ...}
User.model_json_schema()["properties"]["name"]  # {"minLength": 1, ...}
```

We instantiate via `model_validate({...})` rather than `User(name=...,
age=30, ...)` because the latter would require the caller to hand pydantic
an unrefined `int` for a `Refined[int, Positive]` field — and the type
checker correctly refuses. That refusal is the value prop, not a quirk.

## Architecture

```
refined_types/
├── _core/          ← L1 + L2. Zero deps beyond typing_extensions.
├── pydantic/       ← L4 adapter. Optional via [pydantic] extra.
└── hypothesis/     ← L4 adapter stub. Strategy registration in a later alpha.
```

The core is framework-agnostic: it works with plain Python, dataclasses,
`attrs`, `msgspec`, or any modeling layer. Adapters are isolated modules
that import the core plus their framework and nothing else. A static
test under `tests/test_core_isolation.py` enforces that `_core/` never
imports pydantic, hypothesis, attrs, or msgspec.

## What ships in 0.1.0a1

- **Core**: `Result[T, E]` (Ok/Err discriminated union with `match` / `then` /
  `map` / `map_err`), `Refined[T, P]` phantom marker, `ParseError`.
- **Predicates**: `Positive`, `Negative`, `NonNegative`, `NonPositive`,
  `Zero`, `NonEmptyString`, `MinLength.of(n)`, `MaxLength.of(n)`, `Email`,
  `NonEmptyCollection`, `Unique`, `Sorted`. Twelve in total.
- **Parse**: `parse(P, value) -> Result[Refined[T, P], ParseError]` and
  `try_parse(P, value) -> Refined[T, P]` (raises). Both ship on purpose —
  `parse` for total handling, `try_parse` for ergonomic call sites where a
  failure is a bug.
- **Pydantic v2 adapter** (optional extra): refinement-aware
  `__get_pydantic_core_schema__` + JSON Schema constraint emission.
- **Hypothesis adapter**: stub that raises `ImportError` with install
  instructions. Strategy registration lands in a later alpha.

## Why not `phantom-types`?

[`phantom-types`](https://github.com/antonagestam/phantom-types) is the
incumbent and a good library. We differ on axes that matter for
Pydantic-v2-native, type-checker-strict workflows:

| Aspect                          | phantom-types         | refined-types (0.1.0a1)            |
|---------------------------------|-----------------------|------------------------------------|
| DSL                             | inheritance           | `Refined[T, P]` generic            |
| Core dependencies               | typeguard, numerary   | typing-extensions only             |
| Pydantic                        | v1 hook (legacy)      | v2 native, schema-aware             |
| Type-checker distinctness       | weak (subclass of T)  | strong (distinct in invariant slot) |
| Parse failure                   | raises only           | `parse → Result` **and** `try_parse → raise` |
| Predicate algebra               | functions: `both(p,q)`| planned: operators `P & Q` (0.2.0) |
| Refined collections safe API    | absent                | planned (0.2.0)                    |
| Σ-type framing                  | absent                | first-class in docs                |

Honest scope: anything marked "planned" is not in 0.1.0a1.

## Σ-type framing — one paragraph

In MLTT/HoTT a Σ-type is `Σ(x : T). P(x)` — a value of `T` paired with a
proof that `P` holds. Python has no dependent types, so we keep the
**shape** of Σ rather than its full power: a smart constructor is the only
entry, the witness is phantom (erased at runtime, distinct at the type
level), and the refinement transports through function signatures.
Cross-field dependent constraints, proof-relevant equality, type-level
computation — none of that. The discipline Σ encourages — parse-don't-
validate, illegal states unrepresentable, transport through types — is
exactly what this library gives. See `.context/SPEC.md §8` for the longer
discussion.

## Installation

```bash
# Core only — no pydantic, no hypothesis
pip install "refined-types==0.1.0a1"

# With Pydantic v2 integration
pip install "refined-types[pydantic]==0.1.0a1"

# Hypothesis extra installs hypothesis but the adapter is a stub for now
pip install "refined-types[hypothesis]==0.1.0a1"

# Everything
pip install "refined-types[all]==0.1.0a1"
```

Minimum Python: **3.10**.

## Roadmap

- **0.1.0a1** — first alpha (you are here): core, 12 predicates, pydantic v2 adapter, type-check guards
- **0.1.0 (stable)** — README example verified, spec carriers closed, real Hypothesis strategy or explicit defer
- **0.2.0** — predicate algebra (`&`, `|`, `~`), refined collections with safe API (`NonEmptyList.head() -> T`)
- **0.3.0** — Hypothesis strategy registration (if not in 0.1.0), FastAPI recipes, `attrs`/`msgspec` integration examples
- **1.0.0** — stable API, full docs site

## License

MIT — see [LICENSE](LICENSE).
