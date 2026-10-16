# ADL2 → ADL 1.4 benchmark: Ehrtslib vs Archie fork
*Generated 2026-10-15 (Europe/Stockholm). Ehrtslib stack #114–#117 (local branches). Archie fork `feature/adl2-to-adl14-downconverter`.*
## Re-run 2026-10-16 05:30 (Europe/Stockholm): #127 collision rule in both tools

Ehrtslib PR #126 (Closes ehrtslib#127) and Archie fork PR #3 both apply the same rule:
- Value codes keep the shifted code.
- A node and a value code with identical terms share the code.
- Any other colliding node moves to `at9000+` at the same specialisation level (`at0.9000+` when specialised).
- Root codes never move.
- Synthetic `id9000+` ids are dropped.

| Archetype | Ehrtslib parse14 | Archie parse14 | node codes identical | code set identical | `at8999` |
|---|---|---|---|---|---|
| openEHR-EHR-CLUSTER.genomic_copy_number_variant-cancer.v1.0.0 | errors=0 | errors=0 | yes | yes | 0 |
| openEHR-EHR-CLUSTER.genomic_variant_result-cancer.v1.0.0 | errors=0 | errors=0 | yes | yes | 0 |
| openEHR-EHR-CLUSTER.organisation.v1.0.4 | errors=0 | errors=0 | yes | yes | 0 |
| openEHR-EHR-CLUSTER.variant_clinical_implication.v1.0.0 | errors=0 | errors=0 | yes | yes | 0 |
| openEHR-EHR-EVALUATION.code_list_parent.v1.0.0 | errors=0 | errors=0 | yes | yes | 0 |

- The ADL2 spec 9.9 id-coded example (`code_list_parent`) gives `DV_CODED_TEXT[at9000]` and `local::at0003, …, at0008` in both tools, as in the spec's at-coded version.
- The CKM organisation round trip (1.4 → Archie ADL2 → 1.4) reproduces the CKM at-code set exactly. The synthetic `at8999`–`at9003` codes are gone.
- The tools agree on every code. Their text is not byte-identical: the remaining differences are formatting only (`rm_release` default, `-- comment` lines, blank lines, inline vs. block `defining_code`).

## Re-run 2026-10-15 21:59 (Europe/Stockholm): spec-correct code offset

Ehrtslib PR #126 and Archie fork PR #2 both map `id1` → `at0000` (ADL2 spec; inverse of Archie `ADL14NodeIDConverter.convertCode`).

| Archetype | Ehrtslib parse14 | Archie fork parse14 | at-code sets equal |
|---|---|---|---|
| genomic_copy_number_variant-cancer | OK, 0 errors | OK, 0 errors | yes |
| genomic_variant_result-cancer | OK, 0 errors | OK, 0 errors | yes |
| organisation (CKM) | OK, 0 errors | OK, 0 errors | yes |
| variant_clinical_implication | OK, 0 errors | OK, 0 errors | yes |

The organisation round trip (CKM 1.4 → Archie ADL2 → 1.4) reproduces every CKM at-code. It also adds `at8999`–`at9003`, which come from Archie's synthetic `id9000+` node ids; both tools produce these.

The tables below are from the earlier run (off-by-one mapping).

## Summary
### `openEHR-EHR-CLUSTER.genomic_copy_number_variant-cancer.v1.0.0.adl`
| Check | Ehrtslib | Archie |
|---|---|---|
| chars | 5362 | 5257 |
| has_concept | True | True |
| has_language | True | True |
| has_specialize | True | True |
| has_ontology | True | True |
| iso_lang | True | True |
| quoted_name | True | True |
| local_vs | True | True |
| undefined | False | False |
| at_codes | 4 | 3 |
| sv | True | True |

Sections ehrtslib: `['archetype', 'concept', 'definition', 'description', 'language', 'ontology', 'specialize']`  
Sections archie: `['archetype', 'concept', 'definition', 'description', 'language', 'ontology', 'specialize']`

### `openEHR-EHR-CLUSTER.genomic_variant_result-cancer.v1.0.0.adl`
| Check | Ehrtslib | Archie |
|---|---|---|
| chars | 19605 | 17957 |
| has_concept | True | True |
| has_language | True | True |
| has_specialize | True | True |
| has_ontology | True | True |
| iso_lang | True | True |
| quoted_name | True | True |
| local_vs | True | True |
| undefined | False | False |
| at_codes | 18 | 18 |
| sv | True | True |

Sections ehrtslib: `['archetype', 'concept', 'definition', 'description', 'language', 'ontology', 'specialize']`  
Sections archie: `['archetype', 'concept', 'definition', 'description', 'language', 'ontology', 'specialize']`

### `openEHR-EHR-CLUSTER.organisation.v1.0.4.adl`
| Check | Ehrtslib | Archie |
|---|---|---|
| chars | 24864 | 30169 |
| has_concept | True | True |
| has_language | True | True |
| has_specialize | False | False |
| has_ontology | True | True |
| iso_lang | True | True |
| quoted_name | True | True |
| local_vs | False | False |
| undefined | False | False |
| at_codes | 16 | 16 |
| sv | True | True |

Sections ehrtslib: `['archetype', 'concept', 'definition', 'description', 'language', 'ontology']`  
Sections archie: `['archetype', 'concept', 'definition', 'description', 'language', 'ontology']`

### `openEHR-EHR-CLUSTER.variant_clinical_implication.v1.0.0.adl`
| Check | Ehrtslib | Archie |
|---|---|---|
| chars | 9923 | 9361 |
| has_concept | True | True |
| has_language | True | True |
| has_specialize | False | False |
| has_ontology | True | True |
| iso_lang | True | True |
| quoted_name | True | True |
| local_vs | True | True |
| undefined | False | False |
| at_codes | 16 | 16 |
| sv | True | True |

Sections ehrtslib: `['archetype', 'concept', 'definition', 'description', 'language', 'ontology']`  
Sections archie: `['archetype', 'concept', 'definition', 'description', 'language', 'ontology']`

## Gaps observed
- Both emit concept/language/specialize/ontology for specialised drafts.
- Ehrtslib now quotes `\"name\"` ODIN keys; compare `quoted_name` column.
- Value-set expansion (`local::`) depends on members present in ADL2 `value_sets`.
- Template → OET still neither tool (documented in Ehrtslib #117 / Archie docs).
- Outputs: `build/ehrtslib-adl14/` vs `build/archie-adl14/`.

## Archie parse14 results (2026-10-15 evening)

After Ehrtslib stack #114–#117 tip + Archie fork fixes:

| Output set | Result |
|---|---|
| `build/ehrtslib-adl14/` (4 fixtures) | **4/4 OK** |
| `build/archie-adl14/` (4 fixtures) | **4/4 OK** |
| **Total** | **8/8** |

Fixes applied during benchmark:
- Ehrtslib: bare `author` ODIN attrs; per-language `items = <`; inline `{|>0|}`
- Archie: specialize before concept; rewrite `/items[idN]` path codes

Template → OET remains unimplemented in both (Better path).
