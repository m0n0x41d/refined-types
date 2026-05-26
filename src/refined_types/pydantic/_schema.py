"""Pydantic v2 schema generation for ``Refined[T, P]``.

This module is loaded only when ``refined_types.pydantic`` is imported, and
only when pydantic itself is available. The core (``_core/``) does not
reach into pydantic — instead, ``refined_types.pydantic.__init__`` attaches
the hooks defined here onto ``Refined`` at adapter-import time.

Strategy:

1. Pydantic encounters ``Refined[int, Positive]`` as a field type. The
   origin is ``Refined``, so pydantic calls
   ``Refined.__get_pydantic_core_schema__`` (which we set in __init__.py).
2. We extract ``(T, P)`` from the parameterized generic, generate
   pydantic's schema for ``T`` via the handler, then wrap it in an
   after-validator that calls ``P.check`` and raises on failure.
3. For JSON Schema generation, we attach ``__get_pydantic_json_schema__``
   to merge the predicate's ``json_schema_constraint`` into the parent
   schema.

We deliberately do NOT raise here if the type-args extraction fails —
falling back to the inner type's schema is a safer default for unusual
generic shapes (subclasses of Refined for collections, for example).
"""

from __future__ import annotations

from typing import Any, cast, get_args

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, core_schema

from refined_types._core.predicate import Predicate

_METADATA_KEY = "refined_types.predicate"


def get_refined_core_schema(
    cls: type,
    source_type: Any,
    handler: GetCoreSchemaHandler,
) -> CoreSchema:
    """Hook attached to ``Refined.__get_pydantic_core_schema__``."""
    del cls
    args = get_args(source_type)
    if len(args) != 2:
        return handler(source_type)
    inner_type, predicate_raw = args
    if not (isinstance(predicate_raw, type) and issubclass(predicate_raw, Predicate)):
        return handler(inner_type)
    predicate_cls = cast(type[Predicate[Any]], predicate_raw)
    base = handler.generate_schema(inner_type)
    return core_schema.no_info_after_validator_function(
        _build_validator(predicate_cls),
        base,
        metadata={_METADATA_KEY: predicate_cls},
    )


def get_refined_json_schema(
    cls: type,
    schema: CoreSchema,
    handler: GetJsonSchemaHandler,
) -> JsonSchemaValue:
    """Hook attached to ``Refined.__get_pydantic_json_schema__``."""
    del cls
    json_schema = handler(schema)
    predicate_cls = _extract_predicate(schema)
    if predicate_cls is not None:
        json_schema.update(dict(predicate_cls.json_schema_constraint()))
    return json_schema


def _build_validator(predicate_cls: type[Predicate[Any]]) -> Any:
    def validator(value: Any) -> Any:
        if predicate_cls.check(value):
            return value
        raise ValueError(
            f"value {value!r} failed predicate {predicate_cls.__name__}: {predicate_cls.describe()}"
        )

    return validator


def _extract_predicate(schema: CoreSchema) -> type[Predicate[Any]] | None:
    metadata = schema.get("metadata")
    if not isinstance(metadata, dict):
        return None
    pred = metadata.get(_METADATA_KEY)
    if isinstance(pred, type) and issubclass(pred, Predicate):
        return cast(type[Predicate[Any]], pred)
    return None
