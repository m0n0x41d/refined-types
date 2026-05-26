"""Refined[T, P] — the phantom marker for a value that passed predicate P.

``Refined`` is a parameterized generic class that is **never instantiated**
for ordinary refinement. ``parse(P, value)`` returns the raw ``value`` cast
to ``Refined[T, P]`` for the type checker; at runtime there is no wrapper,
no allocation, no ``isinstance(x, Refined)`` check that succeeds.

This is the phantom-typing strategy: pyright and mypy distinguish
``Refined[int, Positive]`` from ``Refined[int, Negative]`` and from raw
``int`` in invariant positions, while the runtime representation is exactly
the underlying value. Σ-types projected into a language without dependent
types: the witness lives at the type level and is erased at run-time.

Subclassing ``Refined`` is reserved for L3 refined collections
(``NonEmptyList`` etc., 0.2.0) that need to add safe methods. Ordinary
predicate-based refinement does not require subclassing.

``ParseError`` carries the value that failed and a description of which
predicate rejected it.
"""

from dataclasses import dataclass
from typing import Any, Final, Generic, TypeVar

from refined_types._core.predicate import Predicate

T = TypeVar("T")
P = TypeVar("P", bound=Predicate[Any])


class Refined(Generic[T, P]):
    """Phantom marker. Not instantiated by ``parse``.

    Two ``Refined`` aliases with different ``P`` arguments are distinct
    types to pyright and mypy in invariant positions. A function declared
    ``def f(x: Refined[int, Positive])`` cannot be called with a raw
    ``int`` — the caller must go through ``parse`` or ``try_parse``.

    At runtime, a value of static type ``Refined[T, P]`` is just ``T`` —
    there is no wrapping object. ``isinstance(x, Refined)`` is therefore
    ``False`` for refined values produced by ``parse``. This is intentional
    and documented; if you need to recover ``T``, you already have it.
    """

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)


@dataclass(frozen=True, slots=True)
class ParseError:
    """Carries the rejected value and a human-readable rejection reason.

    Returned inside ``Err`` from ``parse``. ``try_parse`` raises ``ValueError``
    with the same description string.
    """

    value: object
    predicate: str
    description: str

    def __str__(self) -> str:
        return f"value {self.value!r} failed predicate {self.predicate}: {self.description}"


__all__: Final = ["ParseError", "Refined"]
