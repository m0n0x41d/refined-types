"""E2E test for the pydantic v2 adapter.

A full flow: import the adapter (which attaches hooks onto Refined), declare
a pydantic model whose field is Refined[T, P], validate good and bad
inputs, and inspect the generated JSON Schema.

Note: we use ``User.model_validate({...})`` instead of ``User(age=30, ...)``
because pyright (correctly) refuses to assign raw ``int`` to a parameter
typed ``Refined[int, Positive]``. The point of the library is precisely
this static refusal. ``model_validate`` is pydantic's canonical
runtime-validation entry point.
"""

# pyright: reportUnusedImport=false

from typing import cast

import pytest
from pydantic import BaseModel, ValidationError
from typing_extensions import assert_type

import refined_types.pydantic  # noqa: F401  — side-effect: install hooks
from refined_types import NonEmptyString, Positive, Refined


class User(BaseModel):
    age: Refined[int, Positive]
    name: Refined[str, NonEmptyString]


def takes_positive_int(value: Refined[int, Positive]) -> Refined[int, Positive]:
    return value


def takes_non_empty_string(value: Refined[str, NonEmptyString]) -> Refined[str, NonEmptyString]:
    return value


def test_model_accepts_valid_input() -> None:
    user = User.model_validate({"age": 30, "name": "Ada"})
    assert cast(int, user.age) == 30
    assert cast(str, user.name) == "Ada"


def test_validated_field_is_typed_as_refined() -> None:
    """TS.environment-change.003 evidence: the refinement survives model_validate
    at the type level — pyright/mypy must see user.age as Refined[int, Positive],
    not as int. A function expecting Refined[int, Positive] accepts user.age
    without a cast."""
    user = User.model_validate({"age": 30, "name": "Ada"})
    assert_type(user.age, Refined[int, Positive])
    assert_type(user.name, Refined[str, NonEmptyString])
    takes_positive_int(user.age)
    takes_non_empty_string(user.name)


def test_model_rejects_failing_predicate() -> None:
    with pytest.raises(ValidationError) as exc_info:
        User.model_validate({"age": 0, "name": "Ada"})
    assert "Positive" in str(exc_info.value)


def test_model_rejects_failing_string_predicate() -> None:
    with pytest.raises(ValidationError) as exc_info:
        User.model_validate({"age": 30, "name": ""})
    assert "NonEmptyString" in str(exc_info.value)


def test_json_schema_carries_predicate_constraints() -> None:
    schema = User.model_json_schema()
    props = schema["properties"]
    assert props["age"].get("exclusiveMinimum") == 0
    assert props["name"].get("minLength") == 1


def test_model_dump_returns_underlying_value() -> None:
    user = User.model_validate({"age": 30, "name": "Ada"})
    dump = cast(dict[str, object], user.model_dump())
    assert dump == {"age": 30, "name": "Ada"}


def test_validation_underlying_type_still_enforced() -> None:
    """Predicate runs after T-level validation; T-violations surface as usual."""
    with pytest.raises(ValidationError):
        User.model_validate({"age": "not an int", "name": "Ada"})
