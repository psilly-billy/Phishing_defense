# Phishing Analyzer

Phishing Analyzer is a Gmail add-on that helps users analyze emails for potential phishing content. It integrates a fine-tuned generative AI model deployed on Vertex AI for email classification, checks URLs against the PhishTank database, and provides a detailed explanation using the Google Generative AI (Gemini API). This tool aims to safeguard users by identifying phishing emails that may bypass traditional spam filters.

## Features
- **Email Classification**: Classifies emails as "phishing" or "non-phishing" using a fine-tuned AI model.
- **PhishTank URL Check**: Verifies URLs within emails against the PhishTank database to detect known phishing sites.
- **Detailed Explanations**: Uses the Gemini API to generate user-friendly explanations for the classification.
- **Gmail Integration**: Works directly within Gmail, providing an intuitive and seamless user experience.

## Built With
- **Languages & Frameworks**: Python, JavaScript (Google Apps Script)
- **Cloud Services**: Google Cloud Run, Vertex AI, Google Apps Script, Flask
- **Databases**: PhishTank database (for URL verification)
- **APIs**: Gmail API, Google Generative AI (Gemini API), UrlFetchApp (for external requests)

## How to Run the Project
### Backend Setup (Flask Application)
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/phishing-analyzer.git
   cd phishing-analyzer
   ```

2. **Install Dependencies**:
   Ensure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Deploy the Flask App**:
   Deploy the Flask app on Google Cloud Run or your preferred platform.

### Frontend Setup (Gmail Add-on)
1. **Open Google Apps Script**:
   - Go to [Google Apps Script](https://script.google.com/).
   - Create a new project.

2. **Add Code**:
   - Copy and paste the `code.gs` content into the script editor.

3. **Add appsscript.json Configuration**:
   - Replace the `appsscript.json` file in the project with the provided configuration.

4. **Set Up Permissions and Scopes**:
   Ensure that the add-on has the following OAuth scopes:
   ```json
   "oauthScopes": [
     "https://www.googleapis.com/auth/gmail.addons.execute",
     "https://www.googleapis.com/auth/gmail.readonly",
     "https://www.googleapis.com/auth/gmail.modify",
     "https://www.googleapis.com/auth/script.external_request"
   ]
   ```

5. **Deploy the Add-on**:
   - Click on **Deploy > Test deployments**.
   - Install the add-on in your Gmail account for testing.

## Tutorial: Creating and Running the Gmail Add-on
1. **Create a New Project**:
   - Go to [Google Apps Script](https://script.google.com/).
   - Click on **New Project** and name it "Phishing Analyzer".

2. **Add the Code**:
   - Copy the content of `code.gs` and paste it into the Code Editor.

3. **Configure appsscript.json**:
   - Replace the default `appsscript.json` content with the provided configuration.

4. **Grant Permissions**:
   - Ensure that the necessary scopes and advanced Gmail services are enabled.

5. **Deploy and Test**:
   - Click on **Deploy > Test deployments**.
   - Select **Install add-on** and authorize the required permissions.

6. **Run the Add-on**:
   - Open Gmail and view an email.
   - Click on the Phishing Analyzer icon in the add-on sidebar.
   - Click "Analyze Email" to send the email content to the backend and view the analysis result.

## Challenges Faced
- **Parsing Complex Emails**: Parsing emails with embedded images and complex formatting posed challenges. Ensuring consistent and simplified input for the AI model was essential.
- **Integrating Multiple Services**: Coordinating the Gmail API, Google Cloud Run, Vertex AI, and the Gemini API required careful planning and implementation.

## Future Work
- Enhance parsing capabilities for handling complex email formats.
- Implement more detailed logging and error-handling mechanisms.
- Expand support for additional language processing models.

## Conclusion
Phishing Analyzer is designed to protect users by providing an easy-to-use tool for analyzing potentially harmful emails. This project bridges advanced machine learning capabilities with user-centric security solutions, empowering users to make informed decisions about their email communications.

## License
This project is licensed under the MIT License.

---

For more detailed steps, please refer to the [official documentation](link-to-docs) or contact [your-email@example.com](mailto:your-email@example.com) for support.

