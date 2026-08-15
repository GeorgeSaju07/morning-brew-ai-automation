"""
This file defines application-wide constants used throughout the project.

This file stores reusable values such as API identifiers, file names,
error messages, and user-facing messages to maintain consistency across
the application.
"""

# Methods
WRITE_METHOD = "w"

# Constants
GMAIL = "gmail"
VERSION_NUMBER_ONE = "v1"
ME = "me"
MESSAGES = "messages"
ID = "id"
FULL = "full"
PAYLOAD = "payload"
HEADERS = "headers"
SUBJECT = "subject"
DATE = "Date"
NAME = "name"
VALUE = "value"
EMPTY_STRING = ""
MIME_TYPE = "mimeType"
BODY = "body"
DATA = "data"
REPLACE = "replace"
TEXT_PLAIN = "text/plain"
TEXT_HTML = "text/html"
PARTS = "parts"
HTML_PARSER = "html.parser"
SCRIPT = "script"
STYLE = "style"
LINKEDIN_POST = "LINKEDIN_POST"
ANALYSIS = "ANALYSIS"
YOUR_LINKEDIN_POST = "YOUR LINKEDIN POST"
FOUND_WITH_COLON = "Found:"

# File Names
TOKEN_JSON_FILE = "token.json"
CREDENTIALS_JSON_FILE = "credentials.json"
LINKDIN_POST_LATEST_FILE = "linkedin_post_latest.txt"
LINKDIN_POST_ANALYSIS_FILE = "linkedin_post_analysis.txt"

# Error Message
CONSTANTS_FILE_MISSING_ERROR_MESSAGE = "credentials.json not found. Run the Gmail setup steps first."
NO_MORNING_BREW_MESSAGE_FOUND_IN_INBOX = "No Morning Brew emails found in your inbox."
RELATABLE_CONTENT_NOT_FOUND = "Could not find readable content in the latest email."
GEMINI_API_KEY_IS_NOT_SET = ("GEMINI_API_KEY environment variable not set. "
                             "Get a free key at https://aistudio.google.com/apikey")

# Print Message
CONNECTING_TO_GMAIL = "Connecting to Gmail..."
FETCHING_LATEST_EMAIL_FROM_MORNING_BREW = "Fetching latest Morning Brew email..."
GENERATING_LINKEDIN_POST = "Generating LinkedIn post with Gemini..."
SAVED_POST_MESSAGE = "Saved post to linkedin_post_latest.txt"
SAVED_FULL_ANALYSIS_MESSAGE = "Saved full analysis to linkedin_post_analysis.txt"