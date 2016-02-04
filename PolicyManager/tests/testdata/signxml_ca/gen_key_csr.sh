openssl req -out $1-csr.pem -pubkey -new -keyout $1-key.pem
openssl rsa -in $1-key.pem > $1-key.pem.tmp
mv $1-key.pem.tmp $1-key.pem
