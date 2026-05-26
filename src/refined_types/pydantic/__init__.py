"""Pydantic v2 integration for refined-types.

Requires pydantic to be installed::

    pip install "refined-types[pydantic]"

Importing this module attaches ``__get_pydantic_core_schema__`` and
``__get_pydantic_json_schema__`` hooks onto ``Refined``, so that
``Refined[T, P]`` works as a field type in pydantic models. The core
(``refined_types._core``) does not depend on pydantic — these hooks are
installed only when this adapter is imported.

The patching is idempotent.
"""

from importlib.util import find_spec

if find_spec("pydantic") is None:  # pragma: no cover
    raise ImportError(
        "refined_types.pydantic requires pydantic v2. "
        "Install with: pip install 'refined-types[pydantic]'"
    )

from refined_types._core.refined import Refined
from refined_types.pydantic._schema import (
    get_refined_core_schema,
    get_refined_json_schema,
)

if not getattr(Refined, "_refined_pydantic_attached", False):
    Refined.__get_pydantic_core_schema__ = classmethod(get_refined_core_schema)  # type: ignore[attr-defined]
    Refined.__get_pydantic_json_schema__ = classmethod(get_refined_json_schema)  # type: ignore[attr-defined]
    Refined._refined_pydantic_attached = True  # type: ignore[attr-defined]
