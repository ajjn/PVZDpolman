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
    logging.info("connecting to smtp://%s:%s" %  (conf.SMTP_SMART_HOST, conf.SMTP_PORT))
    if conf.USE_TLS:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        ssl_context.options |= ssl.OP_NO_SSLv2
        # ssl_context.options |= ssl.OP_NO_SSLv3  # TODO: fix " tlsv1 alert decode error"
        # Taken from http://stackoverflow.com/questions/33857698/sending-email-from-python-using-starttls
        ssl_context.set_ciphers(
            'ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:'
            'DH+HIGH:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+HIGH:RSA+3DES:!aNULL:'
            '!eNULL:!MD5')
        ssl_context.set_default_verify_paths()
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        try:
            smtp_server = smtplib.SMTP_SSL(local_hostname='PVZDlivdCD', context=ssl_context)
            #


            # smtp_server.set_debuglevel(1)
            smtp_server.connect (host=conf.SMTP_SMART_HOST, port=conf.SMTP_PORT)
        except Exception as e:
            errmsg = "Connection to mail server smtp://%s:%s failed: %s" %  (conf.SMTP_SMART_HOST, conf.SMTP_PORT, str(e))
            logging.error(errmsg)
            return errmsg
        # only TLSv1 or higher
        logging.info("sending EHLO")
        smtp_server.ehlo()
        try:
            logging.info("authenticating to SMTP server")
            smtp_server.login(conf.ACCOUNT, conf.PASSWORD)
        except Exception as e:
            logging.error("Authentication to mail server failed: " + str(e))
            smtp_server.quit()
            return "Authentication to mail server failed: " + str(e)
    else:
        try:
            smtp_server = smtplib.SMTP(local_hostname='PVZDliveCD')
            smtp_server.set_debuglevel(1)
            smtp_server.connect (host=conf.SMTP_SMART_HOST, port=conf.SMTP_PORT)
        except Exception as e:
            errmsg = "Connection to mail server smtp://%s:%s failed: %s" %  (conf.SMTP_SMART_HOST, conf.SMTP_PORT, str(e))
            logging.error(errmsg)
            return errmsg
    try:
        logging.info("sending message")
        smtp_server.sendmail(conf.FROM, conf.RECIPIENT, composed)
    except Exception as e:
        logging.error('Sending message failed: ' + str(e))
        smtp_server.quit()
        return 'Sending message failed: ' + str(e)
    smtp_server.quit()
    return "OK"
