# ADL2 → ADL 1.4 benchmark: Ehrtslib vs Archie fork
*Generated 2026-10-15 (Europe/Stockholm). Ehrtslib stack #114–#117 (local branches). Archie fork `feature/adl2-to-adl14-downconverter`.*
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
