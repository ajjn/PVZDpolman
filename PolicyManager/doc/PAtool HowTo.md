# Policy Manager/PAtool How-To

## General

Change to the bin directory to start commands
```cd $PROJ_HOME/PolicyManager/bin```

Show commandline help. Note: do not use options -x -a -t (they are set by PMP.sh) 
```./PAtool.sh --help```

## Create Input Files to the PEP
All files need to be signed to provide authentic input to the PEP. See example below.

### Create a minimal EntityDescriptor from a certificate file. 

    ./PAtool.sh  \
        --entityid https://gondor.wie.gv.at/idp \
        --samlrole IDP \
        createED \
        ../tests/testdata/gondorMagwienGvAt_2017-cer.pem \
        ../tests/work/gondorMagwienGvAt_2017-ed.xml
        
### Sign EntityDescriptor 
       
    ./PAtool.sh  \
        --signed_output ../tests/work/gondorMagwienGvAt_2017-ed_sig.xml \
        signED \
        ../tests/work/gondorMagwienGvAt_2017-ed.xml

### Create a Deletion Request for an EntityDesciptor
This creates an EntiyDescriptor with the attribute pvzd:disposition="delete".

    ./PAtool.sh  \
        --entityid https://gondor.wie.gv.at/idp \
        deleteED \
        ../tests/work/gondorMagwienGvAt_2017-ed.xml

## Create Input Files to the PMP

### Create a PMP Request to blacklist a Certificate 

    ./PAtool.sh  \
        --certfile ../tests/testdata/gondorMagwienGvAt_2017-cer.pem \
        revokeCert \
        --reason testing_revocation \
        ../tests/work/gondorMagwienGvAt_2017-cer_revoke.json
        
### Create a PMP Request to add an Issuer Certificate 

    ./PAtool.sh  \
        --certfile ../tests/testdata/BMI_portalverbundCA_crt.pem \
        caCert \
        --pvprole IDP \
        ../tests/work/BMI_portalverbundCA_crt_add.json
        
### Create a PMP Request to add an Admin Certificate 

    ./PAtool.sh adminCert --orgid L9 ../tests/work/add_L9_admin_cert.json
        

        