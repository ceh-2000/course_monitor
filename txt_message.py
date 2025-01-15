"""
Inspired by this Medium post: https://medium.com/testingonprod/how-to-send-text-messages-with-python-for-free-a7c92816e1a4
"""
import json
import smtplib

CARRIERS = {
    "att": "@mms.att.net",
    "tmobile": "@tmomail.net",
    "verizon": "@vtext.com",
    "sprint": "@messaging.sprintpcs.com"
}

EMAIL_KEY = 'email'
PASSWORD_KEY = 'password'
PHONE_KEY = 'phone_number'
CARRIER_KEY = 'carrier'
SMTP_GMAIL_KEY = "smtp.gmail.com"

PORT_NUMBER = 587

EMAIL_SETUP_FILE = 'email_setup.json'

class MessageManager():
    def __init__(self):
        setup_data = self.setup_messages()
        self.server = setup_data[0]
        self.sender = setup_data[1]
        self.recipient = setup_data[2]

    def setup_messages(self):
        with open(EMAIL_SETUP_FILE, 'r') as f:
            # Load the JSON data into a Python dictionary
            data = json.load(f)
            email = data[EMAIL_KEY]
            password = data[PASSWORD_KEY]
            phone_number = data[PHONE_KEY]

            recipient = phone_number + CARRIERS[data[CARRIER_KEY]]

            server = smtplib.SMTP(SMTP_GMAIL_KEY, PORT_NUMBER)
            server.starttls()

            print(email, password)
            server.login(email, password)

            return server, email, recipient

    def send_message(self, message):
        self.server.sendmail(self.sender, self.recipient, message)

if __name__ == '__main__':
    # Text the messaging
    message_manager = MessageManager()
    message_manager.send_message('Hello world!')