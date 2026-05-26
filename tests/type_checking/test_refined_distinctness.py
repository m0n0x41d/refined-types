"""Static type-checking tests for the central library promise:

``Refined[T, A]`` and ``Refined[T, B]`` are distinct types to pyright/mypy
in invariant positions; raw ``T`` is not assignable to ``Refined[T, P]``.

This file is executed under pyright/mypy. The assertions are encoded as
``assert_type`` calls (which both type checkers verify) and as ``# type:
ignore[...]`` markers where we expect the checker to raise.
"""

from typing_extensions import assert_type

from refined_types import Negative, Ok, Positive, Refined, parse


def takes_positive_int(value: Refined[int, Positive]) -> Refined[int, Positive]:
    return value


def takes_negative_int(value: Refined[int, Negative]) -> Refined[int, Negative]:
    return value


def test_parse_return_type_is_refined() -> None:
    result = parse(Positive, 5)
    if isinstance(result, Ok):
        assert_type(result.value, Refined[int, Positive])


def test_refined_positive_is_not_raw_int() -> None:
    # Raw int may not be passed where Refined[int, Positive] is expected.
    takes_positive_int(5)  # type: ignore[arg-type]


def test_refined_positive_and_negative_are_distinct() -> None:
    result = parse(Positive, 5)
    if isinstance(result, Ok):
        # A Refined[int, Positive] must not satisfy Refined[int, Negative].
        takes_negative_int(result.value)  # type: ignore[arg-type]


def test_refined_positive_accepts_parsed_positive() -> None:
    result = parse(Positive, 5)
    if isinstance(result, Ok):
        takes_positive_int(result.value)  # no error expected
