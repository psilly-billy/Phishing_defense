# src/gmail_api.py

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes define the level of access your application has.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate_gmail():
    """Authenticates and returns a Gmail API service instance."""
    creds = None
    token_path = 'token.pickle'

    # Load existing credentials if available
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # If credentials are not available or invalid, initiate the OAuth flow
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            'config/credentials.json',
            SCOPES,
            redirect_uri='http://127.0.0.1:8080/'
        )
        creds = flow.run_local_server(host='127.0.0.1', port=8080)
        # Save the credentials for future use
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    # Build the Gmail API service
    service = build('gmail', 'v1', credentials=creds)
    return service

def add_label_to_message(service, message_id, label_name):
    """Adds a label to a message, creating the label if it doesn't exist."""
    label_id = get_or_create_label(service, label_name)
    body = {
        'addLabelIds': [label_id],
        'removeLabelIds': []
    }
    message = service.users().messages().modify(userId='me', id=message_id, body=body).execute()
    return message

def get_or_create_label(service, label_name):
    """Gets a label ID by name or creates it if it doesn't exist."""
    # Get all labels
    labels = service.users().labels().list(userId='me').execute().get('labels', [])
    for label in labels:
        if label['name'] == label_name:
            return label['id']
    # Create the label
    label_body = {
        'labelListVisibility': 'labelShow',
        'messageListVisibility': 'show',
        'name': label_name
    }
    label = service.users().labels().create(userId='me', body=label_body).execute()
    return label['id']


import base64
from googleapiclient.errors import HttpError

def add_banner_to_email(service, message_id, classification, explanation):
    """Adds a banner with the analysis result to the top of the email."""
    try:
        # Create the banner HTML content
        banner_html = f"""
        <div style="background-color: #ffcccc; padding: 15px; margin-bottom: 15px; border: 1px solid #f5c6cb;">
            <strong>Phishing Analysis Result:</strong>
            <p><strong>Classification:</strong> {classification.capitalize()}</p>
            <p><strong>Explanation:</strong> {explanation}</p>
        </div>
        """

        # Get the original email content
        original_message = service.users().messages().get(userId='me', id=message_id, format='raw').execute()
        msg_str = base64.urlsafe_b64decode(original_message['raw'].encode('UTF-8'))
        email_message = msg_str.decode('utf-8')

        # Add the banner at the top of the email content
        modified_email = banner_html + email_message

        # Encode the modified email content
        encoded_email = base64.urlsafe_b64encode(modified_email.encode('utf-8')).decode('utf-8')

        # Update the email in Gmail
        service.users().messages().modify(
            userId='me',
            id=message_id,
            body={'raw': encoded_email}
        ).execute()

        print(f"Banner added to email {message_id}")

    except HttpError as error:
        print(f'An error occurred while adding the banner: {error}')
