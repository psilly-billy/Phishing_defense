# src/gemini_api.py
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

def configure_gemini(api_key):
    """Configures the Gemini model and starts a chat session."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    return model.start_chat(
        
    )

def LLM_Response(chat, question):
    """Sends a prompt to the Gemini model and returns the response without safety settings."""
    safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        #HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
    }
    
    response = chat.send_message(question, stream=True, safety_settings=safety_settings)
    response.resolve()  # Ensure the response is fully generated
    return response

def generate_email_explanation(chat, email_content, classification_result, phishtank_check):
    """Generates an explanation based on the email analysis and classification."""
    prompt = (
        "You are a cybersecurity expert with deep knowledge of email phishing detection and threat analysis. "
        "Your task is to analyze the given email content and provide a detailed, user-friendly explanation "
        "based on the classification result from an AI model and a URL check against the PhishTank database.\n\n"
        
        "#CONTEXT#\n"
        "The input email has already been processed by a machine learning model that classified it as either 'phishing' or 'non-phishing'. "
        "Additionally, URLs in the email have been checked against the PhishTank database to see if they are known phishing sites.\n\n"
        
        "#OBJECTIVE#\n"
        "Analyze the given email content, the classification result, and the URL check results to craft a clear and informative explanation. "
        "Explain why the email was classified as phishing or non-phishing and what specific factors or red flags were considered. "
        "Make the explanation concise and understandable to an average user.\n\n"
        
        "## Email Content:\n"
        f"{email_content}\n\n"
        
        "## Classification Result:\n"
        f"{classification_result}\n\n"
        
        "## PhishTank Check:\n"
        f"PhishTank Result: {'Phishing URL detected' if phishtank_check else 'No known phishing URLs found'}\n\n"
        
        "#RESPONSE#\n"
        "Based on the provided information, create an analysis and explanation, keep it short and concise:\n"
    )
    response = LLM_Response(chat, prompt)
    return response.candidates[0].content.parts[0].text
