import email.utils
import smtplib  
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ppm.env import get_env_or_raise
from typing import Sequence
import logging

# Config
MAIL_HOST = 'smtp.mailgun.org'
MAIL_PORT = 587

# Rename
HOST = MAIL_HOST
PORT = MAIL_PORT

class Mailgun:    
    @classmethod
    def send_email(cls, to_addrs: Sequence[str], subject: str, body: str, sender_email_address: str, sender_name: str):
        # Get credentials
        username_smtp = get_env_or_raise('USERNAME_SMTP')
        password_smtp = get_env_or_raise('PASSWORD_SMTP')

        # Assert
        assert username_smtp and password_smtp, 'Please call setup_credentials Mailgun.setup_credentials first.'

        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = email.utils.formataddr((sender_name, sender_email_address))
        msg['To'] = ', '.join(to_addrs)

        # Record the MIME types of both parts - text/plain and text/html.
        part = MIMEText(body, 'html')
        
        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part)

        # Try to send the message.
        try:  
            server = smtplib.SMTP(HOST, PORT)
            server.ehlo()
            server.starttls()
            #stmplib docs recommend calling ehlo() before & after starttls()
            server.ehlo()
            server.login(username_smtp, password_smtp)
            server.sendmail(sender_email_address, to_addrs, msg.as_string())
            server.close()
        # Display an error message if something goes wrong.
        except Exception as e:
            logging.error(e, exc_info=True)
