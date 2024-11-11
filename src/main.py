# src/main.py

from src.gmail_api import authenticate_gmail
from src.email_processing import list_messages, get_message, process_email, handle_classification, extract_urls
from src.phishtank import load_phishtank_data
from src.gemini_api import configure_gemini, generate_email_explanation
from src.config_loader import load_credentials 
from src.phishtank import check_urls_against_phishtank

def main():
    # Load the Gemini API key from credentials
    api_key = load_credentials()

    # Configure the Gemini model with the loaded API key
    chat = configure_gemini(api_key)

    # Authenticate with Gmail API
    service = authenticate_gmail()

    # Define your email query (e.g., unread emails)
    query = 'is:unread'  # Modify as needed

    # Load PhishTank data
    phishing_urls = load_phishtank_data()

    # List messages matching the query
    messages = list_messages(service, query=query)
    print(f'Found {len(messages)} messages.')

    for msg in messages:
        email_message = get_message(service, msg['id'])
        if email_message:
            # Process the email and get the classification result
            email_result = process_email(email_message, phishing_urls)

            # Generate an explanation using Gemini
            explanation = generate_email_explanation(
                chat,
                email_result['parsed_email']['body_text'],
                email_result['classification'],
                check_urls_against_phishtank(extract_urls(email_result['parsed_email']['body_text']), phishing_urls)
            )
            email_result['explanation'] = explanation

            # Handle classification (label and move if phishing)
            handle_classification(service, email_result, msg['id'])
            print(f"Email {msg['id']} classified as {email_result['classification']}")
            print(f"Explanation: {email_result['explanation']}")
        else:
            print(f"Failed to retrieve email {msg['id']}")

if __name__ == '__main__':
    main()
