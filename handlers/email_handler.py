'''
    Module for basic email sending (we do not recieve emails, only regular http packets).
    Based heavily off https://medium.com/lyfepedia/sending-emails-with-gmail-api-and-python-49474e32c81f
    which outlines non-Oauth2 method of sending emails through a gmail account. 
'''

import smtplib
import ssl
import threading
from email.message import EmailMessage


EMAIL_SMTP          = "smtp.gmail.com"
EMAIL_PORT_NUMBER   = 465  # For SSL

# What's@Calu's credentials for sending emails. These are not the accounts' real password, but instead a pin setting for 2-factor auth. 
# Weirdly the 2-factor part is absent here; these are just unique pins for certain applications. Why these are allowed but insecure SMTP itself isn't is beyond me. 
EMAIL_ACCOUNT       = "whatsatcalu@gmail.com"
EMAIL_PASSWORD      = "rndozpygpsyxcgiv"
EMAIL_CONTEXT       = ssl.create_default_context()



# uses a throwaway login/connection to send a single email. Ideally can use a logged in server object via another module that's kept alive instead. 
def send_email(to: str, subject: str, body: str):
        # constructs a mail object from the parameters given (and our email handle)
        mail            = EmailMessage()
        mail['To']      = to
        mail['From']    = EMAIL_ACCOUNT
        mail['Subject'] = subject
        mail.set_content(body)

        # actually sends the mail object.
        with smtplib.SMTP_SSL(EMAIL_SMTP, EMAIL_PORT_NUMBER, context=EMAIL_CONTEXT) as server:
            server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ACCOUNT, to, mail.as_string())