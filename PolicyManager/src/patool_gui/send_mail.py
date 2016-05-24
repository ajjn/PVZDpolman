import logging
import os
import sys
import smtplib
import ssl
# For guessing MIME type based on file name extension
import mimetypes


from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_files_via_email(conf, dir, filenames) -> str:
    """
    Send a list of files to a pre-configured address
    :param conf: ConfigReader
    :param dir: input directory
    :param filenames: files to be attachte to the mail
    :return: success message: 'OK' or error message
    """

    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = conf.TITLE
    outer['To'] = conf.RECIPIENT
    outer['From'] = conf.FROM
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    for file in filenames:
        filename = os.path.join(dir, file)
        if not os.path.isfile(filename):
            continue
        # Guess the content type based on the file's extension.  Encoding
        # will be ignored, although we should check for simple things like
        # gzip'd or compressed files.
        ctype, encoding = mimetypes.guess_type(filename)
        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        if maintype == 'text':
            with open(filename) as fp:
                # Note: we should handle calculating the charset
                msg = MIMEText(fp.read(), _subtype=subtype)
        elif maintype == 'image':
            with open(filename, 'rb') as fp:
                msg = MIMEImage(fp.read(), _subtype=subtype)
        else:
            with open(filename, 'rb') as fp:
                msg = MIMEBase(maintype, subtype)
                msg.set_payload(fp.read())
            # Encode the payload using Base64
            encoders.encode_base64(msg)
        # Set the filename parameter
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        outer.attach(msg)
    # Now send the message
    composed = outer.as_string()
    try:
        smtp_server = smtplib.SMTP(conf.SMTP_SMART_HOST, conf.SMTP_PORT)
    except Exception as e:
        logging.error( str(e) + '\nMail sending.')
        return str(e) + '\nMail sending.'
    if not conf.USE_TLS:
        try:
            smtp_server.sendmail(conf.FROM, conf.RECIPIENT, composed)
        except Exception as e:
            logging.error( str(e) + '\nMail sending.')
            return str(e) + '\nMail sending.'
    else:
        # only TLSv1 or higher
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.options |= ssl.OP_NO_SSLv2
        context.options |= ssl.OP_NO_SSLv3
        # Taken from http://stackoverflow.com/questions/33857698/sending-email-from-python-using-starttls
        context.set_ciphers(
            'ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:'
            'DH+HIGH:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+HIGH:RSA+3DES:!aNULL:'
            '!eNULL:!MD5')
        context.set_default_verify_paths()
        context.verify_mode = ssl.CERT_REQUIRED
        smtp_server.ehlo()
        if smtp_server.starttls(context=context)[0] != 220:
            return "Connection is not encrypted"
        try:
            smtp_server.login(conf.ACCOUNT, conf.PASSWORD)
        except Exception as e:
            logging.error(str(e) + '\nMail server authentication.')
            smtp_server.quit()
            return str(e) + '\nMail server authentication.'
        try:
            smtp_server.sendmail(conf.FROM, conf.RECIPIENT, composed)
        except Exception as e:
            logging.error( str(e) + '\nMail sending.')
            smtp_server.quit()
            return str(e) + '\nMail sending.'
        smtp_server.quit()
    return "OK"
