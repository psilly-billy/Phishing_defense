# Phishing Analyzer 

## Overview
Phishing Analyzer is a Gmail add-on designed to help users identify and analyze potentially malicious emails. Leveraging a fine-tuned model trained using Vertex AI and integrating the Gemini API, this tool classifies emails as either phishing or non-phishing and provides detailed explanations for its classifications. Additionally, it checks URLs against the PhishTank database to identify known phishing links. 

The motivation behind this project stemmed from personal experience, where phishing attempts targeted non-technical family members. This tool aims to provide an extra layer of security and clarity to email users by offering insights into potentially harmful communications.

**Note:** The Gmail add-on has been submitted for publishing. Once approved, a direct link to access it will be provided here.

## Features
- **Phishing Classification**: Analyzes email content and classifies it as phishing or non-phishing.
- **Detailed Explanations**: Utilizes the Gemini API to generate comprehensive explanations for the classification results.
- **PhishTank URL Check**: Verifies URLs within the email body against the PhishTank database.
- **User-Friendly Interface**: Easily integrates with Gmail for convenient email analysis.

## Built With
- **Programming Languages**: Python, JavaScript (Google Apps Script)
- **Frameworks**: Flask
- **Platforms**: Google Cloud Platform (GCP), Vertex AI, Google Workspace Add-ons
- **Databases**: PhishTank for URL checking
- **APIs**: Gemini API, Gmail API
- **Deployment**: Cloud Run

## How It Works
1. The Gmail add-on app is installed and integrated with the user's Gmail account.
2. When an email is opened, the add-on presents an "Analyze Email" button.
3. Upon clicking, the add-on extracts the email content and sends it to a backend server hosted on Google Cloud Run.
4. The backend processes the email:
   - Checks URLs against the PhishTank database.
   - Sends the processed content to a fine-tuned AI model for classification.
   - Uses the Gemini API to provide an explanation for the analysis.
5. The classification result and explanation are displayed to the user.

## Installation and Usage
### Prerequisites
- A Google account with access to Gmail.
- Permissions to install Google Workspace add-ons.

### Steps to Install and Run the Gmail Add-on Locally
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/phishing-analyzer.git
   cd phishing-analyzer
   ```
2. **Set up Google Apps Script project**:
   - Navigate to [Google Apps Script](https://script.google.com/).
   - Create a new project and paste the content of `code.gs` into the script editor.
   - Copy the content of `appsscript.json` into the app's manifest file.

3. **Deploy the project**:
   - Save and deploy the script as a test add-on.
   - Enable the Gmail API and set up necessary OAuth scopes as specified in the `appsscript.json` file.

4. **Run the backend server**:
   - Deploy the Flask server using Cloud Run or run it locally for development.

### Analyzing an Email
- Open Gmail and access an email.
- Click the "Analyze Email" button provided by the add-on.
- View the classification and explanation displayed by the tool.

## Challenges Faced
- **Email Parsing**: Handling complex email formats, including embedded images and graphics, posed significant challenges during development.
- **Model Fine-Tuning**: Experimenting with various datasets and adjusting the model for optimal classification accuracy.
- **Integration**: Ensuring seamless communication between the Gmail add-on and the backend server.

## Future Enhancements
- Improve email parsing to handle more complex formats.
- Add support for more languages and email types.
- Provide real-time updates on phishing threats and new URL checks.

## License
This project is licensed under the MIT License.

## Contact
For any questions or feedback, please reach out at m.iurea@gmail.com

---
Stay tuned for the official link to the published Gmail add-on once it is approved!

