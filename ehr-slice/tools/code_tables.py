"""Single source of truth for coded-value correspondences used by the EHR Slice demo.

Each table lists, for one openEHR coded element, the local at-code in the OPT 1.4
(build/opt14) and the FHIR coding it corresponds to. The FSH terminology
(ig/input/fsh/terminology.fsh) and the FHIRconnect `manual` code mappings
(fhirconnect/**/*.yml, generated sections) are both generated from these tables,
so the openEHR and FHIR sides cannot drift apart.
"""
import json, pathlib

REPO = pathlib.Path(__file__).resolve().parents[2]
VS = json.load(open(REPO / "valuesets" / "valuesets.json"))["valuesets"]

CANON = "https://example.org/fhir/ehr-slice-se-genomics"
SO = "http://www.sequenceontology.org"
LOINC = "http://loinc.org"
SCT = "http://snomed.info/sct"
CS_FRAG = f"{CANON}/CodeSystem/fragestallning"
CS_ASCO = f"{CANON}/CodeSystem/asco-amp-tier"
CS_ESCAT = f"{CANON}/CodeSystem/escat-tier"

def _frag():
    out = []
    en = ["Primary diagnostics", "Prediction of treatment response", "Treatment monitoring",
          "Relapse detection (MRD)", "Resistance question", "Pharmacogenomics",
          "Hereditary cancer / oncogenetics", "Other"]
    for i, c in enumerate(VS["fragestallning"]["codes"]):
        out.append(dict(at=f"at0.{i+1}", at_text=en[i], system=CS_FRAG, code=c["code"],
                        display=c["display_sv"], display_en=en[i], definition=c["description"]))
    return out

def _asco():
    out = []
    for i, c in enumerate(VS["asco_tier"]["codes"]):
        out.append(dict(at=f"at0.{10+i}", at_text=c["code"], system=CS_ASCO, code=c["code"],
                        display=c["code"], display_en=c["display_en"], display_sv=c["display_sv"],
                        definition=c["display_en"]))
    return out

def _escat():
    out = []
    for i, c in enumerate(VS["escat_tier"]["codes"]):
        out.append(dict(at=f"at0.{20+i}", at_text="ESCAT " + c["code"], system=CS_ESCAT, code=c["code"],
                        display=c["code"], display_en=c["display_en"], definition=c["display_en"]))
    return out

def _mc():
    out = []
    for i, c in enumerate(VS["molecular_consequence"]["codes"]):
        out.append(dict(at=f"at0.{40+i}", at_text=c["display_en"], system=SO, code=c["so"],
                        display=c["display_en"]))
    return out

# LOINC LL378-1 (Genetic variant source), verified at https://loinc.org/LL378-1
GENETIC_ORIGIN = [
    dict(at="at0.1", at_text="Somatic", system=LOINC, code="LA6684-0", display="Somatic"),
    dict(at="at0.2", at_text="Germline", system=LOINC, code="LA6683-2", display="Germline"),
    dict(at="at0.3", at_text="Likely somatic", system=LOINC, code="LA18195-0", display="Likely somatic"),
    dict(at="at0.4", at_text="Likely germline", system=LOINC, code="LA18194-3", display="Likely germline"),
    dict(at="at0.5", at_text="Unknown origin", system=LOINC, code="LA18197-6", display="Unknown genomic origin"),
]

def _specimen_type():
    en = ["Blood venous", "Marrow", "Tissue", "Tumor", "Pleural fluid", "Fluid, Abdomen",
          "Cerebrospinal fluid", "Bone", "Skin", "Bile Fluid", "Cervical Mucus", "Urine"]
    out = []
    for i, c in enumerate(VS["provtyp"]["codes"][:12]):   # template ac0.1 = at0.1..at0.12
        assert c["display_en"] == en[i], (c, en[i])
        out.append(dict(at=f"at0.{i+1}", at_text=en[i], system=SCT, code=c["snomed"],
                        display=c["display_en"], display_sv=c["display_sv"]))
    return out

# laboratory_test_result.v1 Overall test status (CKM at-codes) <-> FHIR DiagnosticReport.status
REPORT_STATUS = [
    dict(at="at0107", at_text="Registered", code="registered"),
    dict(at="at0037", at_text="Partial", code="partial"),
    dict(at="at0120", at_text="Preliminary", code="preliminary"),
    dict(at="at0038", at_text="Final", code="final"),
    dict(at="at0040", at_text="Amended", code="amended"),
    dict(at="at0115", at_text="Corrected", code="corrected"),
    dict(at="at0119", at_text="Appended", code="appended"),
    dict(at="at0074", at_text="Cancelled", code="cancelled"),
    dict(at="at0116", at_text="Entered in error", code="entered-in-error"),
]

FRAGESTALLNING = _frag()
ASCO = _asco()
ESCAT = _escat()
MOLECULAR_CONSEQUENCE = _mc()
SPECIMEN_TYPE = _specimen_type()

if __name__ == "__main__":
    for n in ["FRAGESTALLNING", "ASCO", "ESCAT", "MOLECULAR_CONSEQUENCE", "GENETIC_ORIGIN", "SPECIMEN_TYPE"]:
        print(n, [(r["at"], r["code"]) for r in globals()[n]])
