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
- (c) hand-maintain 1.4 versions of the 3 drafts and build T1/T2 as OETs in a graphical template designer.

## New gaps found 2026-10-16 (genomics value-set bindings)

Status 2026-10-21: A = ehrtslib#133, B = ehrtslib#134, C = ehrtslib#135, all fixed/documented on ehrtslib main (ebc2434). The build workaround for A is removed and the fix for B is confirmed in the T2 OPT. Gap D = ehrtslib#141 and gap E = ehrtslib#142 (filed 2026-10-21, open).

### A. ADL2 tokenizer rejects `#` (and likely `?`) inside ODIN URI values
- Input: `["at0.10"] = <http://hl7.org/fhir/uv/genomics-reporting/CodeSystem/genomic-study-type-cs#alt-splc>` in `term_bindings`.
- Ehrtslib: `Unexpected character '#'` from `parser/adl2_tokenizer.ts`; the whole archetype fails to load, so templates using it lose that archetype ("no published base archetype in chain").
- Archie: parses and validates.
- Expected: URI values in ODIN accept full RFC 3986 syntax, including fragment and query.
- ~~Workaround in `tools/build.sh`~~: removed 2026-10-21. Parsing now works; the bindings are still missing from the OPT because of gap D.

### B. Differential path through `description` attribute not resolved (INSTRUCTION activities)
- Input (T2 overlay on service_request): `/activities[id2]/description[id10]/items[id63]/value matches { DV_CODED_TEXT[id9006.1] ... }`.
- Ehrtslib warns `differential path /items[id63]/value not found in parent`. The leading `/activities[id2]/description[id10]` segment appears to be lost, probably because `description` is also an ADL section keyword. The constraint is dropped from the OPT, but the at0.x terms are kept.
- Archie: flattens and validates correctly.

### C. OET 1.4 has no export for local coded-text redefinitions
- `value constraint at /items[at0029] has no OET equivalent; kept only in the OPT export` (specimen type, collection method, fixation method).
- The OPT is complete. The OET lacks these value sets. That may be acceptable, since OET textConstraint cannot carry new local codes. Document this in ADL_SUPPORT.md.

### D. OPT 1.4 exporter silently drops term bindings that are not `[t::c]` or `http://<host>/id/<code>` (new 2026-10-21, [ehrtslib#141](https://github.com/ErikSundvall/ehrtslib/issues/141))
- `generation/opt14/opt14_exporter.ts` `parseBinding()` only accepts `[terminology::code]` or `https?://<host>/id/<code>` (SNOMED/LOINC/openEHR style).
- Valid ADL2 binding URIs such as `http://hl7.org/fhir/uv/genomics-reporting/CodeSystem/genomic-study-type-cs#cnv` and `http://purl.obolibrary.org/obo/SO_0001583` return `undefined` and are dropped with no warning.
- Effect: T1 OPT has the SNOMED CT bindings but none of the HL7 study type/method or SO bindings.
- Expected: map at least `<code-system-uri>#<code>` (FHIR style) and OBO PURLs to a terminology id + code (e.g. terminology id from a configurable URI→id table, defaulting to the binding key), or warn when a binding cannot be exported.
- Related: Ehrtslib's ADL 1.4 down-conversion (`tools/ehrtslib-down14.ts`, `ADL14Serializer`) writes no `term_bindings` section at all for the drafts (SNOMED CT, SO and HL7 bindings all missing in `build/ehrtslib-adl14/`).
- Archie keeps all these bindings in its ADL 1.4 output (`build/archie-adl14/`: 12 HL7 bindings in `sequencing_assay-genomic_study`, 8 SO bindings in `genomic_variant_result-cancer`).

### E. OPT 1.4 export omits term_definitions for structural nodes (new 2026-10-21, [ehrtslib#142](https://github.com/ErikSundvall/ehrtslib/issues/142))

The exported OPTs have no `term_definitions` entry for locatable structural nodes such as `ITEM_TREE` (e.g. `at0001`, `at0003`, `at0004` in `laboratory_test_result.v1`, `at0008`/`at0009` in `service_request.v1`) and `HISTORY` (`at0001`). The OPTs are XSD-valid, but the EHRbase SDK web-template parser (`OPTParser.buildNode`, openEHR_SDK 2.19.0, used by openFHIR 3.0.2) throws a NullPointerException for any locatable node without a term, so the templates cannot be used by that engine. Workaround: `ehr-slice/tools/repair_opt_terms.py` copies the missing terms from the CKM ADL 1.4 sources (10 terms across the two OPTs). Suggested fix: emit a term for every node id of the flat archetype, including structural nodes.
