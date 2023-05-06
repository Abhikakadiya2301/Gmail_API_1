import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set up credentials
creds = Credentials.from_authorized_user_file("token.json")

# Create Gmail API client
service = build('gmail', 'v1', credentials=creds)

def send_email(to, subject, body):
    try:
        message = MIMEMultipart()
        text = MIMEText(body)
        message.attach(text)
        message['to'] = to
        message['subject'] = subject

        # Create the message using the API
        create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
        send_message = (service.users().messages().send(userId="me", body=create_message).execute())
        print(F'sent message to {to} Message Id: {send_message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    return send_message


to = "abhihkakadiya2301@gmail.com"
subject = "Test email"
body = "This is a test email sent through the Gmail API"
send_email(to, subject, body)