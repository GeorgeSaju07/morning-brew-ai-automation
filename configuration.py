"""
This file contains the configuration values stored under their respective keys.
"""

import os

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
SEARCH_QUERY = 'from:(morningbrew.com OR crew@morningbrew.com OR dailybrief@morningbrew.com)'
GEMINI_MODEL = "gemini-flash-lite-latest"
UTF_8_ENCODING = "utf-8"

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
SECTIONS = ["SOURCE", "TOPIC", "KEY_FACTS", "KEY_ENTITIES",
                "MAIN_INSIGHT", "LINKEDIN_POST", "CONFIDENCE"]

LIST_OF_HEADERS = ["TOPIC", "KEY_FACTS", "KEY_ENTITIES", "MAIN_INSIGHT", "CONFIDENCE"]