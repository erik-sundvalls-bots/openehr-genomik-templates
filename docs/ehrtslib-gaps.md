# Ehrtslib vs Archie: ADL2 → ADL 1.4 gaps

*Tested 2026-10-15 (Europe/Stockholm), ehrtslib commit `7dfd54b`, Deno 2.x. Script: `tools/ehrtslib-down14.ts` (`parseAdl` + `ADL14Serializer`).*

## Context
Archie 3.21 converts only ADL 1.4 → 2; it has no 2 → 1.4 path. Ehrtslib's `ADL14Serializer` is the only down-converter available, so it was tried on our 5 ADL2 artefacts (3 drafts + T1/T2). The 1.4 output was then checked with Archie `parse14`.

## Result: 0/5 usable
All 5 "succeeded" with no exception, but every output is invalid ADL 1.4. Archie `parse14` rejects all of them.

| # | Gap | Evidence |
|---|-----|----------|
| G1 | **cADL parser fails on valid ADL2 that Archie accepts.** The error goes into `warnings`, not `errors`, and `definition` ends up empty. | Draft: `cADL parse error at line 56, column 23: Unexpected token: matches` (`items cardinality matches {1..*; unordered} matches {`). Archie-generated CKM `organisation.v1.0.4.adls`: `Expected archetype id constraint` (slot regex `archetype_id/value matches {/…/}`) |
| G2 | **Serializer writes `definition undefined[undefined]`** when the definition is empty, instead of failing. | All 5 outputs |
| G3 | **Missing `concept` section** in the 1.4 header. | Archie: `expecting {'concept', SYM_SPECIALIZE}` at line 3 |
| G4 | **`specialise` section dropped** for specialised archetypes and templates. | CNV-cancer, GVR-cancer, T1, T2 outputs |
| G5 | **`language` section missing**, so the `sv` translation is lost. | All outputs |
| G6 | **ODIN quoting wrong**: `original_author` keys are unquoted (`name = <…>` instead of `["name"]`), and `language = <"ISO_639-1::en">` is written as a string instead of a code phrase. | All outputs |
| G7 | **Specialised codes (`id0.x`, `at0.x`, `ac0.x`) not mapped to 1.4 `at0000.x` form.** `value_sets` are not turned into inline 1.4 `[local:: …]` constraints. | ontology section of the outputs |
| G8 | **No template → OET/OPT 1.4 path verified** for ADL2 `template` files that use `use_archetype`. | T1/T2 |
| G9 | **Silent failure**: `parseErrors=0` while `warnings` contains a fatal cADL error. | probe script |

## Recommendations for Ehrtslib (issues Erik may want to file himself; not filed)
1. Make cADL parse failures hard errors.
2. Support the `cardinality matches {…; unordered} matches` and slot `archetype_id/value matches {/regex/}` forms produced by Archie's serializer.
3. ADL14Serializer: emit `concept`, `language` and `specialise`; quote ODIN keys correctly; write code phrases as `[ISO_639-1::en]`.
4. Map id-codes to at-codes, including specialised codes (`id0.1` → `at0.1`, `id1.1` → `at0000.1`), and turn value_sets into inline local constraints.
5. Add a round-trip test: Archie ADL2 output → Ehrtslib 1.4 → Archie `parse14`.

## Consequence for the main path
There is still **no working automatic ADL2 → 1.4 path** on the box (Archie can't, Ehrtslib produces invalid ADL). Options:
- (a) fix Ehrtslib (G1–G7)
- (b) write a small Archie-based Java down-converter (AOM2 → AOM1.4 serializer)
- (c) hand-maintain 1.4 versions of the 3 drafts and build T1/T2 as OETs in Better Template Designer.
