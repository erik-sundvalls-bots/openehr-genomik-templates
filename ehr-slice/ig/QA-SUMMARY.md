# IG Publisher run (2026-10-21, 20:12 CEST)

`java -jar publisher.jar -ig ig.ini` (HL7 FHIR IG Publisher, latest release downloaded 2026-10-21, FHIR IG Publisher Version 3.0.1; Java 17; Jekyll 4.3.4; terminology server tx.fhir.org).

**Result:** Errors 0, Warnings 105, Info 67, Broken links 0. Build errors 0.

Re-run 2026-10-22 (after the Ehrtslib update, IG Publisher tool 6.0.0-snapshot1, FHIR 4.0.1): same result. Errors 0, Warnings 105, Info 67, Broken links 0. SUSHI: 0 errors, 0 warnings. A second re-run the same day, with Ehrtslib main 35f33da (OPT export pinned to fca190a), gave the same result. A third re-run with Ehrtslib main a5b7541 also gave the same result.

Main warning groups: example identifier systems under `https://example.org` (placeholder namespace),
the Sequence Ontology CodeSystem `http://www.sequenceontology.org` is not known to the terminology
server (SO codes cannot be validated), and the `Binary` artefacts have no description / are not
FHIR definitions (expected for OPT, ADL2 and FHIRconnect files).

The generated site (`output/`) is not committed. Note: the base template's Ant script fetched FHIR
schemas over plain http, which hung on this host; the local package cache copy was switched to https.
