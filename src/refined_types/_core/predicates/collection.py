"""Collection predicates: structural checks on iterables.

These predicates apply to anything sized and iterable. Refined collections
with safe methods (``NonEmptyList.head()`` etc.) land in 0.2.0 — for now,
predicate-level refinement is all that's offered.
"""

from collections.abc import Mapping, Sequence, Sized
from typing import Final

from refined_types._core.predicate import Predicate


class NonEmptyCollection(Predicate[Sized]):
    description = "len(c) > 0"

    @classmethod
    def check(cls, value: Sized) -> bool:
        return len(value) > 0

    @classmethod
    def json_schema_constraint(cls) -> Mapping[str, object]:
        return {"minItems": 1}


class Unique(Predicate[Sequence[object]]):
    description = "all elements distinct"

    @classmethod
    def check(cls, value: Sequence[object]) -> bool:
        seen: set[object] = set()
        for item in value:
            if item in seen:
                return False
            seen.add(item)
        return True

    @classmethod
    def json_schema_constraint(cls) -> Mapping[str, object]:
        return {"uniqueItems": True}


class Sorted(Predicate[Sequence[object]]):
    description = "ascending order by <"

    @classmethod
    def check(cls, value: Sequence[object]) -> bool:
        return all(value[i] <= value[i + 1] for i in range(len(value) - 1))  # type: ignore[operator]

    @classmethod
    def json_schema_constraint(cls) -> Mapping[str, object]:
        return {}


__all__: Final = ["NonEmptyCollection", "Sorted", "Unique"]
