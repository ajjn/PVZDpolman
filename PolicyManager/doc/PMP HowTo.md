# Policy Manager/PMP How-To

## General

Change to the bin directory to start commands
```cd $PROJ_HOME/PolicyManager/bin```

Show commandline help. Note: options -x -a -t are provided by PMP.sh - do not use those 
```./PMP.sh --help```

## Maintain the Policy Journal

Initialize the policy journal

    ./PMP.sh create

Add some policies

    ./PMP.sh append ../tests/testdata/PMPns01_pmp_input1.json

Add an organization with domain & authorized signing certificate. The signing certificate
is a PEM-file without BEGIN/END lines. (See in the next example how to obtain it.)

    echo '[{"record":["organization", "L9", "Stadt Wien"], "delete": false}]' | ./PMP.sh append -
    echo '[{"record": ["domain", "portal.wien.gv.at", "L9"], "delete": false}]' | ./PMP.sh append -
    echo -n '[{"record": ["userprivilege", "{cert}' > /tmp/$0.$$.tmp && \
    perl -pe 's/\s*//g' ../tests/testdata/r2h2_ecard_qcert.b64   >> /tmp/$0.$$.tmp && \
    echo '", "L9", "Testeroni Testimatics"], "delete": false}]' >> /tmp/$0.$$.tmp && \
    ./PMP.sh append /tmp/$0.$$.tmp && rm /tmp/$0.$$.tmp

Store the signing certificate from the citizen card.

    # start the MOCCA citizen card client. Select "Karte | Zertifikat speichern" in the menu.
    # store the certificate in the filesystem, e.g. in /tmp/qualified.cer. The convert it to PEM: 
    openssl x509 -inform der -in /tmp/name_ecard_qcert.cer -text > /tmp/name_ecard_qcert_crt.pem
 
    # open the -pem file and double check that you are taking the correct certificate.
    # Extract the lines between -----BEGIN CERTIFICATE----- and -----END CERTIFICATE----- 
    # and store the result in /tmp/name_ecard_qcert_crt.b64. 

Add issuer certificate (for TLS): use the PAtool. Or alternatively:

    echo -n '[{"record": ["issuer", "BMI Portalverbund-CA", "IDP", "' > /tmp/$0.$$.tmp && \
    perl -pe 's/\s*//g' ../tests/testdata/BMI_portalverbundCA_crt.b64   >> /tmp/$0.$$.tmp && \
    echo '"], "delete": false}]' >> /tmp/$0.$$.tmp && \
    ./PMP.sh append /tmp/$0.$$.tmp && rm /tmp/$0.$$.tmp
    
Remove issuer certificate from the policy directory:
Take the example above and change "delete": false to "delete": true

Blacklist a portal certificate (for TLS)

    ./PMP.sh append ../tests/testdata/PAT05_gondorMagwienGvAt_2011-cer_revoke.json

## Export and Display

Display what you have written to the policy journal so far (JSON)

    ./PMP.sh read --journal 

Show the policy directory (JSON). Different sorting that the journal, and
records may be updated or deleted

    ./PMP.sh read --poldirjson 

Show the policy directory (HTML). Make sure that the output file can reference
tables.css

    ./PMP.sh read --poldirhtml > ../tests/work/poldir.html 

