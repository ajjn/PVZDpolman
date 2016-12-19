# Policy Manager/PMP How-To

## Voraussetzungen

- Im Backend System (PEP) ist das Signaturzertifikat des Depositors hinterlegt.
- Das Policy Journal wurde initialisiert (`PMP.sh create`)
- Dem PMP steht die letzte Version des Policy Journals zur Verfügung (-> Git)

## Vorbereitung

Wechsel ins bin Verzeichnis:
```cd $PROJ_HOME/PolicyManager/bin```

Befehle anzeigen:

    PMP.sh --help
    # Subcommand
    PMP.sh <subcommand> --help   

Der Aufruf erfolgt immer mit PMP.sh als Wrapper für PMP.py


## Meldungen ins Policy Journal einpflegen

Policies (d.h. Organisationen, Domains, Portaladmins, ..) werden als
.json-Datei vom Portalverantwortlichen außerhalb des Systems gesichert
übermittelt. Wenn eine ordunungsgemäße Meldung eingeht, wird diese 
vom Depositar signiert und das neue Policy Journal an das Backendsystem
hochgeladen:

    PMP.sh append /transfer/PMPns01_pmp_input1.json
    git ..
    
TLS-Zertifikat für Stammportal melden

Der vom Portaldamin übermittelte EntityDescriptor wird in den entsprechenden
Directory in git hochgeladen.

Eine Organization mit Domain & Signaturzertifikat hinzufügen 

    echo '[{"record":["organization", "L9", "Stadt Wien"], "delete": false}]' | PMP.sh append -
    echo '[{"record": ["domain", "portal.wien.gv.at", "L9"], "delete": false}]' | PMP.sh append -
    ./PAtool.sh adminCert --orgid L9 ../tests/work/add_L9_admin_cert.json
    PMP.sh append ../tests/work/add_L9_admin_cert.json
    
Jeder Aufruf von PMP mit einer Änderung am Policy Journal muss signiert werden. Es können aber 
mehrere Datensätze in einem Aufruf eingegeben werden.

Issuer Zertifikat (für TLS):  

    # Mit PAtool wird zuerst das Zertifikate in einen JSON-formatierten PMP-input verpackt:
    PMP.sh append <add_issuer_cert.json>
    
Um ein Issuer Zertifikat zu entfernen:
Wie im vorhergehenden Beispiel, aber ersetze '"delete": false' durch '"delete": true'

Portal Zertifikat (TLS) sperren:

    PMP.sh append ../tests/testdata/PAT05_gondorMagwienGvAt_2011-cer_revoke.json

## Export und Anzeige

Zeige Policy Journal chronologisch (JSON):

    PMP.sh read --journal 

Zeige Policy Directory nach Keys (ohne gelöschte und überschriebene Einträge, JSON)

    PMP.sh read --poldirjson 

Zeige Policy Directory  (HTML).

    PMP.sh read --poldirhtml > ../tests/work/poldir.html 

(Outputfile muss tables.css referenzieren können)
