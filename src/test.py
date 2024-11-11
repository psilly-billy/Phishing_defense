# src/test.py
from phishing_detection import predict_phishing

def test_predict_phishing():
    # Sample email text for testing
    test_email_text = """
    Subject: Important - Update Your Account Information

    Dear user, we noticed unusual activity in your account. Please click the link below to verify your account information to avoid suspension.

    http://suspicious-link.com/verify
    """

    # Get the model's response for the sample email
    prediction = predict_phishing(test_email_text)
    
    # Print the model's classification and explanation
    print("Model Prediction Output:")
    print(prediction)

# Run the test
test_predict_phishing()
