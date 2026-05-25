"""Pydantic v2 integration for refined-types.

Requires pydantic to be installed::

    pip install "refined-types[pydantic]"

Lands in 0.1.0. This module currently raises ImportError at import time if
pydantic is not available, and is otherwise empty.
"""

try:
    import pydantic as _pydantic  # noqa: F401
except ImportError as _err:  # pragma: no cover
    raise ImportError(
        "refined_types.pydantic requires pydantic v2. "
        "Install with: pip install 'refined-types[pydantic]'"
    ) from _err
