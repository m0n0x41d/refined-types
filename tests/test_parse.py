"""Unit tests for parse / try_parse — the smart constructors."""

from typing import cast

import pytest

from refined_types import (
    Email,
    Err,
    Negative,
    NonEmptyString,
    Ok,
    ParseError,
    Positive,
    Unique,
    parse,
    try_parse,
)


def test_parse_ok_on_passing_value() -> None:
    result = parse(Positive, 5)
    assert isinstance(result, Ok)
    assert cast(int, result.value) == 5


def test_parse_err_on_failing_value() -> None:
    result = parse(Positive, -1)
    assert isinstance(result, Err)
    assert result.error.predicate == "Positive"
    assert "Positive" in str(result.error)


def test_parse_err_carries_failed_value() -> None:
    result = parse(Negative, 0)
    assert isinstance(result, Err)
    assert result.error.value == 0


def test_try_parse_returns_value_on_success() -> None:
    value = try_parse(Positive, 7)
    assert cast(int, value) == 7


def test_try_parse_raises_on_failure() -> None:
    with pytest.raises(ValueError, match="Positive"):
        try_parse(Positive, -1)


def test_parse_string_predicate() -> None:
    result = parse(NonEmptyString, "hello")
    assert isinstance(result, Ok)
    assert parse(NonEmptyString, "").match(lambda _v: False, lambda _e: True) is True


def test_parse_email() -> None:
    assert isinstance(parse(Email, "a@b.co"), Ok)
    assert isinstance(parse(Email, "not-an-email"), Err)


def test_parse_unique() -> None:
    assert isinstance(parse(Unique, [1, 2, 3]), Ok)
    assert isinstance(parse(Unique, [1, 2, 1]), Err)


def test_parse_error_is_frozen() -> None:
    result = parse(Positive, -1)
    assert isinstance(result, Err)
    err: ParseError = result.error
    try:
        err.value = 99  # type: ignore[misc]
    except (AttributeError, Exception):
        pass
    else:
        raise AssertionError("ParseError must be frozen")


def test_refined_value_is_raw_value_at_runtime() -> None:
    """D6: pure phantom — refined value is the underlying T at runtime."""
    from refined_types import Refined

    result = parse(Positive, 42)
    assert isinstance(result, Ok)
    refined = result.value
    raw = cast(int, refined)
    assert raw == 42
    assert type(raw) is int
    assert not isinstance(refined, Refined)
