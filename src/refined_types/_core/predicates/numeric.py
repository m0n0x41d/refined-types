"""Numeric predicates: sign-based classifiers for int and float.

All predicates here check sign relative to zero. Range / interval predicates
land in a later milestone alongside the algebra layer; for 0.1.0 the
shipped numeric set is intentionally minimal but covers the cases that
caused the original primitive-obsession pain (positive counts, non-negative
indices, etc.).
"""

from collections.abc import Mapping
from typing import Final

from refined_types._core.predicate import Predicate

Number = int | float


class Positive(Predicate[Number]):
    description = "x > 0"

    @classmethod
    def check(cls, value: Number) -> bool:
        return value > 0

    @classmethod
    def json_schema_constraint(cls) -> Mapping[str, object]:
        return {"exclusiveMinimum": 0}


class Negative(Predicate[Number]):
    description = "x < 0"

    @classmethod
    def check(cls, value: Number) -> bool:
        return value < 0

    @classmethod
    def json_schema_constraint(cls) -> Mapping[str, object]:
        return {"exclusiveMaximum": 0}


class NonNegative(Predicate[Number]):
    description = "x >= 0"

    @classmethod
    def check(cls, value: Number) -> bool:
        return value >= 0

    @classmethod
    def json_schema_constraint(cls) -> Mapping[str, object]:
        return {"minimum": 0}


class NonPositive(Predicate[Number]):
    description = "x <= 0"

    @classmethod
    def check(cls, value: Number) -> bool:
        return value <= 0

    @classmethod
    def json_schema_constraint(cls) -> Mapping[str, object]:
        return {"maximum": 0}


class Zero(Predicate[Number]):
    description = "x == 0"

    @classmethod
    def check(cls, value: Number) -> bool:
        return value == 0

    @classmethod
    def json_schema_constraint(cls) -> Mapping[str, object]:
        return {"const": 0}


__all__: Final = ["Negative", "NonNegative", "NonPositive", "Positive", "Zero"]
