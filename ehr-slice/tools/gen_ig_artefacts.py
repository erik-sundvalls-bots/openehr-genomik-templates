"""Package the openEHR and FHIRconnect artefacts of the slice as FHIR resources in the IG.

Each file becomes a Binary (base64) in ig/input/resources/, and one Library resource
(ehr-slice-manifest) lists them all with their role, so the IG carries the complete slice:
OPT 1.4 templates, ADL2 templates and FHIRconnect mappings next to the FHIR profiles.
"""
import base64, hashlib, json, pathlib, re
import code_tables as ct
HERE = pathlib.Path(__file__).resolve().parent
SLICE = HERE.parent; REPO = SLICE.parent
OUT = SLICE / "ig" / "input" / "resources"; OUT.mkdir(parents=True, exist_ok=True)
for old in OUT.glob("Binary-*.json"): old.unlink()

def rid(prefix, path):
    stem = re.sub(r"[^A-Za-z0-9.-]+", "-", path.name).strip("-").replace("_", "-")
    i = f"{prefix}-{stem}"
    return i if len(i) <= 64 else i[:55] + "-" + hashlib.sha1(i.encode()).hexdigest()[:8]

ART = []   # (id, title, contentType, role, repo-relative path)
for p in sorted((SLICE / "templates" / "opt14").glob("*.opt")):
    ART.append((rid("opt", p), f"OPT 1.4: {p.name}", "application/xml", "openEHR operational template (OPT 1.4)", p))
for p in sorted((REPO / "templates" / "adl2").glob("*.adls")):
    ART.append((rid("adl2", p), f"ADL2 template: {p.name}", "text/plain", "openEHR template (ADL2 source)", p))
for p in sorted((SLICE / "fhirconnect").rglob("*.y*ml")):
    kind = "context" if p.name.endswith(".context.yaml") else ("model" if "/model/" in str(p) else "extension")
    ART.append((rid("fc", p), f"FHIRconnect {kind}: {p.relative_to(SLICE / 'fhirconnect')}", "application/yaml",
                f"FHIRconnect {kind} mapping", p))

rel = []
for i, title, mime, role, p in ART:
    b = {"resourceType": "Binary", "id": i, "contentType": mime,
         "data": base64.b64encode(p.read_bytes()).decode()}
    (OUT / f"Binary-{i}.json").write_text(json.dumps(b, indent=2) + "\n")
    rel.append({"type": "composed-of", "label": role, "display": title,
                "document": {"contentType": mime, "url": f"Binary/{i}", "title": p.relative_to(REPO).as_posix()}})

lib = {"resourceType": "Library", "id": "ehr-slice-manifest",
       "url": f"{ct.CANON}/Library/ehr-slice-manifest", "version": "0.1.0",
       "name": "EHRSliceManifestSECancerGenomics",
       "title": "EHR Slice manifest – Swedish cancer genomics (demo)",
       "status": "draft", "experimental": True,
       "type": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/library-type", "code": "asset-collection"}]},
       "description": ("The technology-neutral artefacts of this EHR Slice: openEHR templates (ADL2 and OPT 1.4) and "
                       "the bidirectional FHIRconnect mappings between them and the FHIR profiles in this guide."),
       "relatedArtifact": rel}
(OUT / "Library-ehr-slice-manifest.json").write_text(json.dumps(lib, indent=2, ensure_ascii=False) + "\n")
print(f"{len(ART)} Binary resources + Library-ehr-slice-manifest.json -> {OUT.relative_to(SLICE)}")

# Round-trip page: intro + the generated results table
res = SLICE / "roundtrip" / "RESULTS.md"
if res.exists():
    body = res.read_text().split("\n", 1)[1]          # drop the H1
    intro = """The mappings in this guide were executed with the open-source FHIRconnect engine
**openFHIR 3.0.2** (Docker image pinned by digest in `ehr-slice/engine/docker-compose.yml`):
the example FHIR resources of this guide were converted to openEHR compositions (flat and
canonical JSON), the canonical composition was converted back to FHIR, and that FHIR was
converted to openEHR once more. Reproduce with `ehr-slice/engine/bootstrap.sh` and
`ehr-slice/roundtrip/run.sh`.

Mappningarna har körts med den öppna motorn openFHIR 3.0.2: exemplen i guiden har översatts
FHIR → openEHR → FHIR → openEHR och jämförts fält för fält nedan.

Known, expected differences: the requesting physician (ServiceRequest.requester) has no element
in the T2 template and only reaches the composition as *composer*, so it is not regenerated;
party references get new `urn:uuid` ids on export.
"""
    (SLICE / "ig" / "input" / "pagecontent" / "roundtrip.md").write_text(intro + body.replace("\n## ", "\n### "))
    print("wrote ig/input/pagecontent/roundtrip.md")
