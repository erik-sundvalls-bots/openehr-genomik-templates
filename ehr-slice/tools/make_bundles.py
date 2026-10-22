"""Assemble the FHIR input Bundles for the round-trip from the SUSHI-built examples."""
import json, pathlib, uuid
HERE = pathlib.Path(__file__).resolve().parent
RES = HERE.parent / "ig" / "fsh-generated" / "resources"
OUT = HERE.parent / "examples" / "fhir"; OUT.mkdir(parents=True, exist_ok=True)

def load(rt, id_): return json.load(open(RES / f"{rt}-{id_}.json"))

def bundle(name, items):
    b = {"resourceType": "Bundle", "id": name, "type": "transaction", "entry": []}
    for rt, id_ in items:
        r = load(rt, id_)
        b["entry"].append({"fullUrl": f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, rt + '/' + id_)}",
                           "resource": r, "request": {"method": "PUT", "url": f"{rt}/{id_}"}})
    (OUT / f"{name}.json").write_text(json.dumps(b, indent=2, ensure_ascii=False) + "\n")
    print("wrote", (OUT / f"{name}.json").relative_to(HERE.parent))

bundle("T2-request-bundle", [("ServiceRequest", "servicerequest-demo-1"), ("Condition", "diagnosis-demo-1"),
                             ("Organization", "lab-genomics-demo"), ("Practitioner", "practitioner-demo-1"),
                             ("Patient", "patient-demo-1")])
bundle("T1-report-bundle", [("DiagnosticReport", "genomic-report-demo-1"), ("Observation", "variant-demo-egfr"),
                            ("Observation", "variant-demo-tp53"), ("Specimen", "specimen-demo-1"),
                            ("Organization", "lab-genomics-demo"), ("ServiceRequest", "servicerequest-demo-1"),
                            ("Patient", "patient-demo-1")])
