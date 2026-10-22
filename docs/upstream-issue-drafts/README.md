# Upstream issue drafts (not filed)

Drafts for bugs found while building the genomics EHR-slice demo. Nothing here has been posted.
Ehrtslib gaps D/E were filed directly as ErikSundvall/ehrtslib#141 and #142. After the 2026-10-22 retest, the follow-ups were filed as #145 (structural terms, ADL2 input), #146 (#144 not on main; LOINC `/ver/` bindings) and #147 (bound local value sets exported as external codes). The catch-up PR #148 is merged (35f33da). On 2026-10-22 #145 and #146 were still open and reproducible. #147 was closed through the #148 reference but is not fixed (commented, reopening requested). Later the same day: #146 was fixed on main (PR #149). The fixes for #147/#145 (PRs #150/#151) landed on stacked branches, with catch-up PR #154. The test-path issue is filed as #155. #154 was merged the same day (37657ec): #145 and #147 are fixed on main, and this repo no longer needs any Ehrtslib workaround. #155 is still open.

| File | Target | Title |
|---|---|---|
| 01-mapping-lib-service-request-provider.md | SevKohler/FHIRconnect-mapping-lib | service_request.v1: requester mapped to non-existent `$composition/provider` |
| 02-mapping-lib-lab-result-status-basedon.md | SevKohler/FHIRconnect-mapping-lib | laboratory_test_result.v1: status always `unknown`, `basedOn` emits empty CarePlan |
| 03-mapping-lib-readme-version.md | SevKohler/FHIRconnect-mapping-lib | README says engine supports only v0.9.0 |
| 04-spec-schema-link-key.md | SevKohler/FHIRconnect-spec | JSON Schema does not allow `link` |
| 05-openfhir-manual-on-repeating-element.md | openFHIR/openfhir | `manual` on repeating element applies last code to all repetitions |
| 06-openfhir-text-or-identifier.md | openFHIR/openfhir | DV_TEXT/DV_IDENTIFIER choice loses identifier on toFHIR |
| 07-openfhir-parsable-formalism.md | openFHIR/openfhir | DV_PARSABLE formalism always `text/html` |
| 08-openfhir-structuredefinition-profile-url.md | openFHIR/openfhir | profile URL in `fhirConfig.structureDefinition` silently disables mapping |
| 09-archie-fork-master-build.md | erik-sundvalls-bots/archie (own fork) | adl14 down-converter does not compile on Archie 4.0.0 |

IG Publisher: no real bug found (0 errors), so no draft.
