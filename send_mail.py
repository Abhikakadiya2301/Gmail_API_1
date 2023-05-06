from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Set up the Gmail API client
creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/gmail.send'])
service = build('gmail', 'v1', credentials=creds)

# Construct the message
message = MIMEMultipart()
message['to'] = 'avanlukhi@gmail.com'
message['subject'] = 'Return Not Received After 25/45 Day Of Return - 312359154867_1'
body = MIMEText('''I have not received return  with  No :- 13409975666194 TYPE :- Courier Return (RTO) , as per the meesho policy If I do not receive Courier Return (RTO) return within [RTO IN 45 DAYS/ RET IN 25 DAYS], then I can raise the ticket as lost parcel. Though,  AWB No :- 13409975666194 which is still In Transit and it's been 225 days and still I didn't receive this parcel. So check this issue as soonaspossible.''')
message.attach(body)

# Attach an image file to the email (optional)
"""with open('first.png', 'rb') as f:
    img_data = f.read()
image = MIMEImage(img_data, name=os.path.basename('first.png'))
message.attach(image)"""

# Encode the message in base64
raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

# Send the message using the Gmail API
try:
    message = service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
    print(F'Sent message to user:',message)
except HttpError as error:
    print(F'An error occurred: {error}')
    message = None