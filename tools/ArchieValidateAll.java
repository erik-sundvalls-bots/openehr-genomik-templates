import com.nedap.archie.adlparser.ADLParser;
import com.nedap.archie.aom.Archetype;
import com.nedap.archie.archetypevalidator.*;
import com.nedap.archie.flattener.InMemoryFullArchetypeRepository;
import org.openehr.referencemodels.BuiltinReferenceModels;
import java.nio.file.*; import java.util.*;
/** Validate (incl. specialisation/flattening) all ADL2 files under given dirs with Archie. */
public class ArchieValidateAll {
  public static void main(String[] args) throws Exception {
    var repo = new InMemoryFullArchetypeRepository();
    List<String> names = new ArrayList<>();
    for (String d : args) try (var s = Files.walk(Path.of(d))) {
      for (Path p : s.filter(x -> x.toString().matches(".*\\.adl[st]$")).toList()) {
        ADLParser parser = new ADLParser();
        Archetype a = parser.parse(Files.readString(p));
        if (parser.getErrors().hasErrors()) { System.out.println("PARSE-ERR " + p + " " + parser.getErrors()); continue; }
        repo.addArchetype(a); names.add(a.getArchetypeId().getFullId());
      }
    }
    repo.compile(BuiltinReferenceModels.getMetaModelProvider());
    int bad = 0;
    for (ValidationResult r : repo.getAllValidationResults()) {
      long errs = r.getErrors().stream().filter(m -> !m.isWarning()).count();
      if (errs > 0 || !r.passes()) { bad++; System.out.println("FAIL " + r.getArchetypeId());
        r.getErrors().stream().filter(m -> !m.isWarning()).forEach(m -> System.out.println("   " + m)); }
      else System.out.println("OK   " + r.getArchetypeId());
    }
    System.out.println("total=" + names.size() + " failing=" + bad);
  }
}
