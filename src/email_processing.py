import re
import html
from src.phishing_detection import predict_phishing
from src.phishtank import check_urls_against_phishtank


def sanitize_text(text):
    """Sanitize text to handle problematic characters and replace contractions."""
    # Decode HTML entities
    text = html.unescape(text)
    
    # Replace curly quotes with straight quotes for consistency
    text = text.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')
    
    # Define a dictionary for common contractions
    contractions = {
        "it's": "it is",
        "don't": "do not",
        "I'm": "I am",
        "can't": "cannot",
        "you're": "you are",
        "we're": "we are",
        "they're": "they are",
        "I've": "I have",
        "that's": "that is",
        "there's": "there is",
        "wouldn't": "would not",
        "shouldn't": "should not",
        "couldn't": "could not",
        "won't": "will not",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "haven't": "have not",
        "hasn't": "has not",
        "hadn't": "had not",
        "you'd": "you would",
        "she'd": "she would",
        "he'd": "he would",
        "it'd": "it would",
        "we'd": "we would",
        "they'd": "they would",
        "you'll": "you will",
        "she'll": "she will",
        "he'll": "he will",
        "it'll": "it will",
        "we'll": "we will",
        "they'll": "they will",
        "I'd": "I would",
        "we've": "we have",
    }
    
    # Replace contractions
    for contraction, full_form in contractions.items():
        text = re.sub(r"\b" + re.escape(contraction) + r"\b", full_form, text, flags=re.IGNORECASE)

    # Replace non-breaking spaces if needed
    text = text.replace("\u00A0", " ")

    return text

def format_email_content(subject, body):
    """Formats the email content to match the training data format."""
    sanitized_subject = sanitize_text(subject)
    sanitized_body = sanitize_text(body)
    return f"Email Subject: {sanitized_subject}\n\nEmail Body: {sanitized_body}\n\nIs this email a phishing email or not?"

def process_email(email_content, phishing_urls):
    """Processes a plain text email content for classification and returns the results."""
    try:
        # Ensure the email content is non-empty
        if not email_content.strip():
            raise ValueError("Email content is invalid or empty.")
        
        # Attempt to split into subject and body using simple heuristics
        lines = email_content.strip().splitlines()
        subject = lines[0] if lines else "No Subject"
        body = "\n".join(lines[1:]) if len(lines) > 1 else "No Body"

        # Format the email for model input
        formatted_content = format_email_content(subject, body)

        # Extract URLs from the body text and check against PhishTank
        urls = extract_urls(body)
        is_phishing_url = check_phishtank_results(urls, phishing_urls)

        # Classify based on URL check and model prediction
        if is_phishing_url:
            classification = 'phishing'
            explanation = 'The email contains a known phishing URL from PhishTank.'
        else:
            prediction = predict_phishing(formatted_content)
            classification, explanation = parse_model_response(prediction)

        return {
            'classification': classification,
            'explanation': explanation,
            'parsed_email': {
                'subject': subject,
                'body_text': body
            }
        }
    except Exception as e:
        print(f"Error while processing the email: {e}")
        return {
            'classification': 'error occurred while processing the email.',
            'explanation': str(e)
        }


def extract_urls(text):
    """Extracts URLs from the given text."""
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    urls = url_pattern.findall(text)
    return urls

def check_phishtank_results(urls, phishing_urls):
    """Checks URLs against PhishTank separately."""
    return check_urls_against_phishtank(urls, phishing_urls)



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
