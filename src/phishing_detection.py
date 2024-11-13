import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Configuration for generation
generation_config = {
    "max_output_tokens": 10,
    "temperature": 1,
    "top_p": 0.95,
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

def single_turn_generate_content(prompt):
    # Initialize Vertex AI project and location
    vertexai.init(project="326052719550", location="europe-west2")
    
    # Load the model from the specific endpoint
    model = GenerativeModel("projects/326052719550/locations/europe-west2/endpoints/5019354143681150976")
    
    # Start a new chat session
    chat = model.start_chat(response_validation=False)

    try:
        # Generate content based on the prompt
        response = chat.send_message(prompt, generation_config=generation_config, safety_settings=safety_settings)
        
        # Log the full response object
        logging.debug(f"Full response object: {response}")
        
        # Check if response has candidates and handle empty response
        if response.candidates and len(response.candidates) > 0:
            return response.candidates[0].content
        else:
            logging.warning("No candidates returned by the model.")
            return "Model did not provide a valid response."
    
    except Exception as e:
        logging.error(f"Error during message generation: {e}")
        return "Error occurred while processing the email."

def predict_phishing(combined_text):
    """Predicts whether an email is phishing or legitimate using the trained model."""
    logging.debug(f"Predicting phishing status for content: {combined_text[:500]}")
    prediction = single_turn_generate_content(combined_text)
    return prediction
