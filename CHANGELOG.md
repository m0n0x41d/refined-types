# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] — 2026-05-29

First stable release of the 0.1.0 line. All `SPEC.md §11` 0.1.0
definition-of-done items now have shipped evidence in tests. API
surface is the same as `0.1.0a2`; this release records the DoD
verdict and freezes the alpha → stable transition.

### Added
- `tests/test_pydantic_e2e.py::test_json_schema_covers_five_predicate_categories`
  — JSON Schema generation evidence across 7 predicates from all three
  categories (`Positive`, `NonNegative`, `NonEmptyString`, custom
  `MaxLength` subclass, `Email`, `NonEmptyCollection`, `Unique`). Closes
  the last DoD gap from `SPEC.md §11`.

### Documentation
- Test docstring records the documented phantom-typing consequence:
  `MaxLength.of(n)` is the runtime parameterization form and cannot live
  in a type-expression slot; use an explicit subclass with `bound = n`
  there.

### Scope reminder
- Hypothesis adapter remains a stub raising `ImportError`. Full strategy
  registration ships in **0.3.0** per `SPEC.md §11` roadmap, not 0.1.0.

## [0.1.0a2] — 2026-05-26

Docs alpha. No code changes; this release exists to ship an honest
README to PyPI's project page and to record the spec rebaseline.

### Fixed
- README quickstart referenced an API that was never shipped (`Annotated[T, Refined[P]]`, `.unwrap()`, `NonEmpty`, `Range[0, 150]`). Replaced with code that matches the actual 0.1.0a1+ API surface and demonstrates the load-bearing type-checker rejection of raw values where refinements are expected.
- Comparison matrix with phantom-types now distinguishes shipped features from planned ones explicitly.

### Changed
- Spec section `TS.environment-change.002` rebaselined: scoped to `parse` + `pydantic` for 0.1.0a*, with the Hypothesis adapter marked roadmap. `valid_until` shortened so refresh ceremony fires if the Hypothesis adapter slips.

## [0.1.0a1] — 2026-05-26

First alpha of the 0.1.0 line. Pre-release; API surface considered
subject to change up to 0.1.0 stable.

### Added
- **L1 algebraic core**: `Result[T, E]` (Ok/Err discriminated union with `match` / `then` / `map` / `map_err`, no `unwrap` — total handling required), `Refined[T, P]` phantom marker, `ParseError`.
- **L2 predicate machinery**: `Predicate[T_contra]` ABC with `check` / `describe` / `json_schema_constraint`. Pure synchronous predicates, no I/O, no global state.
- **Smart constructors**: `parse(P, value) -> Result[Refined[T, P], ParseError]` and `try_parse(P, value) -> Refined[T, P]` (raises). Both ship on purpose.
- **12 bundled predicates**: numeric (`Positive`, `Negative`, `NonNegative`, `NonPositive`, `Zero`), string (`NonEmptyString`, `MinLength.of(n)`, `MaxLength.of(n)`, `Email`), collection (`NonEmptyCollection`, `Unique`, `Sorted`).
- **Pydantic v2 adapter** (optional extra): refinement-aware `__get_pydantic_core_schema__` hook that wraps the inner-type schema with an after-validator running the predicate, and `__get_pydantic_json_schema__` that emits the predicate's `json_schema_constraint`.
- **Hypothesis adapter** (optional extra): stub that raises `ImportError` with install instructions; full strategy registration lands in a later alpha.
- **Type-checker honesty**: `Refined[T, A]` and `Refined[T, B]` are distinct types under pyright strict and mypy strict in invariant positions; raw `T` is not assignable to `Refined[T, P]`. Guarded by `tests/type_checking/` with `assert_type` and expected-error markers.
- **Dep-isolation guard**: a static AST-walking test rejects any import of pydantic, hypothesis, attrs, or msgspec from `src/refined_types/_core/`. The "zero-deps core" invariant from `CLAUDE.md §2.1` is now a test, not a convention.

### Tooling
- mypy `warn_unused_ignores=true` and pyright `reportUnnecessaryTypeIgnoreComment=error` so the type-system promise cannot silently degrade behind a stale ignore comment. `warn_redundant_casts` was turned off because it conflicted with pyright's check at the pydantic Any-typed boundary.
- CI `enable-cache: false` on the `setup-uv` step — the library does not commit `uv.lock`, and the cache required a checked-in lock to glob against.

### Known gaps (carried to 0.1.0 stable)
- The README "type-checker rejection" example is in this release; it is also the evidence target for `TS.environment-change.001` and needs to stay accurate as the API evolves.
- `TS.environment-change.002` (predicates work in parse / pydantic / hypothesis) overclaims the hypothesis surface — that adapter is a stub in 0.1.0a1.

## [0.0.1] — 2026-05-25

### Added
- Initial PyPI name reservation.
- Project scaffolding, README, MIT license.
- Public placeholder `__version__`.

[Unreleased]: https://github.com/m0n0x41d/refined-types/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/m0n0x41d/refined-types/releases/tag/v0.1.0
[0.1.0a2]: https://github.com/m0n0x41d/refined-types/releases/tag/v0.1.0a2
[0.1.0a1]: https://github.com/m0n0x41d/refined-types/releases/tag/v0.1.0a1
[0.0.1]: https://github.com/m0n0x41d/refined-types/releases/tag/v0.0.1
