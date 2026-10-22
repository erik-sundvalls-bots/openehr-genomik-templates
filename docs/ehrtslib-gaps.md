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

Status 2026-10-21: A = ehrtslib#133, B = ehrtslib#134, C = ehrtslib#135, all fixed/documented on ehrtslib main (ebc2434). The build workaround for A is removed and the fix for B is confirmed in the T2 OPT. Gap D = ehrtslib#141 and gap E = ehrtslib#142 (filed 2026-10-21).

Status 2026-10-22, fourth retest: **all open gaps for this repo are fixed on Ehrtslib main @ 37657ec** (PR #154 merged; it carries the fixes from PRs #150/#151, verified with `git merge-base --is-ancestor` and `git cherry`):
- `tools/build.sh` exports OPT/OET from Ehrtslib main. The fca190a pin (`EHRTSLIB_OPT_REF`, git worktree) and `ehr-slice/tools/repair_opt_terms.py` are removed.
- #147: every DV_CODED_TEXT code list in both OPTs is `local` (30 + 4 code phrases), with no LOINC LA codes. The external codes are `term_bindings`: `LOINC(2.65)`, `LOINC(2.80)`, SNOMED CT, `SO` (CURIE form `SO:0001583`) and both HL7 code systems. 0 `Cannot export` warnings.
- #145: the 10 structural terms are synthesised from the RM type ("Tree", "History"), with a warning per node in `build/ehrtslib-export-log.txt`. openFHIR loads the plain OPTs.
- Results unchanged: Archie 31/31, XSD valid, round-trip FHIR 45/46 and openEHR flat 78/89, "missense_variant" kept with its code.
- Side effect: compositions now name these structural nodes "History"/"Tree" where the CKM ADL 1.4 text was e.g. "Event Series"/"structure". Flat paths and FHIRconnect mappings do not use these names, so nothing else changed.
- Still open: ehrtslib#155 (the #117 test hardcodes this repo's path and writes into `build/ehrtslib-adl14/`).

Status 2026-10-22, third retest: Ehrtslib main @ a5b7541, plus catch-up branch `cursor/catchup-150-151` (06d2007, [PR #154](https://github.com/ErikSundvall/ehrtslib/pull/154)):
- **LOINC `/ver/` bindings are fixed on main** (ehrtslib#146, PR #149). With an unpinned export there are 0 `Cannot export` warnings, and the bindings appear as `LOINC(2.65)` / `LOINC(2.80)`.
- **#147 (local value sets) and #145 (structural terms) are fixed by PRs #150/#151, but those were merged into stacked base branches, not main.** On main a5b7541, SO codes still replace the local codes, and 10 structural terms are still missing. Catch-up: PR #154.
- On the catch-up branch with `EHRTSLIB_OPT_REF=HEAD`:
  - Local code lists are kept, with no LOINC LA codes in any code_list.
  - `term_bindings` carry `LOINC(2.65)`/`LOINC(2.80)`, SNOMED CT, `SO` with `SO:0001583`, and both HL7 code systems.
  - The structural terms are synthesised ("Tree", "History").
  - openFHIR loads the OPTs **without** `repair_opt_terms.py`. The round-trip stays at 45/46 and 78/89, and "missense_variant" is preserved. The only composition difference is the synthesised structural names ("History" instead of CKM "Event Series", "Tree" instead of "structure").
- ~~Until PR #154 is on main, the fca190a pin and `repair_opt_terms.py` stay.~~ Done in the fourth retest above.
- Also filed: ehrtslib#155. The #117 test hardcodes `/workspace/openehr-genomik-templates` and writes into this repo's `build/ehrtslib-adl14/`.

Status 2026-10-22, second retest with ehrtslib main @ 35f33da (#148 brought #144 to main):
- **D is fixed on main** (ehrtslib#141, PR #144 via catch-up PR #148, commit b300f3a). HL7 and SO bindings now reach the OPT, and the Ehrtslib ADL 1.4 down-conversion writes `term_bindings` (SNOMED CT, SO, HL7). The build uses main for the down-conversion.
- **E is still open for this repo** ([ehrtslib#145](https://github.com/ErikSundvall/ehrtslib/issues/145)). #142 / PR #143 fixed only the ADL 1.4 → ADL2 converter. This build feeds ADL2 (Archie-converted CKM) archetypes, whose structural id-codes have no terms, so the OPTs still lack the same 10 terms. Without `ehr-slice/tools/repair_opt_terms.py`, openFHIR rejects both templates ("Could not create a WebTemplate"). The workaround stays.
- **LOINC `/ver/<v>/id/<code>` bindings are still dropped** (170 warnings): [ehrtslib#146](https://github.com/ErikSundvall/ehrtslib/issues/146).
- **New regression on main: bound local value sets are exported as external code lists** ([ehrtslib#147](https://github.com/ErikSundvall/ehrtslib/issues/147), closed through the #148 reference but not fixed; reopening requested). For example, molecular consequence becomes `SO` `0001583…` instead of `local` `at0.40…`. With such an OPT, openFHIR writes `DV_CODED_TEXT` without `value` ("missense_variant" lost). The round-trip score is unchanged (45/46, 78/89), but the data is RM-invalid. **Decision:** `tools/build.sh` pins the OPT/OET export to fca190a (`EHRTSLIB_OPT_REF`, a git worktree) until #147 is fixed. The OPTs therefore have no HL7/SO bindings yet; those bindings are mapping metadata, not data. Set `EHRTSLIB_OPT_REF=HEAD` to test main.

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

### D. OPT 1.4 exporter silently drops term bindings that are not `[t::c]` or `http://<host>/id/<code>` (new 2026-10-21, [ehrtslib#141](https://github.com/ErikSundvall/ehrtslib/issues/141); fixed on main by PR #144/#148, commit b300f3a; used by this build since the pin was removed on 2026-10-22)
- `generation/opt14/opt14_exporter.ts` `parseBinding()` only accepts `[terminology::code]` or `https?://<host>/id/<code>` (SNOMED/LOINC/openEHR style).
- Valid ADL2 binding URIs such as `http://hl7.org/fhir/uv/genomics-reporting/CodeSystem/genomic-study-type-cs#cnv` and `http://purl.obolibrary.org/obo/SO_0001583` return `undefined` and are dropped with no warning.
- Effect: T1 OPT has the SNOMED CT bindings but none of the HL7 study type/method or SO bindings.
- Expected: map at least `<code-system-uri>#<code>` (FHIR style) and OBO PURLs to a terminology id + code (e.g. terminology id from a configurable URI→id table, defaulting to the binding key), or warn when a binding cannot be exported.
- Related: Ehrtslib's ADL 1.4 down-conversion (`tools/ehrtslib-down14.ts`, `ADL14Serializer`) writes no `term_bindings` section at all for the drafts (SNOMED CT, SO and HL7 bindings all missing in `build/ehrtslib-adl14/`).
- Archie keeps all these bindings in its ADL 1.4 output (`build/archie-adl14/`: 12 HL7 bindings in `sequencing_assay-genomic_study`, 8 SO bindings in `genomic_variant_result-cancer`).

### E. OPT 1.4 export omits term_definitions for structural nodes (new 2026-10-21, [ehrtslib#142](https://github.com/ErikSundvall/ehrtslib/issues/142); ADL2 sources: [ehrtslib#145](https://github.com/ErikSundvall/ehrtslib/issues/145), fixed on main 37657ec; workaround removed)

The exported OPTs have no `term_definitions` entry for locatable structural nodes such as `ITEM_TREE` (e.g. `at0001`, `at0003`, `at0004` in `laboratory_test_result.v1`, `at0008`/`at0009` in `service_request.v1`) and `HISTORY` (`at0001`). The OPTs are XSD-valid, but the EHRbase SDK web-template parser (`OPTParser.buildNode`, openEHR_SDK 2.19.0, used by openFHIR 3.0.2) throws a NullPointerException for any locatable node without a term, so the templates cannot be used by that engine. The former workaround (`ehr-slice/tools/repair_opt_terms.py`, 10 terms copied from the CKM ADL 1.4 sources) was removed on 2026-10-22. Suggested fix: emit a term for every node id of the flat archetype, including structural nodes.
