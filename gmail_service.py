"""
This File Handles Gmail integration for retrieving and processing Morning Brew emails.

This file also manages Gmail authentication, fetches the latest Morning Brew
email, and extracts its subject, date, and readable content for further
AI-powered processing.
"""

import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import configuration as config
import constants
import gmail_processor


def get_gmail_service():
    """
    This function authenticate the application with the Gmail API and return an
    authorized Gmail API service instance.
    :return: An authorized Gmail API service instance that can be used to
            interact with the user's Gmail account.
    """

    # Initialize credentials
    creds = None

    # Load previously saved OAuth credentials, if available
    if os.path.exists(constants.TOKEN_JSON_FILE):
        creds = Credentials.from_authorized_user_file(constants.TOKEN_JSON_FILE, config.SCOPES)

    # Validate existing credentials or initiate authentication
    if not creds or not creds.valid:

        # Refresh expired credentials when a refresh token is available
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:

            #  A new OAuth flow requires the Google API client credentials
            if not os.path.exists(constants.CREDENTIALS_JSON_FILE):
                raise FileNotFoundError(constants.CONSTANTS_FILE_MISSING_ERROR_MESSAGE)

            # Initiate the local OAuth authentication flow
            flow = InstalledAppFlow.from_client_secrets_file(constants.CREDENTIALS_JSON_FILE, config.SCOPES)
            creds = flow.run_local_server(port=0)

        #  Save the credentials for reuse in future executions
        with open(constants.TOKEN_JSON_FILE, constants.WRITE_METHOD) as f:
            f.write(creds.to_json())

    # Build and return the authenticated Gmail API service
    return build(constants.GMAIL, constants.VERSION_NUMBER_ONE, credentials=creds)



def get_latest_morning_brew_email(service):
    """
    This method Fetch the most recent Morning Brew email from Gmail and extract
    its subject, date, and readable content.
    :param service: Authenticated Gmail API service instance.
    :return: A tuple containing the email subject, date, and cleaned content.
    """

    # Search Gmail for the latest Morning Brew email
    results = service.users().messages().list(userId=constants.ME, q=config.SEARCH_QUERY, maxResults=1).execute()

    # Retrieve the list of matching email messages
    messages = results.get(constants.MESSAGES, [])
    if not messages:
        raise RuntimeError(constants.NO_MORNING_BREW_MESSAGE_FOUND_IN_INBOX)

    # Fetch the complete content of the latest email
    msg = service.users().messages().get(userId=constants.ME,
                                         id=messages[0][constants.ID],
                                         format=constants.FULL).execute()

    # Extract the email subject and date from the message headers
    headers = msg[constants.PAYLOAD].get(constants.HEADERS, [])
    subject = gmail_processor.get_header(headers, constants.SUBJECT)
    date_str = gmail_processor.get_header(headers, constants.DATE)

    # Extract both plain-text and HTML content from the email
    plain_text, html_text = gmail_processor.extract_body(msg[constants.PAYLOAD])

    # Use plain-text content when available; otherwise convert HTML to text
    if plain_text.strip():
        content = plain_text
    elif html_text.strip():
        content = gmail_processor.html_to_clean_text(html_text)
    else:
        raise RuntimeError(constants.RELATABLE_CONTENT_NOT_FOUND)

    # Return the email details for further processing
    return subject, date_str, content
