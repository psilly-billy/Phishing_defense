#phishing_detection.py

import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def multiturn_generate_content(prompt):
    # Initialize the Vertex AI with your project and location
    vertexai.init(project="326052719550", location="us-central1")
    
    # Use from_endpoint to load the model from the specific endpoint
    model = GenerativeModel("projects/326052719550/locations/us-central1/endpoints/3853446307238641664")
    
    # Start a new chat session
    chat = model.start_chat(response_validation=False)
    
    # Set up the generation configuration and safety settings (if necessary)
    generation_config = {
        # Example configuration
        # "max_output_tokens": 8192,
        # "temperature": 1,
        # "top_p": 0.95,
    }
    safety_settings = [
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=SafetySetting.HarmBlockThreshold.OFF
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=SafetySetting.HarmBlockThreshold.OFF
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=SafetySetting.HarmBlockThreshold.OFF
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=SafetySetting.HarmBlockThreshold.OFF
        ),
    ]
    
    try:
        # Generate content based on the provided prompt
        response = chat.send_message(prompt, **generation_config)
        
        # Log the full response object for debugging
        logging.debug(f"Full response object: {response}")
        
        # Check if the response contains candidates
        if not response.candidates:
            # Log a warning and return a default message
            logging.warning(f"No candidates returned for prompt: {prompt}")
            return "Model did not provide a valid response."

        # Return the model's prediction as the response text
        return response.candidates[0].content
    
    except Exception as e:
        # Log any exceptions that occur during the message generation
        logging.error(f"Error during message generation: {e}")
        return "Error occurred while processing the email."

# src/phishing_detection.py

def predict_phishing(combined_text):
    """Predicts whether an email is phishing or legitimate using the trained model."""
    prediction = multiturn_generate_content(combined_text)
    return prediction
