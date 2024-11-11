import base64
import re
from src.phishing_detection import predict_phishing
from src.phishtank import check_urls_against_phishtank

def extract_urls(text):
    """Extracts URLs from the given text."""
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    urls = url_pattern.findall(text)
    return urls

def check_phishtank_results(urls, phishing_urls):
    """Checks URLs against PhishTank separately."""
    return check_urls_against_phishtank(urls, phishing_urls)

def process_email(email_content, phishing_urls):
    """Processes a plain text email content for classification and returns the results."""
    try:
        # Ensure the email content is non-empty
        if not email_content.strip():
            raise ValueError("Email content is invalid or empty.")
        
        # Extract URLs from the email content and check against PhishTank
        urls = extract_urls(email_content)
        is_phishing_url = check_phishtank_results(urls, phishing_urls)

        # Classify based on URL check and model prediction
        if is_phishing_url:
            classification = 'phishing'
            explanation = 'The email contains a known phishing URL from PhishTank.'
        else:
            print("The email content:", email_content[:500])  # Log truncated content for review
            prediction = predict_phishing(email_content)
            classification, explanation = parse_model_response(prediction)

        return {
            'classification': classification,
            'explanation': explanation,
            'parsed_email': {
                'body_text': email_content
            }
        }
    except Exception as e:
        print(f"Error while processing the email: {e}")
        return {
            'classification': 'error occurred while processing the email.',
            'explanation': str(e)
        }

def parse_model_response(prediction):
    """Parses the model's response to extract the classification only."""
    print("Model prediction response:", prediction)
    if hasattr(prediction, 'parts') and len(prediction.parts) > 0:
        text = prediction.parts[0].text.strip()
        print("Extracted text from prediction:", text)
    else:
        text = str(prediction).strip()

    lines = text.split('\n')
    classification = ''
    for line in lines:
        if line.strip():
            classification = line.strip()
            break

    return classification.lower(), "Explanation not provided"
