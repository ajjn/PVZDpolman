# Policy ManagePAtool How-To
PAtool has 2 functions:
 a) generate input for the PEP (create, sign, delete EntityDescriptors)
 b) generate input for the PMP (create policy entries for issuer certs, admins and revocations)

## General

Change to the bin directory to start commands
```cd $PROJ_HOME/PolicyManager/bin```

Show commandline help. 

    PAtool.sh --help
    # then, select a subcommand and run
    PAtool.sh <subcommand> --help    

Note: do not use options -x -a -t (they are set by PMP.sh) 

## Create Input Files to the PEP
All files need to be signed to provide authentic input to the PEP. See example below.
Files MUST follow a strict naming convention. File names are derived from the entityId in the file:
    filename := camelCaseForSeperators(FQDN) "_" camelCaseForSeperators(path) ".xml"
    FQDN := hostname part of the entityId URL
    Path := path part of the entityId URL
    camelCaseForSeperators := transformation with 2 steps:
        1. change the character after a separator to uppercase
        2. remove all separators
    separator: '.', '/'
Example:
    EntityId = https://gondor.wien.gv.at/idp
    Filename = gondorWienGvAt_idp.xml


### Createand sign a minimal EntityDescriptor from a certificate file. 
To create the file ../tests/work/gondorWienGvAt_idpXml.xml us this commmand:

    PAtool.sh createED \
        --entityid https://gondor.wien.gv.at/idp.xml \
        --samlrole IDP \
        --outputdir ../tests/work/ \
        --sign \
        ../tests/testdata/gondorMagwienGvAt_2017-cer.pem 

        
### Sign EntityDescriptor
For EntityDescriptor created with another tool, or edited ater creating with createED,
the file must be signed to be accepted by the PEP:
       
    PAtool.sh signED \
        --outputdir ../tests/work/ \
        ../tests/work/gondorWienGvAt_idp-unsigned.xml

### Create and sign a deletion request for an EntityDesciptor
This creates an EntiyDescriptor with the attribute pvzd:disposition="delete".

    PAtool.sh deleteED \
        --entityid https://gondor.wien.gv.at/idp \
        --outputdir ../tests/work/ \
        ../tests/work/

## Create Input Files to the PMP

### Create a PMP Request to blacklist a Certificate 

    PAtool.sh revokeCert \
        --certfile ../tests/testdata/gondorMagwienGvAt_2017-cer.pem \
        --reason testing_revocation \
        ../tests/work/gondorMagwienGvAt_2017-cer_revoke.json
        
### Create a PMP Request to add an Issuer Certificate
Certificates contained in EntityDescriptors must validate against issuer certificates. The full
chain of root and intermediate issuer certificates must be included in the policy directory.

    PAtool.sh caCert \
        --certfile ../tests/testdata/BMI_portalverbundCA_crt.pem \
        --pvprole IDP \
        ../tests/work/BMI_portalverbundCA_crt_add.json
        
### Create a PMP Request to add an Admin Certificate 

    PAtool.sh adminCert --orgid L9 ../tests/work/add_L9_admin_cert.json   # requires a challenge to be signed
    PAtool.sh adminCert --orgid L9 -c ../testdata/PAT/08/ecard_qcert.pem ../tests/work/add_L9_admin_cert.json   # requires a the signing cert as PEM or Base64 file
        

        