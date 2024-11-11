import base64
import re
from src.phishing_detection import predict_phishing
from src.phishtank import check_urls_against_phishtank
from bs4 import BeautifulSoup

def extract_urls(text):
    """Extracts URLs from the given text."""
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    urls = url_pattern.findall(text)
    return urls

def truncate_url(url, max_length=50):
    """Truncates URLs if they exceed the maximum length."""
    if len(url) > max_length:
        return url[:max_length] + '... [truncated]'
    return url

def check_phishtank_results(urls, phishing_urls):
    """Checks URLs against PhishTank separately."""
    return check_urls_against_phishtank(urls, phishing_urls)

def clean_email_content(email_content, max_length=2000):
    """Preprocesses email content to simplify structure for model prediction."""
    # Remove HTML tags and scripts using BeautifulSoup
    soup = BeautifulSoup(email_content, 'html.parser')
    for script in soup(['script', 'style', 'img', 'table']):
        script.decompose()

    # Get text content and clean unnecessary whitespace
    cleaned_text = soup.get_text(separator=' ')
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    # Truncate the content to a maximum length with key sentence extraction
    if len(cleaned_text) > max_length:
        sentences = cleaned_text.split('. ')
        cleaned_text = '. '.join(sentences[:max_length // 100]) + '... [truncated]'

    return cleaned_text

def process_email(email_content, phishing_urls):
    """Processes a plain text email content for classification and returns the results."""
    try:
        # Ensure the email content is non-empty
        if not email_content.strip():
            raise ValueError("Email content is invalid or empty.")

        # Clean the email content to simplify structure
        cleaned_content = clean_email_content(email_content)
        
        # Extract URLs from the cleaned content and truncate them for logging/verification
        urls = extract_urls(cleaned_content)
        truncated_urls = [truncate_url(url) for url in urls]
        is_phishing_url = check_phishtank_results(urls, phishing_urls)

        # Classify based on URL check and model prediction
        if is_phishing_url:
            classification = 'phishing'
            explanation = 'The email contains a known phishing URL from PhishTank.'
        else:
            print("The cleaned email content (first 500 chars):", cleaned_content[:500])  # Log truncated content for review
            prediction = predict_phishing(cleaned_content)
            classification, explanation = parse_model_response(prediction)

        return {
            'classification': classification,
            'explanation': explanation,
            'parsed_email': {
                'body_text': cleaned_content,
                'urls': truncated_urls  # Include for context but not sent to the model
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
