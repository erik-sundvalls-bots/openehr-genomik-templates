package se.rcc;

import com.nedap.archie.adl14.ADL14ConversionConfiguration;
import com.nedap.archie.adl14.ADL14Converter;
import com.nedap.archie.adl14.ADL14Parser;
import com.nedap.archie.adl14.ADL2ConversionResult;
import com.nedap.archie.adl14.ADL2ConversionResultList;
import com.nedap.archie.adlparser.ADLParser;
import com.nedap.archie.aom.Archetype;
import com.nedap.archie.rminfo.MetaModelProvider;
import com.nedap.archie.serializer.adl.ADLArchetypeSerializer;
import org.openehr.referencemodels.BuiltinReferenceModels;

import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Collections;

/**
 * Archie helper for openehr-genomik-templates.
 * Commands: parse14 | to2 | parse2 | roundtrip14to2
 * Archie converts ADL 1.4 → ADL 2 only; use Ehrtslib for ADL 2 → 1.4.
 */
public class ArchieConvert {
    public static void main(String[] args) throws Exception {
        if (args.length < 2) {
            System.err.println("Usage: ArchieConvert <parse14|to2|parse2|roundtrip14to2> <file> [out]");
            System.exit(2);
        }
        String cmd = args[0];
        Path in = Path.of(args[1]);
        String text = "";
        if (!cmd.equals("batch")) {
            text = Files.readString(in, StandardCharsets.UTF_8);
            if (!text.isEmpty() && text.charAt(0) == '\uFEFF') text = text.substring(1);
        }
        MetaModelProvider models = BuiltinReferenceModels.getMetaModelProvider();
        ADL14ConversionConfiguration cfg = new ADL14ConversionConfiguration();
        switch (cmd) {
            case "parse14" -> {
                ADL14Parser p = new ADL14Parser(models);
                Archetype a = p.parse(text, cfg);
                System.out.println("OK ADL1.4 parse: " + a.getArchetypeId().getFullId()
                        + " errors=" + p.getErrors().getErrors().size());
                if (!p.getErrors().hasNoErrors()) System.exit(1);
            }
            case "to2", "roundtrip14to2" -> {
                ADL14Parser p = new ADL14Parser(models);
                Archetype a14 = p.parse(text, cfg);
                if (!p.getErrors().hasNoErrors()) {
                    System.err.println("Parse errors: " + p.getErrors());
                    System.exit(1);
                }
                ADL14Converter conv = new ADL14Converter(models, cfg);
                ADL2ConversionResultList list = conv.convert(Collections.singletonList(a14));
                ADL2ConversionResult res = list.getConversionResults().get(0);
                if (res.getException() != null) {
                    res.getException().printStackTrace();
                    System.exit(1);
                }
                Archetype a2 = res.getArchetype();
                String adl2 = ADLArchetypeSerializer.serialize(a2);
                if (cmd.equals("to2")) {
                    Path out = Path.of(args[2]);
                    if (out.getParent() != null) Files.createDirectories(out.getParent());
                    Files.writeString(out, adl2, StandardCharsets.UTF_8);
                    System.out.println("Wrote ADL2 " + a2.getArchetypeId().getFullId() + " -> " + out
                            + " (" + adl2.length() + " chars)");
                } else {
                    System.out.println("Converted " + a2.getArchetypeId().getFullId()
                            + " len=" + adl2.length());
                }
            }
            case "batch" -> {
                // args[1]=input dir, args[2]=output dir : converts all .adl together (handles specialisation parents)
                Path dir = in;
                Path outDir = Path.of(args[2]);
                Files.createDirectories(outDir);
                java.util.List<Archetype> all = new java.util.ArrayList<>();
                try (var s = Files.list(dir)) {
                    for (Path f : s.filter(x -> x.toString().endsWith(".adl")).sorted().toList()) {
                        String t = Files.readString(f, StandardCharsets.UTF_8);
                        if (!t.isEmpty() && t.charAt(0) == '\uFEFF') t = t.substring(1);
                        ADL14Parser p = new ADL14Parser(models);
                        Archetype a = p.parse(t, cfg);
                        if (!p.getErrors().hasNoErrors()) { System.err.println("PARSE FAIL " + f + ": " + p.getErrors()); continue; }
                        all.add(a);
                    }
                }
                ADL14Converter conv = new ADL14Converter(models, cfg);
                ADL2ConversionResultList list = conv.convert(all);
                int ok = 0, fail = 0;
                for (ADL2ConversionResult r : list.getConversionResults()) {
                    if (r.getException() != null || r.getArchetype() == null) {
                        fail++; System.err.println("CONVERT FAIL " + r.getArchetypeId() + ": " + r.getException());
                        continue;
                    }
                    Archetype a2 = r.getArchetype();
                    String id = a2.getArchetypeId().getFullId();
                    Files.writeString(outDir.resolve(id + ".adls"), ADLArchetypeSerializer.serialize(a2), StandardCharsets.UTF_8);
                    ok++;
                }
                System.out.println("batch ok=" + ok + " fail=" + fail);
            }
            case "parse2" -> {
                ADLParser p = new ADLParser(models);
                Archetype a = p.parse(text);
                if (!p.getErrors().hasNoErrors()) {
                    System.err.println("Errors: " + p.getErrors());
                    System.exit(1);
                }
                System.out.println("OK ADL2 parse: " + a.getArchetypeId().getFullId()
                        + " adlVersion=" + a.getAdlVersion());
            }
            default -> {
                System.err.println("Unknown command: " + cmd);
                System.exit(2);
            }
        }
    }
}
