"""parse / try_parse — the only legal smart constructors for ``Refined``.

``parse(P, value)`` returns ``Result[Refined[T, P], ParseError]``. Never
raises on predicate failure. This is the canonical entry point for
functional control flow.

``try_parse(P, value)`` raises ``ValueError`` on predicate failure and
returns the refined value directly. Useful at exception-based boundaries
(e.g. inside pydantic validators, where raising is the convention).

Both functions are the *only* legal way to produce a value of type
``Refined[T, P]``. Casting around is technically possible in Python but is
a discipline violation — like any phantom-typing system, the guarantee is
"if you only construct through the smart constructor, the type tells the
truth".

At runtime, ``parse(P, value)`` produces the raw ``value`` itself (typed as
``Refined[T, P]`` for the type checker). No wrapping, no allocation beyond
the ``Ok`` envelope.
"""

from typing import Any, Final, TypeVar, cast

from refined_types._core.predicate import Predicate
from refined_types._core.refined import ParseError, Refined
from refined_types._core.result import Err, Ok, Result

T = TypeVar("T")
P = TypeVar("P", bound=Predicate[Any])


def parse(predicate: type[P], value: T) -> Result[Refined[T, P], ParseError]:
    """Smart constructor. Returns ``Ok(refined)`` on success, ``Err(ParseError)`` on failure.

    Never raises on predicate failure. Predicate exceptions (which are a
    bug — predicates must be total) propagate.
    """
    if predicate.check(value):
        return Ok(cast(Refined[T, P], value))
    return Err(
        ParseError(
            value=value,
            predicate=predicate.__name__,
            description=predicate.describe(),
        )
    )


def try_parse(predicate: type[P], value: T) -> Refined[T, P]:
    """Same as ``parse`` but raises ``ValueError`` on failure.

    For exception-based call sites such as pydantic validators or
    constructors that already raise. Prefer ``parse`` in functional code.
    """
    if predicate.check(value):
        return cast(Refined[T, P], value)
    raise ValueError(
        f"value {value!r} failed predicate {predicate.__name__}: {predicate.describe()}"
    )


__all__: Final = ["parse", "try_parse"]
