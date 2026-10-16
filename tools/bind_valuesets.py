#!/usr/bin/env python3
"""Helpers that map valuesets/*.json to local at-codes (en/sv text + SNOMED CT bindings). Used once to generate the bound overlays in templates/adl2 (the generated ADL2 is the source of truth)."""
import json, os
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V=lambda n: json.load(open(f"{R}/valuesets/{n}.json"))["codes"]
SCT="http://snomed.info/id/"
EM_EN={"DNA":"DNA","RNA":"RNA","ctDNA":"Circulating tumour DNA (ctDNA)","ctRNA":"Circulating tumour RNA (ctRNA)","cfDNA":"Cell-free DNA (cfDNA)"}
FR_EN={"1":"Primary diagnostics","2":"Prediction of treatment response","3":"Treatment monitoring","4":"Relapse detection (MRD)","5":"Resistance question","6":"Pharmacogenomics","7":"Hereditary cancer / oncogenetics","8":"Other"}
def specimen_type():
    out=[(c["display_en"],c["display_sv"],c.get("snomed"),f'HL7 v2 0487: {c["hl7_v2"]}') for c in V("provtyp")]
    out+=[(EM_EN[c["code"]],c["display_sv"],c.get("snomed"),"Extracted material") for c in V("extraherat_material")]
    return out
def collection(): return [(c["display_en"],c["display_sv"],c.get("snomed"),"Collection technique") for c in V("provtagningsteknik")]
def fixation(): return [(c["display_en"],c["display_sv"],c.get("snomed"),"Fixation / preservation method") for c in V("fixeringsmetod")]
def question(): return [(FR_EN[c["code"]],c["display_sv"],None,f'Local request question code {c["code"]}') for c in V("fragestallning")]
def terms(start, items):
    en=sv=""; sn=[]; codes=[]
    for i,(e,s,sct,d) in enumerate(items):
        c=f"at0.{start+i}"; codes.append(c)
        en+=f'\t\t\t["{c}"] = <\n\t\t\t\ttext = <"{e}">\n\t\t\t\tdescription = <"{d}.">\n\t\t\t>\n'
        sv+=f'\t\t\t["{c}"] = <\n\t\t\t\ttext = <"{s}">\n\t\t\t\tdescription = <"{d}.">\n\t\t\t>\n'
        if sct: sn.append(f'\t\t\t["{c}"] = <{SCT}{sct}>')
    return codes,en,sv,sn
