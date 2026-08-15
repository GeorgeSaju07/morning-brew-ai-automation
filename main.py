"""
This file is the Main entry point for the Morning Brew to LinkedIn automation workflow.

This file coordinates Gmail retrieval, AI content generation,
response parsing, and saving the generated LinkedIn post and analysis.
"""

import ai_content_generator
import configuration as config
import constants
import gmail_service


def main():
    """
    Execute the complete Morning Brew to LinkedIn content workflow.

    Retrieves the latest Morning Brew email, generates and parses the
    AI response, displays the analysis and LinkedIn post, and saves
    the results to local files.
    :return: None
    """

    # Connect to Gmail using the configured authentication
    print(constants.CONNECTING_TO_GMAIL)
    service = gmail_service.get_gmail_service()

    # Retrieve the latest Morning Brew email and extract its content
    print(constants.FETCHING_LATEST_EMAIL_FROM_MORNING_BREW)
    subject, date_str, content = gmail_service.get_latest_morning_brew_email(service)
    print(f"  {constants.FOUND_WITH_COLON} \"{subject}\" ({date_str})")

    # Generate a structured AI response from the email content
    print(constants.GENERATING_LINKEDIN_POST)
    raw_response = ai_content_generator.generate_linkedin_post(subject, content)

    # Parse the AI response into individual sections
    parsed = ai_content_generator.parse_structured_response(raw_response)

    # Retrieve the generated LinkedIn post from the parsed response
    # Fall back to the raw response if parsing fails
    post = parsed.get(constants.LINKEDIN_POST, raw_response)

    # Display the AI-generated analysis
    print("\n" + "=" * 60)
    print(constants.ANALYSIS)
    print("=" * 60)
    for key in config.LIST_OF_HEADERS:
        if key in parsed:
            print(f"\n{key}:\n{parsed[key]}")

    # Display the final LinkedIn post
    print("\n" + "=" * 60)
    print(constants.YOUR_LINKEDIN_POST)
    print("=" * 60)
    print(post)
    print("=" * 60)

    # Save the ready-to-publish LinkedIn post
    with open(constants.LINKDIN_POST_LATEST_FILE, constants.WRITE_METHOD, encoding=config.UTF_8_ENCODING) as f:
        f.write(post)
    print(f"\n{constants.SAVED_POST_MESSAGE}")

    # Save the complete AI response for analysis and future auditing
    with open(constants.LINKDIN_POST_ANALYSIS_FILE, constants.WRITE_METHOD, encoding=config.UTF_8_ENCODING) as f:
        f.write(raw_response)
    print(constants.SAVED_FULL_ANALYSIS_MESSAGE)


if __name__ == "__main__":
    main()