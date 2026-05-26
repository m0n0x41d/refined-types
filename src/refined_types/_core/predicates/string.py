"""String predicates: emptiness, length, and the obvious format check.

``MinLength`` and ``MaxLength`` are families of predicates parameterized by
an integer bound. Because we cannot put runtime values into types in stock
Python, each bound is its own subclass — produced by ``MinLength.of(n)`` /
``MaxLength.of(n)``. Cached for identity so repeated calls with the same
``n`` return the same class.

``Email`` uses a deliberately permissive regex — enough to reject obviously
broken inputs without claiming RFC 5322 compliance. Users who need
strictness should write their own predicate.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import ClassVar, Final

from refined_types._core.predicate import Predicate


class NonEmptyString(Predicate[str]):
    description = "len(s) > 0"

    @classmethod
    def check(cls, value: str) -> bool:
        return len(value) > 0

    @classmethod
    def json_schema_constraint(cls) -> Mapping[str, object]:
        return {"minLength": 1}


class MinLength(Predicate[str]):
    """Family of predicates parameterized by minimum length.

    Use ``MinLength.of(n)`` to obtain the predicate class for bound ``n``.
    Direct subclasses must set ``bound`` as a class variable.
    """

    bound: ClassVar[int] = 0
    _cache: ClassVar[dict[int, type[MinLength]]] = {}

    @classmethod
    def check(cls, value: str) -> bool:
        return len(value) >= cls.bound

    @classmethod
    def describe(cls) -> str:
        return f"len(s) >= {cls.bound}"

    @classmethod
    def json_schema_constraint(cls) -> Mapping[str, object]:
        return {"minLength": cls.bound}

    @classmethod
    def of(cls, n: int) -> type[MinLength]:
        cached = cls._cache.get(n)
        if cached is not None:
            return cached
        subclass = type(f"MinLength_{n}", (cls,), {"bound": n})
        cls._cache[n] = subclass
        return subclass


class MaxLength(Predicate[str]):
    """Family of predicates parameterized by maximum length."""

    bound: ClassVar[int] = 0
    _cache: ClassVar[dict[int, type[MaxLength]]] = {}

    @classmethod
    def check(cls, value: str) -> bool:
        return len(value) <= cls.bound

    @classmethod
    def describe(cls) -> str:
        return f"len(s) <= {cls.bound}"

    @classmethod
    def json_schema_constraint(cls) -> Mapping[str, object]:
        return {"maxLength": cls.bound}

    @classmethod
    def of(cls, n: int) -> type[MaxLength]:
        cached = cls._cache.get(n)
        if cached is not None:
            return cached
        subclass = type(f"MaxLength_{n}", (cls,), {"bound": n})
        cls._cache[n] = subclass
        return subclass


_EMAIL_RE: Final = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


class Email(Predicate[str]):
    description = "matches a basic email shape"

    @classmethod
    def check(cls, value: str) -> bool:
        return _EMAIL_RE.match(value) is not None

    @classmethod
    def json_schema_constraint(cls) -> Mapping[str, object]:
        return {"format": "email"}


__all__: Final = ["Email", "MaxLength", "MinLength", "NonEmptyString"]
