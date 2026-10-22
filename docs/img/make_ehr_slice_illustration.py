W,H=1700,940
F="DejaVu Sans, Noto Sans, Liberation Sans, sans-serif"
out=[]
a=out.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{F}">')
a('''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4f8fb"/><stop offset="1" stop-color="#e9f1f6"/></linearGradient>
<marker id="ah" markerUnits="userSpaceOnUse" markerWidth="22" markerHeight="22" refX="18" refY="11" orient="auto-start-reverse"><path d="M0,0 L22,11 L0,22 z" fill="#3b5b73"/></marker>
<filter id="sh" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#1d3a4f" flood-opacity="0.15"/></filter>
</defs>''')
a(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
# title
a(f'<text x="{W/2}" y="62" text-anchor="middle" font-size="38" font-weight="bold" fill="#1d3a4f">En EHR Slice för harmoniserad datamängd cancergenomik</text>')
a(f'<text x="{W/2}" y="102" text-anchor="middle" font-size="24" fill="#3b5b73">Ett versionerat paket som binder ihop openEHR-lagring och FHIR-utbyte</text>')
# cloud: union of circles
cx,cy=850,470
circ=[(850,300,150),(670,330,120),(1030,330,120),(550,420,105),(1150,420,105),(550,560,105),(1150,560,105),(670,640,115),(850,660,125),(1030,640,115)]
rect=(545,330,610,330)
def circles(extra,fill):
    s=''.join(f'<circle cx="{x}" cy="{y}" r="{r+extra}" fill="{fill}"/>' for x,y,r in circ)
    x,y,w,h=rect
    s+=f'<rect x="{x-extra}" y="{y-extra}" width="{w+2*extra}" height="{h+2*extra}" fill="{fill}"/>'
    return s
a(f'<g filter="url(#sh)">{circles(4,"#7fa9c4")}</g>')
a(f'<g>{circles(0,"#ffffff")}</g>')
a(f'<text x="{cx}" y="240" text-anchor="middle" font-size="46" font-weight="bold" fill="#1d3a4f">EHR Slice</text>')
a(f'<text x="{cx}" y="278" text-anchor="middle" font-size="21" fill="#3b5b73">= en utökad FHIR Implementation Guide (IG)</text>')
# tiles 2x2
tiles=[
 ("openEHR-templates","byggda på internationella","arketyper (CKM)","#e3f1dc","#5a8f3c"),
 ("FHIRconnect-mappningar","dubbelriktade:","template ⇄ FHIR-profil","#fdf0d5","#b7862a"),
 ("FHIR-profiler","på HL7 Genomics","Reporting IG","#dcecf8","#2f6f9f"),
 ("Kodverk och värdemängder","CodeSystem / ValueSet","(SO, LOINC, SNOMED CT, lokala)","#ece3f5","#7350a0"),
]
tw,th=310,128; gx,gy=16,22
x0=cx-tw-gx/2; y0=318
for i,(t1,t2,t3,bgc,fg) in enumerate(tiles):
    x=x0+(i%2)*(tw+gx); y=y0+(i//2)*(th+gy)
    a(f'<rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="16" fill="{bgc}" stroke="{fg}" stroke-width="2.5"/>')
    a(f'<text x="{x+tw/2}" y="{y+44}" text-anchor="middle" font-size="19" font-weight="bold" fill="{fg}">{t1}</text>')
    a(f'<text x="{x+tw/2}" y="{y+78}" text-anchor="middle" font-size="18" fill="#33475b">{t2}</text>')
    a(f'<text x="{x+tw/2}" y="{y+103}" text-anchor="middle" font-size="18" fill="#33475b">{t3}</text>')
# banner
by=y0+2*th+gy+26
a(f'<rect x="{cx-350}" y="{by}" width="700" height="54" rx="27" fill="#fbe3c2" stroke="#c98a3a" stroke-width="2.5"/>')
a(f'<text x="{cx}" y="{by+35}" text-anchor="middle" font-size="19" font-weight="bold" fill="#7a4d14">Versioneras och publiceras tillsammans · leverantörsneutralt</text>')
# side boxes
def side(x,title,lines,fill,stroke):
    a(f'<rect x="{x}" y="320" width="260" height="310" rx="20" fill="{fill}" stroke="{stroke}" stroke-width="3" filter="url(#sh)"/>')
    a(f'<text x="{x+130}" y="385" text-anchor="middle" font-size="26" font-weight="bold" fill="{stroke}">{title[0]}</text>')
    a(f'<text x="{x+130}" y="417" text-anchor="middle" font-size="17" fill="{stroke}">{title[1]}</text>')
    for j,l in enumerate(lines):
        a(f'<text x="{x+130}" y="{470+j*30}" text-anchor="middle" font-size="18" fill="#33475b">{l}</text>')
side(30,("openEHR CDR","(Clinical Data Repository)"),["beständig, strukturerad","lagring i openEHR-format","sökbar med AQL","valfri leverantör"],"#eef6ea","#4a7d2f")
side(1410,("FHIR API","(HL7 FHIR R4)"),["utbyte med andra system","t.ex. IPÖ, nationella","tjänster och EHDS","inget openEHR-beroende"],"#e8f1f9","#2f6f9f")
# cylinder icon left, plug icon right (simple)
a('<g transform="translate(135,565)" fill="none" stroke="#4a7d2f" stroke-width="3"><ellipse cx="25" cy="8" rx="25" ry="8" fill="#d7ead0"/><path d="M0,8 v34 a25,8 0 0 0 50,0 v-34"/><path d="M0,25 a25,8 0 0 0 50,0"/></g>')
a('<g transform="translate(1515,563)" fill="none" stroke="#2f6f9f" stroke-width="3"><rect x="0" y="10" width="50" height="34" rx="6" fill="#d3e5f4"/><path d="M14,10 v-10 M36,10 v-10 M25,44 v12"/></g>')
# arrows
for (x1,x2,lab) in [(298,440,"openEHR-data"),(1260,1402,"FHIR-resurser")]:
    a(f'<line x1="{x1}" y1="470" x2="{x2}" y2="470" stroke="#3b5b73" stroke-width="5" marker-start="url(#ah)" marker-end="url(#ah)"/>')
    a(f'<text x="{(x1+x2)/2}" y="505" text-anchor="middle" font-size="17" fill="#3b5b73">{lab}</text>')
# caption
a(f'<text x="{W/2}" y="830" text-anchor="middle" font-size="21" fill="#33475b">Samma specifikation ger både ett FHIR-gränssnitt och en färdig, plattformsoberoende väg till openEHR-lagring.</text>')
a(f'<text x="{W/2}" y="895" text-anchor="middle" font-size="17" fill="#5b6f80">Inspirerad av illustration från openEHR International: openehr.org/what-is-an-ehr-slice-and-why-is-it-relevant-to-the-ehds/</text>')
a('</svg>')
open('docs/img/ehr-slice-illustration.svg','w').write('\n'.join(out))
import cairosvg
cairosvg.svg2png(url='docs/img/ehr-slice-illustration.svg',write_to='docs/img/ehr-slice-illustration.png',output_width=1700)
