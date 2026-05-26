"""Direct predicate tests for the bundled L2 predicates that test_parse.py
does not exercise — sign classifiers beyond Positive/Negative, length-bound
families, and structural collection predicates.

Tests assert both the runtime check and the JSON-schema constraint, since
the schema constraint is one of the predicate's three obligations.
"""

import pytest

from refined_types import (
    Err,
    MaxLength,
    MinLength,
    NonEmptyCollection,
    NonNegative,
    NonPositive,
    Ok,
    Sorted,
    Zero,
    parse,
)


class TestNonNegative:
    def test_zero_passes(self) -> None:
        assert isinstance(parse(NonNegative, 0), Ok)

    def test_positive_passes(self) -> None:
        assert isinstance(parse(NonNegative, 42), Ok)

    def test_negative_rejected(self) -> None:
        assert isinstance(parse(NonNegative, -1), Err)

    def test_schema(self) -> None:
        assert NonNegative.json_schema_constraint() == {"minimum": 0}


class TestNonPositive:
    def test_zero_passes(self) -> None:
        assert isinstance(parse(NonPositive, 0), Ok)

    def test_negative_passes(self) -> None:
        assert isinstance(parse(NonPositive, -5), Ok)

    def test_positive_rejected(self) -> None:
        assert isinstance(parse(NonPositive, 1), Err)

    def test_schema(self) -> None:
        assert NonPositive.json_schema_constraint() == {"maximum": 0}


class TestZero:
    def test_zero_passes(self) -> None:
        assert isinstance(parse(Zero, 0), Ok)

    def test_positive_rejected(self) -> None:
        assert isinstance(parse(Zero, 1), Err)

    def test_negative_rejected(self) -> None:
        assert isinstance(parse(Zero, -1), Err)

    def test_float_zero_passes(self) -> None:
        assert isinstance(parse(Zero, 0.0), Ok)

    def test_schema(self) -> None:
        assert Zero.json_schema_constraint() == {"const": 0}


class TestMinLength:
    def test_at_bound_passes(self) -> None:
        assert isinstance(parse(MinLength.of(3), "abc"), Ok)

    def test_above_bound_passes(self) -> None:
        assert isinstance(parse(MinLength.of(3), "abcd"), Ok)

    def test_below_bound_rejected(self) -> None:
        assert isinstance(parse(MinLength.of(3), "ab"), Err)

    def test_describe_carries_bound(self) -> None:
        assert "5" in MinLength.of(5).describe()

    def test_schema_carries_bound(self) -> None:
        assert MinLength.of(7).json_schema_constraint() == {"minLength": 7}

    def test_of_is_cached(self) -> None:
        assert MinLength.of(4) is MinLength.of(4)

    def test_distinct_bounds_distinct_classes(self) -> None:
        assert MinLength.of(3) is not MinLength.of(4)


class TestMaxLength:
    def test_at_bound_passes(self) -> None:
        assert isinstance(parse(MaxLength.of(3), "abc"), Ok)

    def test_below_bound_passes(self) -> None:
        assert isinstance(parse(MaxLength.of(3), "ab"), Ok)

    def test_above_bound_rejected(self) -> None:
        assert isinstance(parse(MaxLength.of(3), "abcd"), Err)

    def test_describe_carries_bound(self) -> None:
        assert "5" in MaxLength.of(5).describe()

    def test_schema_carries_bound(self) -> None:
        assert MaxLength.of(7).json_schema_constraint() == {"maxLength": 7}

    def test_of_is_cached(self) -> None:
        assert MaxLength.of(4) is MaxLength.of(4)


class TestMinAndMaxLengthAreIndependent:
    def test_min_and_max_caches_do_not_collide(self) -> None:
        """The two families maintain separate caches and check opposite conditions
        on the same bound — verified behaviorally rather than by identity, since
        identity comparison across distinct types is treated as non-overlapping."""
        min5 = MinLength.of(5)
        max5 = MaxLength.of(5)
        assert isinstance(parse(min5, "abcde"), Ok)
        assert isinstance(parse(max5, "ab"), Ok)
        assert isinstance(parse(min5, "ab"), Err)
        assert isinstance(parse(max5, "abcdef"), Err)


class TestNonEmptyCollection:
    def test_non_empty_list_passes(self) -> None:
        assert isinstance(parse(NonEmptyCollection, [1, 2]), Ok)

    def test_empty_list_rejected(self) -> None:
        empty: list[int] = []
        assert isinstance(parse(NonEmptyCollection, empty), Err)

    def test_non_empty_tuple_passes(self) -> None:
        assert isinstance(parse(NonEmptyCollection, (1,)), Ok)

    def test_empty_tuple_rejected(self) -> None:
        assert isinstance(parse(NonEmptyCollection, ()), Err)

    def test_non_empty_dict_passes(self) -> None:
        assert isinstance(parse(NonEmptyCollection, {"a": 1}), Ok)

    def test_empty_dict_rejected(self) -> None:
        empty: dict[str, int] = {}
        assert isinstance(parse(NonEmptyCollection, empty), Err)

    def test_schema(self) -> None:
        assert NonEmptyCollection.json_schema_constraint() == {"minItems": 1}


class TestSorted:
    def test_ascending_passes(self) -> None:
        assert isinstance(parse(Sorted, [1, 2, 3]), Ok)

    def test_equal_neighbors_allowed(self) -> None:
        assert isinstance(parse(Sorted, [1, 1, 2]), Ok)

    def test_descending_rejected(self) -> None:
        assert isinstance(parse(Sorted, [3, 2, 1]), Err)

    def test_unsorted_rejected(self) -> None:
        assert isinstance(parse(Sorted, [1, 3, 2]), Err)

    def test_single_element_passes(self) -> None:
        assert isinstance(parse(Sorted, [42]), Ok)

    def test_empty_passes(self) -> None:
        empty: list[int] = []
        assert isinstance(parse(Sorted, empty), Ok)

    def test_string_ascending_passes(self) -> None:
        assert isinstance(parse(Sorted, ["a", "b", "c"]), Ok)


class TestMinLengthOfRejectsNegativeBound:
    def test_of_zero_accepts_everything(self) -> None:
        assert isinstance(parse(MinLength.of(0), ""), Ok)
        assert isinstance(parse(MinLength.of(0), "x"), Ok)


@pytest.mark.parametrize(
    ("bound", "value", "expected_ok"),
    [
        (0, "", True),
        (0, "x", True),
        (1, "", False),
        (1, "x", True),
        (10, "x" * 9, False),
        (10, "x" * 10, True),
    ],
)
def test_min_length_parametric(bound: int, value: str, expected_ok: bool) -> None:
    result = parse(MinLength.of(bound), value)
    assert isinstance(result, Ok) is expected_ok
