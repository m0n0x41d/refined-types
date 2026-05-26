"""Built-in L2 predicates: pure synchronous classifiers shipped with the library.

These are the predicates a user gets without writing any of their own. They
are organized by the domain they classify — numbers, strings, collections —
and re-exported here for the public surface.

All predicates here are stateless classes inheriting ``Predicate`` and are
referenced by class identity, not instance.
"""

from refined_types._core.predicates.collection import NonEmptyCollection, Sorted, Unique
from refined_types._core.predicates.numeric import (
    Negative,
    NonNegative,
    NonPositive,
    Positive,
    Zero,
)
from refined_types._core.predicates.string import Email, MaxLength, MinLength, NonEmptyString

__all__ = [
    "Email",
    "MaxLength",
    "MinLength",
    "Negative",
    "NonEmptyCollection",
    "NonEmptyString",
    "NonNegative",
    "NonPositive",
    "Positive",
    "Sorted",
    "Unique",
    "Zero",
]
