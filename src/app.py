import logging
from flask import Flask, request, jsonify
from src.email_processing import process_email
from src.phishtank import load_phishtank_data
from src.gemini_api import configure_gemini, generate_email_explanation

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Set to DEBUG for more detailed output
logger = logging.getLogger(__name__)

# Initialize Gemini API chat session
api_key = ""  # Replace with your actual API key
chat = configure_gemini(api_key)

@app.route('/analyze-email', methods=['POST'])
def analyze_email():
    try:
        data = request.json
        email_content = data.get('content')
        if not email_content:
            logger.error("Email content not provided.")
            return jsonify({"error": "Email content not provided"}), 400
        
        # Load PhishTank data
        phishing_urls = load_phishtank_data()

        # Process the email content
        email_result = process_email(email_content, phishing_urls)
        
        # Extract details for explanation
        classification_result = email_result.get('classification', 'Unknown')
        is_phishing_url_detected = 'Phishing URL detected' in email_result.get('explanation', '')

        # Generate explanation using Gemini API
        explanation = generate_email_explanation(chat, email_content, classification_result, is_phishing_url_detected)
        email_result['explanation'] = explanation

        logger.info(f"Email processed successfully: {email_result}")
        return jsonify(email_result), 200

    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        return jsonify({
            "classification": "error occurred while processing the email.",
            "explanation": "Explanation not provided due to an internal error."
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
