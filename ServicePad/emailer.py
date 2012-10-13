'''
Created on Oct 13, 2012

@author: Bryan
'''
import os
import smtplib, logging
from email.MIMEText import MIMEText

PORT = os.getenv("MAILGUN_SMTP_PORT", None)
SERVER = os.getenv("MAILGUN_SMTP_SERVER",None)
USERNAME = os.getenv("MAILGUN_SMTP_LOGIN",None)
PASSWORD = os.getenv("MAILGUN_SMTP_PASSWORD",None)
DOMAIN = "servicepad.heroku.com"

FROM = "admin@servicepad.org"
TEXT_SUBTYPE = 'plain'

def send_email(To,Subject,Content):
    try:
        msg = MIMEText(Content,TEXT_SUBTYPE)
        msg['Subject'] = Subject
        msg['From'] = FROM
        smtp_obj = smtplib.SMTP(SERVER,PORT)
        smtp_obj.set_debuglevel(False)
        smtp_obj.login(USERNAME, PASSWORD)
        try:
            smtp_obj.sendmail(FROM, To, msg.as_string())
        finally:
            smtp_obj.close()
    except Exception, exc:
        logger = logging.getLogger(__name__)
        logger.error("Failed to send email: %s".format(exc))
    