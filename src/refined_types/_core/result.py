"""Result[T, E] — a minimal bundled Result type for refined-types.

Encoded as a discriminated union ``Ok[T] | Err[E]`` so that pyright and mypy
narrow naturally in ``match``, ``isinstance``, and ``case`` branches without
any plugins. No external dependencies.

The two variants are independent dataclasses; ``Result`` is the type alias
for their union. ``match`` is the recommended consumption pattern because it
is total — both branches must be handled — but ``then`` / ``map`` /
``map_err`` are provided for monadic composition.

Deliberately omitted: ``unwrap`` / ``unwrap_or`` / ``unwrap_or_else``. They
encourage hiding the error path. Use ``match`` and pass an explicit fallback
if you need one. For predicate-style branch checks, use ``isinstance(r, Ok)``
— pyright and mypy narrow on it.
"""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Final, Generic, TypeAlias, TypeVar, final

T = TypeVar("T")
E = TypeVar("E")
U = TypeVar("U")
F = TypeVar("F")
R = TypeVar("R")


@final
@dataclass(frozen=True, slots=True)
class Ok(Generic[T]):
    """The success branch. Carries the produced value."""

    value: T

    def match(
        self,
        on_success: Callable[[T], R],
        on_failure: Callable[[E], R],
    ) -> R:
        del on_failure
        return on_success(self.value)

    def then(self, f: Callable[[T], "Result[U, F]"]) -> "Result[U, F]":
        return f(self.value)

    def map(self, f: Callable[[T], U]) -> "Ok[U]":
        return Ok(f(self.value))

    def map_err(self, _f: Callable[[E], F]) -> "Ok[T]":
        return self


@final
@dataclass(frozen=True, slots=True)
class Err(Generic[E]):
    """The failure branch. Carries the error."""

    error: E

    def match(
        self,
        on_success: Callable[[T], R],
        on_failure: Callable[[E], R],
    ) -> R:
        del on_success
        return on_failure(self.error)

    def then(self, _f: Callable[[T], "Result[U, F]"]) -> "Err[E]":
        return self

    def map(self, _f: Callable[[T], U]) -> "Err[E]":
        return self

    def map_err(self, f: Callable[[E], F]) -> "Err[F]":
        return Err(f(self.error))


Result: TypeAlias = Ok[T] | Err[E]


__all__: Final = ["Err", "Ok", "Result"]
