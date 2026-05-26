"""refined-types — first-class refinement types for Python.

A practical projection of Σ-types into a language without dependent types:
smart-constructor-only values carrying type-level evidence that a predicate
was checked at the boundary.

The core (this package) is framework-agnostic. Optional integrations live in
subpackages and require their own extras:

- ``refined_types.pydantic``  — needs ``pip install "refined-types[pydantic]"``
- ``refined_types.hypothesis`` — needs ``pip install "refined-types[hypothesis]"``

Canonical usage::

    from refined_types import Refined, parse, Positive, Ok, Err

    type Age = Refined[int, Positive]

    match parse(Positive, 5):
        case Ok(value=age):
            ...
        case Err(error=e):
            ...

See ``.context/SPEC.md`` for the full design.
"""

from refined_types._core.parse import parse, try_parse
from refined_types._core.predicate import Predicate
from refined_types._core.predicates import (
    Email,
    MaxLength,
    MinLength,
    Negative,
    NonEmptyCollection,
    NonEmptyString,
    NonNegative,
    NonPositive,
    Positive,
    Sorted,
    Unique,
    Zero,
)
from refined_types._core.refined import ParseError, Refined
from refined_types._core.result import Err, Ok, Result

__version__ = "0.0.1"

__all__ = [
    "Email",
    "Err",
    "MaxLength",
    "MinLength",
    "Negative",
    "NonEmptyCollection",
    "NonEmptyString",
    "NonNegative",
    "NonPositive",
    "Ok",
    "ParseError",
    "Positive",
    "Predicate",
    "Refined",
    "Result",
    "Sorted",
    "Unique",
    "Zero",
    "__version__",
    "parse",
    "try_parse",
]
