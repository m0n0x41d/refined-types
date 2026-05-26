"""Predicate — the L2 base for refinement checks.

A ``Predicate[T]`` is a pure synchronous classifier of ``T`` values.
Concrete predicates are *classes* (not function instances) so they can carry
identity in the type system and metadata for the algebra layer (0.2.0) and
framework adapters (pydantic, hypothesis).

A predicate exposes three things:

- ``check(value) -> bool`` — the actual classification. Pure, total, no I/O.
- ``describe() -> str`` — a short human-readable form of the constraint,
  used in error messages.
- ``json_schema_constraint() -> Mapping[str, object]`` — JSON Schema
  fragment representing this constraint, merged into the parent schema by
  the pydantic adapter. Predicates with no schema representation return an
  empty mapping.

Predicates are stateless. Subclasses must be declarable with ``class
MyPred(Predicate[int]): ...`` and used as ``parse(MyPred, value)`` — the
class itself is the predicate identity, instances are never required.
"""

from collections.abc import Mapping
from typing import ClassVar, Final, Generic, TypeVar

T_contra = TypeVar("T_contra", contravariant=True)


class Predicate(Generic[T_contra]):
    """Base class for refinement predicates.

    Subclasses override ``check`` (and optionally ``describe`` /
    ``json_schema_constraint``). The class is never instantiated by
    library code — its identity is the type itself.
    """

    description: ClassVar[str] = ""

    @classmethod
    def check(cls, value: T_contra) -> bool:
        raise NotImplementedError(f"{cls.__name__} must override Predicate.check")

    @classmethod
    def describe(cls) -> str:
        return cls.description or cls.__name__

    @classmethod
    def json_schema_constraint(cls) -> Mapping[str, object]:
        return {}


__all__: Final = ["Predicate"]
