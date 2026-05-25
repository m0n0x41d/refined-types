# refined-types

Annotated-based refinement types for Python — with first-class Pydantic v2 integration.
A practical projection of Σ-types into a language without dependent types.

> Status: **0.0.1 — name reservation.** Real API ships in 0.1.0. Star/watch for updates.

## What this is

A small library that gives you first-class **refinement types** — values that
carry, at the type level, the evidence that a predicate was checked at the
boundary. Built around `Annotated[T, Refined[P]]`, with a tiny zero-dependency
core and **optional** integrations for Pydantic v2 and Hypothesis.

```python
# Coming in 0.1.0 — preview only

# 1. Standalone — no pydantic needed
from refined_types import Refined, Positive, NonEmpty, parse

def buy(quantity: Refined[int, Positive], item: Refined[str, NonEmpty]) -> None: ...

match parse(Positive, 5):
    case Ok(qty):   buy(qty, parse(NonEmpty, "apple").unwrap())
    case Err(why):  log.error(why)

# 2. Pydantic v2 — opt-in via `refined-types[pydantic]`
from pydantic import BaseModel
from refined_types import Refined, Range, Email

class User(BaseModel):
    email: Refined[str, Email]
    age:   Refined[int, Range[0, 150]]
```

## Architecture

```
refined_types/
├── _core/          ← zero deps beyond typing_extensions
├── pydantic/       ← optional; needs `refined-types[pydantic]`
└── hypothesis/     ← optional; needs `refined-types[hypothesis]`
```

The **core is framework-agnostic**: works with plain Python, dataclasses,
`attrs`, `msgspec`, or any other modeling layer. Pydantic v2 gets a
first-class adapter — `__get_pydantic_core_schema__` hook + JSON Schema
constraint translation — but it is **not a dependency** of the core.

## Why not `phantom-types`?

[`phantom-types`](https://github.com/antonagestam/phantom-types) is a great
library that occupies this niche. We differ on the axes that matter for
Pydantic-v2-native, type-checker-strict workflows:

| Aspect                             | phantom-types        | refined-types                       |
|------------------------------------|----------------------|--------------------------------------|
| DSL                                | inheritance          | `Annotated[T, Refined[P]]`           |
| Core dependencies                  | typeguard, numerary  | typing-extensions only               |
| Pydantic                           | v1 hook (legacy)     | v2 native (`__get_pydantic_core_schema__`) |
| Type-checker distinctness          | weak (subclass of bound) | strong (NewType-discriminated)   |
| Parse failure                      | raises               | raises **and** `try_parse() -> Result` |
| Predicate algebra                  | functions: `both(p, q)` | operators: `P & Q`                |
| Refined collections safe API       | absent               | `NonEmpty.head() -> T`               |
| Σ-type framing                     | absent               | first-class in docs                  |

## Connection to type theory

In MLTT/HoTT, a Σ-type is `Σ(x : T). P(x)` — a value of type `T` paired with a
proof that `P(x)` holds. In a language without dependent types, we keep the
**shape** of Σ: a smart constructor is the only entry point, and the resulting
type carries (proof-irrelevantly) the witness that the predicate was checked.

This is not full Σ — Python cannot express type-level computation, cross-field
dependent constraints, or proof-relevant equality. But the **discipline** Σ
encourages — parse-don't-validate, illegal states unrepresentable, transport
guarantees through function signatures — is exactly what this library gives.

## Installation

```bash
# Core only — no pydantic, no hypothesis
pip install refined-types

# With Pydantic v2 integration
pip install "refined-types[pydantic]"

# With Hypothesis strategy registration
pip install "refined-types[hypothesis]"

# Everything
pip install "refined-types[all]"
```

## Roadmap

- **0.0.1** — name reservation (you are here)
- **0.1.0** — `Refined[T, P]` core, smart constructors with `Result`, built-in
  numeric/string/collection predicates, Pydantic v2 adapter, JSON Schema
- **0.2.0** — predicate algebra (`&`, `|`, `~`), refined collections with safe API
- **0.3.0** — Hypothesis strategy registration, FastAPI recipes,
  `attrs`/`msgspec` integration examples
- **1.0.0** — stable API, full docs site

## License

MIT — see [LICENSE](LICENSE).
