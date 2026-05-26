"""Unit tests for Result[T, E] — Ok and Err variants."""

from refined_types import Err, Ok


def test_ok_match_invokes_success() -> None:
    result: Ok[int] = Ok(5)
    out = result.match(lambda v: v * 2, lambda e: 0)
    assert out == 10


def test_err_match_invokes_failure() -> None:
    result: Err[str] = Err("boom")
    out = result.match(lambda v: "no", lambda e: f"got {e}")
    assert out == "got boom"


def test_ok_then_chains() -> None:
    def inc(v: int) -> Ok[int] | Err[str]:
        return Ok(v + 1)

    result = Ok(3).then(inc)
    assert isinstance(result, Ok)
    assert result.value == 4


def test_ok_then_can_fail() -> None:
    def half(v: int) -> Ok[int] | Err[str]:
        if v % 2 == 0:
            return Ok(v // 2)
        return Err("odd")

    assert Ok(4).then(half) == Ok(2)
    assert Ok(5).then(half) == Err("odd")


def test_err_then_short_circuits() -> None:
    called = False

    def f(v: int) -> Ok[int] | Err[str]:
        nonlocal called
        called = True
        return Ok(v)

    result = Err("nope").then(f)
    assert isinstance(result, Err)
    assert result.error == "nope"
    assert called is False


def test_ok_map_transforms_value() -> None:
    assert Ok(3).map(lambda v: v + 1) == Ok(4)


def test_err_map_is_identity() -> None:
    err: Err[str] = Err("x")
    assert err.map(lambda v: v) is err


def test_err_map_err_transforms_error() -> None:
    assert Err("x").map_err(lambda e: e.upper()) == Err("X")


def test_ok_map_err_is_identity() -> None:
    ok: Ok[int] = Ok(1)
    assert ok.map_err(lambda e: e) is ok


def test_ok_and_err_are_distinct_types() -> None:
    assert not isinstance(Ok(1), Err)
    assert not isinstance(Err(1), Ok)


def test_ok_is_frozen() -> None:
    ok = Ok(1)
    try:
        ok.value = 2  # type: ignore[misc]
    except (AttributeError, Exception):
        pass
    else:
        raise AssertionError("Ok must be frozen")
