"""Hypothesis strategy registration for refined-types.

Requires hypothesis to be installed::

    pip install "refined-types[hypothesis]"

Lands in 0.3.0. This module currently raises ImportError at import time if
hypothesis is not available, and is otherwise empty.
"""

from importlib.util import find_spec

if find_spec("hypothesis") is None:  # pragma: no cover
    raise ImportError(
        "refined_types.hypothesis requires hypothesis. "
        "Install with: pip install 'refined-types[hypothesis]'"
    )
