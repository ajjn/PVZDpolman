# Policy Manager/PMP How-To

## Allgemein

Wechsel in das bin Directory
```cd $PROJ_HOME/PolicyManager/bin```

Commandline Hilfe anzeigen. Anmerkung: Die Optionen -x -a -t werden über Umgebungsvariable gesetzt 
```./PMP.sh --help```
```./PMP.sh <subcommand> --help```

## Policy Journal pflegen

Initialisieren

    ./PMP.sh create

Policies hinzufügen

    ./PMP.sh append ../tests/testdata/PMPns01_pmp_input1.json

Eine Organization mit Domain & Signaturzertifikat hinzufügen 

    echo '[{"record":["organization", "L9", "Stadt Wien"], "delete": false}]' | ./PMP.sh append -
    echo '[{"record": ["domain", "portal.wien.gv.at", "L9"], "delete": false}]' | ./PMP.sh append -
    ./PAtool.sh adminCert --orgid L9 ../tests/work/add_L9_admin_cert.json
    ./PMP.sh append ../tests/work/add_L9_admin_cert.json
    
Jeder Aufruf von PMP mit einer Änderung am Policy Journal muss signiert werden. Es können aber 
mehrere Datensätze in einem Aufruf eingegeben werden.

Issuer Zertifikat (für TLS):  

    # Mit PAtool wird zuerst das Zertifikate in einen JSON-formatierten PMP-input verpackt:
    ./PMP.sh append <add_issuer_cert.json>
    
Um ein Issuer Zertifikat zu entfernen:
Wie im vorhergehenden Beispiel, aber ersetze '"delete": false' durch '"delete": true'

Portal Zertifikat (TLS) sperren:

    ./PMP.sh append ../tests/testdata/PAT05_gondorMagwienGvAt_2011-cer_revoke.json

## Export und Anzeige

Zeige Policy Journal chronologisch (JSON):

    ./PMP.sh read --journal 

Zeige Policy Directory nach Keys (ohne gelöschte und überschriebene Einträge, JSON)

    ./PMP.sh read --poldirjson 

Zeige Policy Directory  (HTML).

    ./PMP.sh read --poldirhtml > ../tests/work/poldir.html 

(Outputfile muss tables.css referenzieren können)
