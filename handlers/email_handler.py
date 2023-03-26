'''
    Module for basic email sending (we do not recieve emails, only regular http packets).
'''

import smtplib
import ssl
import global_values as glob
import threading

EMAIL_PORT_NUMBER   = 465  # For SSL
EMAIL_PASSWORD      = "#(*$dsLJnO461ag&@45>jAwaj-D"
EMAIL_CONTEXT       = ssl.create_default_context()





# The program that works on sending emails to potential accounts. We will not check to see if they're sent successfully. 
class CALUEmailhandlerThread(threading.Thread):
    def run(self):
        with smtplib.SMTP_SSL("smtp.gmail.com", EMAIL_PORT_NUMBER, context=EMAIL_CONTEXT) as server:
            server.login("whatsatcalu@gmail.com", EMAIL_PASSWORD)