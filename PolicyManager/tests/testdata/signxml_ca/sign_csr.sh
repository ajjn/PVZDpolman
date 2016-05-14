openssl x509 -req -in $1-csr.pem -CA unittest_ca-cer.pem -CAkey unittest_ca-key.pem -CAcreateserial -out $1-cer.pem -days 7300
