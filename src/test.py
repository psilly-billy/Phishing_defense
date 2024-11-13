# src/test.py
from phishing_detection import predict_phishing

def test_predict_phishing():
    # Sample email text for testing
    test_email_text = """
    Subject: Important - Update Your Account Information

 ---------- Forwarded message --------- From: Workday - MMC <mmc@myworkday.com> Date: Tue, 29 Oct 2024 at 04:45 Subject: Application status update - R_276938 Python Engineer - Network and Security @MMCTech at Marsh To: <m.iurea@gmail.com> Dear Robert Marian, Thank you for your interest in the position of Python Engineer - Network and Security @MMCTech . After careful evaluation of the qualifications and experience required, you have unfortunately not been selected to continue with the application process. We appreciate the time you took to explore opportunities within the organization and hope you will continue to view Marsh as a future employer. Please continue to visit https://careers.mmc.com to view all available opportunities. Best of luck with your career search. Marsh Recruitment Team Replies to this message are undeliverable and will not reach the Human Resource Department. Please do not reply. This email was intended for m.iurea@gmail.com
    """

    # Get the model's response for the sample email
    prediction = predict_phishing(test_email_text)
    
    # Print the model's classification and explanation
    print("Model Prediction Output:")
    print(prediction)

# Run the test
test_predict_phishing()
