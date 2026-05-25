"""Hypothesis strategy registration for refined-types.

Requires hypothesis to be installed::

    pip install "refined-types[hypothesis]"

Lands in 0.1.0. This module currently raises ImportError at import time if
hypothesis is not available, and is otherwise empty.
"""

try:
    import hypothesis as _hypothesis  # noqa: F401
except ImportError as _err:  # pragma: no cover
    raise ImportError(
        "refined_types.hypothesis requires hypothesis. "
        "Install with: pip install 'refined-types[hypothesis]'"
    ) from _err
