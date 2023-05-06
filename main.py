import json
import pickle

import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# set up the Google API client
CLIENT_SECRETS_FILE = 'web_credentials.json'
SCOPES = ['https://mail.google.com/']
API_VERSION = 'v1'
SERVICE_NAME = 'gmail'
state = "state"
# create a Flow object to handle the OAuth 2.0 flow
flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=SCOPES,
    redirect_uri='https://app.buissmaster.com',
    state="state"
)

auth_url, _ = flow.authorization_url(prompt='consent')
print('Please go to this URL and authorize the application: {}'.format(auth_url))

response = requests.post(auth_url)
# # wait for the user to complete the authorization flow and enter the code
authorization_response = input('Enter the full authorization code: ')

# # exchange the authorization code for an access token
flow.fetch_token(authorization_response=authorization_response)

# # save the access token to a file or database
creds = flow.credentials
# # for example, to save the access token to a file:
with open('token.pickle', 'wb') as token_file:
    pickle.dump(creds, token_file)
    # Load the pickle file
with open('token.pickle', 'rb') as f:
    creds = pickle.load(f)

# Convert the creds object to a dictionary
creds_dict = {
    'token': creds.token,
    'refresh_token': creds.refresh_token,
    'token_uri': creds.token_uri,
    'client_id': creds.client_id,
    'client_secret': creds.client_secret,
    'scopes': creds.scopes
}
creds_json = json.dumps(creds_dict)
# print(creds_json)
with open("token.json", "w") as file:
    file.write(creds_json)
# # create a Gmail API client with the access token
if creds and creds.expired and creds.refresh_token:
    creds.refresh(Request())
#
service = build(SERVICE_NAME, API_VERSION, credentials=creds)