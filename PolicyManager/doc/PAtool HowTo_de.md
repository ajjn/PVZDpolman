# Policy Manager/PAtool How-To

PAtool hat 2 Funktionen:
 a) SAML Metadaten erstellen (create, sign, delete EntityDescriptors)
 b) PMP Inputdaten für das Policy Store erzeugen (Organisationen, Domains, Admin Zertifikate, Issuer Zertifiakte und Zertifikatssperren)

## Vorbereitung


Wechsel ins bin Verzeichnis
```cd $PROJ_HOME/PolicyManager/bin```

Befehle anzeigen:

    ./PAtool.sh --help
    # Subcommand
    ./PAtool.sh <subcommand> --help   
    git add $POLMAN_REPODIR/policydir/aods.xml
    git commit -m update
    git push
    
Der Aufruf erfolgt immer mit ./PAtool.sh als Wrapper für PAtool.py

Outputdateien müssen signiert werden - dafür ist ein Kartenleser und
eine Bürgerkarte erforderlich. Wenn keine Bürgerkarte vorhanden ist,
kann die eCard on-line über die Handysignatur dazu eingerichtet werden.


## TLS-Zertifikat für Stammportal melden

    ./PAtool.sh createED \
        --entityid "https://gondor.wien.gv.at/idp.xml" \
        --samlrole IDP \
        --outputdir /transfer \
        --sign \
        /transfer/mein-STP-Zertifikat-cer.pem 

Mit diesem Befehl wird das TLS-Zertifikat in einen EntityDescriptor
verpackt und signiert. Das STP muss mit einer entityID identifiziert werden,
die im zentralen ldap.gv.at einzutragen ist.


        
### Sign EntityDescriptor
For EntityDescriptor created with another tool, or edited ater creating with createED,
the file must be signed to be accepted by the PEP:
       
    ./PAtool.sh signED \
        --outputdir ../tests/work/ \
        ../tests/work/gondorWienGvAt_idp-unsigned.xml

### Create and sign a deletion request for an EntityDesciptor
This creates an EntiyDescriptor with the attribute pvzd:disposition="delete".

    ./PAtool.sh deleteED \
        --entityid https://gondor.wien.gv.at/idp \
        --outputdir ../tests/work/ \
        ../tests/work/

## Create Input Files to the PMP

### Create a PMP Request to blacklist a Certificate 

    ./PAtool.sh revokeCert \
        --certfile ../tests/testdata/gondorMagwienGvAt_2017-cer.pem \
        --reason testing_revocation \
        ../tests/work/gondorMagwienGvAt_2017-cer_revoke.json
        
### Create a PMP Request to add an Issuer Certificate
Certificates contained in EntityDescriptors must validate against issuer certificates. The full
chain of root and intermediate issuer certificates must be included in the policy directory.

    ./PAtool.sh caCert \
        --certfile ../tests/testdata/BMI_portalverbundCA_crt.pem \
        --pvprole IDP \
        ../tests/work/BMI_portalverbundCA_crt_add.json
        
### Create a PMP Request to add an Admin Certificate 

    ./PAtool.sh adminCert --orgid L9 ../tests/work/add_L9_admin_cert.json   # requires a challenge to be signed
    ./PAtool.sh adminCert --orgid L9 -c ../testdata/PAT/08/ecard_qcert.pem ../tests/work/add_L9_admin_cert.json   # requires a the signing cert as PEM or Base64 file
        

        