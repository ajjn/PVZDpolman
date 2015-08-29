package at.wien.ma14.pvzd.verifysigapi.validateXSD;

import org.xml.sax.SAXException;

import javax.xml.XMLConstants;
import javax.xml.transform.stream.StreamSource;
import javax.xml.validation.Schema;
import javax.xml.validation.SchemaFactory;
import javax.xml.validation.Validator;
import java.io.File;
import java.io.FilenameFilter;
import java.io.IOException;
//import java.util.ArrayList;
import java.util.Arrays;
//import java.util.List;
import java.util.stream.Collectors;

import static java.lang.System.out;
import static org.junit.Assert.assertTrue;

public class XmlValidator {
    private String [] xsdFiles = null;

    public XmlValidator(String schemaDir) {
        final File samlMdSchemaDir = new File(schemaDir);
        System.out.println(samlMdSchemaDir.getAbsolutePath());
        assertTrue(samlMdSchemaDir.exists());
        FilenameFilter xsdFilter = new FilenameFilter() {
            public boolean accept(File dir, String name) {
                return (name.toLowerCase().endsWith(".xsd"));
            }
        };
        final String[] schemasFiles = samlMdSchemaDir.list(xsdFilter);
        xsdFiles = new String[schemasFiles.length];
        for (int i = 0; i < schemasFiles.length; i++) {
            xsdFiles[i] = samlMdSchemaDir + File.separator + schemasFiles[i];
        }
    }

    /**
     * Validate provided XML against the XSD schema files in a given directory.
     *
     * @param xmlFilePath    Path/name of XML file to be validated;
     */
    public  void validateSchema(final String xmlFilePath) throws IOException, SAXException {
        final SchemaFactory schemaFactory = SchemaFactory.newInstance(XMLConstants.W3C_XML_SCHEMA_NS_URI);
        final StreamSource[] xsdSources = generateStreamSourcesFromXsdPaths(xsdFiles);
        assertTrue(new File(xmlFilePath).exists());
        try {
            final Schema schema = schemaFactory.newSchema(xsdSources);
            final Validator validator = schema.newValidator();
            out.println("Validating " + xmlFilePath + " against XSDs " + Arrays.toString(xsdFiles) + "...");
            validator.validate(new StreamSource(new File(xmlFilePath)));
        } catch (IOException | SAXException e) {
            out.println("ERROR: Unable to validate " + xmlFilePath + "\n" + e);
            throw e;
        }
    }

    /**
     * @param xsdFilesPaths String representations of paths/names XSD files.
     * @return array of StreamSource instances representing XSDs.
     */
    private StreamSource[] generateStreamSourcesFromXsdPaths(
            final String[] xsdFilesPaths) {
        return Arrays.stream(xsdFilesPaths)
                .map(StreamSource::new)
                .collect(Collectors.toList())
                .toArray(new StreamSource[xsdFilesPaths.length]);
    }
}

