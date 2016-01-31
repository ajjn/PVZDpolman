# Policy Manager/PAtool How-To

## General

Change to the bin directory to start commands
```cd $PROJ_HOME/PolicyManager/bin```

Show commandline help. 

    ./PAtool.sh --help
    # then, select a subcommand and run
    ./PAtool.sh <subcommand> --help    

Note: do not use options -x -a -t (they are set by PMP.sh) 

## Create Input Files to the PEP
All files need to be signed to provide authentic input to the PEP. See example below.

### Create a minimal EntityDescriptor from a certificate file. 

    ./PAtool.sh createED \
        --entityid https://gondor.wie.gv.at/idp \
        --samlrole IDP \
        ../tests/testdata/gondorMagwienGvAt_2017-cer.pem \
        ../tests/work/gondorMagwienGvAt_2017-ed.xml
        
### Sign EntityDescriptor 
       
    ./PAtool.sh signED \
        --signed_output ../tests/work/gondorMagwienGvAt_2017-ed_sig.xml \
        ../tests/work/gondorMagwienGvAt_2017-ed.xml

### Create a Deletion Request for an EntityDesciptor
This creates an EntiyDescriptor with the attribute pvzd:disposition="delete".

    ./PAtool.sh deleteED \
        --entityid https://gondor.wie.gv.at/idp \
        ../tests/work/gondorMagwienGvAt_2017-ed.xml

## Create Input Files to the PMP

### Create a PMP Request to blacklist a Certificate 

    ./PAtool.sh revokeCert \
        --certfile ../tests/testdata/gondorMagwienGvAt_2017-cer.pem \
        --reason testing_revocation \
        ../tests/work/gondorMagwienGvAt_2017-cer_revoke.json
        
### Create a PMP Request to add an Issuer Certificate 

    ./PAtool.sh caCert \
        --certfile ../tests/testdata/BMI_portalverbundCA_crt.pem \
        --pvprole IDP \
        ../tests/work/BMI_portalverbundCA_crt_add.json
        
### Create a PMP Request to add an Admin Certificate 

    ./PAtool.sh adminCert --orgid L9 ../tests/work/add_L9_admin_cert.json
        

        