#!/usr/bin/env python3
"""Inject a local Swedish (sv) translation into CKM ADL2 copies (term texts/descriptions + details).
Source of translations: translations/sv/<concept>.json. Idempotent (skips files that already have sv)."""
import re, json, sys, glob, os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def esc(s): return s
for jf in sorted(glob.glob(f"{ROOT}/translations/sv/*.json")):
    concept=os.path.basename(jf)[:-5]; tr=json.load(open(jf))
    files=[f for f in glob.glob(f"{ROOT}/archetypes/ckm-adl2/openEHR-EHR-CLUSTER.{concept}.v*.adls")]
    for f in files:
        s=open(f).read()
        if '["sv"] = <\n            language = <[ISO_639-1::sv]>' in s: print("skip",f); continue
        tdi=s.index('term_definitions = <')
        i=s.index('        ["en"] = <',tdi); j=s.index('\n        >',i)
        en=dict((k,(t,d)) for k,t,d in re.findall(r'\["((?:id|at|ac)[0-9.]+)"\] = <\s*text = <"(.*?)">\s*description = <"(.*?)">',s[i:j],re.S))
        entext2sv={t:tr[k][0] for k,(t,d) in en.items() if k in tr}
        lines=['        ["sv"] = <']; missing=[]
        for k,(t,d) in en.items():
            if k in tr: st,sd=tr[k]
            elif re.fullmatch(r'Chromosome (\w+)',t): n=t.split()[1]; st,sd=f"Kromosom {n}",f"Kromosom {n}."
            elif t.endswith(' (synthesised)') and t[:-14] in entext2sv:
                st=entext2sv[t[:-14]]+" (syntetiserad)"; sd=st
            else: st,sd=t,d; missing.append(k)
            lines+= [f'            ["{k}"] = <', f'                text = <"{st}">', f'                description = <"{sd}">', '            >']
        lines.append('        >')
        s=s[:j]+'\n        >\n'+'\n'.join(lines)+s[j+len('\n        >'):]
        auth=('        ["sv"] = <\n            language = <[ISO_639-1::sv]>\n            author = <\n'
              '                ["name"] = <"Erik Sundvall">\n            >\n'
              '            accreditation = <"Local draft translation, not CKM-reviewed">\n        >\n')
        s=s.replace('    translations = <\n','    translations = <\n'+auth,1)
        det=(f'        ["sv"] = <\n            language = <[ISO_639-1::sv]>\n            purpose = <"{tr["_purpose"]}">\n'
             f'            use = <"Lokal svensk översättning (utkast) – se docs/forum-proposals/07-ckm-swedish-translations.md.">\n        >\n')
        s=s.replace('    details = <\n','    details = <\n'+det,1)
        open(f,'w').write(s); print("sv added",os.path.basename(f),"untranslated:",missing)
