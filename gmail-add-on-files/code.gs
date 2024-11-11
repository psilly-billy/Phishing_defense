/**
 * Builds the add-on card with an "Analyze Email" button.
 * @param {Object} e - The event object.
 * @return {CardService.Card} - The card to display.
 */
function buildAddOn(e) {
  Logger.log(JSON.stringify(e));
  return CardService.newCardBuilder()
    .setHeader(CardService.newCardHeader().setTitle('Phishing Analyzer'))
    .addSection(CardService.newCardSection()
      .addWidget(CardService.newTextParagraph()
        .setText('Click the button below to analyze this email for phishing content.'))
      .addWidget(CardService.newTextButton()
        .setText('Analyze Email')
        .setOnClickAction(CardService.newAction()
          .setFunctionName('analyzeEmail')
          .setParameters({ messageId: e.messageMetadata.messageId }))))
    .build();
}

/**
 * Handles the "Analyze Email" button click, sends the email content to the backend for analysis,
 * and displays the result.
 * @param {Object} e - The event object.
 * @return {CardService.Card} - The card with the analysis result.
 */
function analyzeEmail(e) {
  var messageId = e.messageMetadata.messageId;
  var message = GmailApp.getMessageById(messageId);
  var emailContent = message.getPlainBody();

  // Send the email content to the Flask server
  var response = UrlFetchApp.fetch('https://gh-submision.uc.r.appspot.com/analyze-email', {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify({ content: emailContent })  // Ensure 'content' field is included
  });

  var result = JSON.parse(response.getContentText());

  return CardService.newCardBuilder()
    .setHeader(CardService.newCardHeader()
      .setTitle('Analysis Result'))
    .addSection(CardService.newCardSection()
      .addWidget(CardService.newTextParagraph()
        .setText('Classification: ' + result.classification))
      .addWidget(CardService.newTextParagraph()
        .setText('Explanation: ' + result.explanation)))
    .build();
}

