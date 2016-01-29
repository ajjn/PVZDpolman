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

Add an organization with domain & authorized signing certificate. 

    echo '[{"record":["organization", "L9", "Stadt Wien"], "delete": false}]' | ./PMP.sh append -
    echo '[{"record": ["domain", "portal.wien.gv.at", "L9"], "delete": false}]' | ./PMP.sh append -
    ./PAtool.sh adminCert --orgid L9 ../tests/work/add_L9_admin_cert.json
    ./PMP.sh append ../tests/work/add_L9_admin_cert.json

Add issuer certificate (for TLS):  

    # use PAtool to pack the certificate into a JSOM-formatted PMP-input
    ./PMP.sh append <add_issuer_cert.json>
    
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

