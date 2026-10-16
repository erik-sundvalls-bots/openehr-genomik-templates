import { parseAdl } from "../../ehrtslib/parser/parse_adl.ts";
import { ADL14Serializer } from "../../ehrtslib/generation/adl14_serializer.ts";
const out = Deno.args[0];
for (const f of Deno.args.slice(1)) {
  const name = f.split("/").pop()!;
  try {
    const r: any = parseAdl(await Deno.readTextFile(f));
    const a = r.archetype ?? r.template ?? r.result ?? r;
    const errs = (r.errors ?? []).length;
    const txt = new ADL14Serializer().serialize(a);
    const o = `${out}/${name.replace(/\.v(\d+)\.\d+\.\d+.*\.adls$/, ".v$1.adl")}`;
    await Deno.writeTextFile(o, txt);
    console.log(`OK ${name} parseErrors=${errs} warnings=${(r.warnings??[]).length} -> ${o.split("/").pop()}`);
  } catch (e) { console.log(`FAIL ${name}: ${(e as Error).message.slice(0,200)}`); }
}
