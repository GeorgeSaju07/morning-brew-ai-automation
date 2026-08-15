"""
This file provides utilities for processing and extracting content from Gmail messages.

This file also handles email header extraction, message body parsing,
and conversion of HTML email content into clean, readable text.
"""

import base64
import re

import constants
import configuration as config

from bs4 import BeautifulSoup


def get_header(headers, name):
    """
    This function retrieve the value of a specific email header by name.
    :param headers: List of email headers from the Gmail message.
    :param name: Name of the header to retrieve.
    :return: The header value if found; otherwise, an empty string.
    """

    # Search through the available email headers
    for h in headers:
        if h[constants.NAME].lower() == name.lower():
            return h[constants.VALUE]

    # Return an empty string if the requested header is not found
    return constants.EMPTY_STRING


def extract_body(payload):
    """
    This function extract plain-text and HTML content from a Gmail message payload.
    :param payload: Gmail message payload containing the email body and
                    its nested MIME parts.
    :return: A tuple containing the extracted plain-text and HTML content.

    """

    # Initialize variables to store plain-text and HTML content
    plain_text = constants.EMPTY_STRING
    html_text = constants.EMPTY_STRING

    def walk(part):
        """
        Allow the nested function to update the outer content variables
        """

        nonlocal plain_text, html_text

        # Identify the MIME type and encoded body data
        mime_type = part.get(constants.MIME_TYPE, constants.EMPTY_STRING)
        body_data = part.get(constants.BODY, {}).get(constants.DATA)

        # Decode and store the email body based on its MIME type
        if body_data:
            decoded = base64.urlsafe_b64decode(body_data).decode(config.UTF_8_ENCODING, errors=constants.REPLACE)
            if mime_type == constants.TEXT_PLAIN:
                plain_text += decoded
            elif mime_type == constants.TEXT_HTML:
                html_text += decoded

        # Recursively process nested MIME parts
        for sub_part in part.get(constants.PARTS, []):
            walk(sub_part)

    # Start processing the Gmail message payload
    walk(payload)

    # Return both plain-text and HTML content
    return plain_text, html_text


def html_to_clean_text(html):
    """
    This function convert HTML email content into clean, readable plain text.
    :param html: Raw HTML content extracted from the email.
    :return: Cleaned text with HTML elements removed and unnecessary
            blank lines reduced.
    """

    # Parse the HTML content
    soup = BeautifulSoup(html, constants.HTML_PARSER)

    # Remove scripts and styles that are not part of the readable content
    for tag in soup([constants.SCRIPT, constants.STYLE]):
        tag.decompose()

    # Extract readable text while preserving line breaks
    text = soup.get_text(separator="\n")

    # Collapse multiple blank lines into a single blank line
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Remove leading and trailing whitespace and return the text
    return text.strip()
