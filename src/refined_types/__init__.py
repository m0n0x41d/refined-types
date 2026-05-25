"""refined-types — Annotated-based refinement types for Python.

A practical projection of Σ-types into a language without dependent types:
smart-constructor-only values carrying type-level evidence that a predicate
was checked at the boundary.

The core (this package) is framework-agnostic. Optional integrations live in
subpackages and require their own extras:

- ``refined_types.pydantic``  — needs ``pip install "refined-types[pydantic]"``
- ``refined_types.hypothesis`` — needs ``pip install "refined-types[hypothesis]"``

This is the 0.0.1 placeholder release reserving the package name on PyPI.
The real API lands in 0.1.0.
"""

__version__ = "0.0.1"
__all__ = ["__version__"]
