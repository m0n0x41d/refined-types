"""Enforce CLAUDE.md hard invariant §2.1:

``src/refined_types/_core/`` has zero runtime dependencies beyond
``typing_extensions``. No pydantic, no hypothesis, no attrs, no msgspec.
No import of ``refined_types.pydantic`` or ``refined_types.hypothesis``.

Held statically by walking the AST of every module under ``_core/`` and
inspecting Import / ImportFrom nodes — so an accidental ``import pydantic``
fails CI before runtime ever sees it.
"""

from __future__ import annotations

import ast
from collections.abc import Iterator
from pathlib import Path
from typing import Final

FORBIDDEN_TOP_LEVEL: Final = frozenset({
    "pydantic",
    "hypothesis",
    "attrs",
    "attr",
    "msgspec",
})

FORBIDDEN_PREFIXES: Final = (
    "refined_types.pydantic",
    "refined_types.hypothesis",
    "refined_types.algebra",
)

CORE_ROOT: Final = Path(__file__).parent.parent / "src" / "refined_types" / "_core"


def _core_modules() -> Iterator[Path]:
    yield from sorted(CORE_ROOT.rglob("*.py"))


def _imports(tree: ast.AST) -> Iterator[str]:
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif (
            isinstance(node, ast.ImportFrom)
            and node.module is not None
            and node.level == 0
        ):
            yield node.module


def _is_forbidden(module_name: str) -> bool:
    top = module_name.split(".", 1)[0]
    if top in FORBIDDEN_TOP_LEVEL:
        return True
    return any(module_name.startswith(prefix) for prefix in FORBIDDEN_PREFIXES)


def test_core_root_exists() -> None:
    assert CORE_ROOT.is_dir(), f"_core not found at {CORE_ROOT}"


def test_no_core_module_imports_forbidden_package() -> None:
    offenses: list[str] = []
    for module_path in _core_modules():
        source = module_path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(module_path))
        for imported in _imports(tree):
            if _is_forbidden(imported):
                rel = module_path.relative_to(CORE_ROOT.parent.parent.parent)
                offenses.append(f"{rel}: imports {imported}")
    assert not offenses, (
        "Core layer must not import framework adapters or third-party libs. "
        "Move adapter-specific code into refined_types/<adapter>/.\n  "
        + "\n  ".join(offenses)
    )


def test_core_modules_were_actually_scanned() -> None:
    """Guard against an empty walk silently passing the isolation test."""
    modules = list(_core_modules())
    assert len(modules) >= 4, f"Expected ≥4 _core modules, found {len(modules)}"
