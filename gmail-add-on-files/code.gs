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
 * and displays the result with a more modern layout.
 * @param {Object} e - The event object.
 * @return {CardService.Card} - The card with the analysis result.
 */
function analyzeEmail(e) {
  var messageId = e.messageMetadata.messageId;
  var message = GmailApp.getMessageById(messageId);
  var emailContent = message.getPlainBody();

  // Send the email content to the backend server
  var response = UrlFetchApp.fetch('https://gh-submision.uc.r.appspot.com/analyze-email', {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify({ content: emailContent })
  });

  var result = JSON.parse(response.getContentText());

  // Build the card with a modern layout
  var card = CardService.newCardBuilder()
    .setHeader(CardService.newCardHeader().setTitle('Phishing Analyzer').setSubtitle('Analysis Result'));

  // Add classification section with color indication
  var classification = result.classification === 'phishing' ? 'Phishing ⚠️' : 'Non-Phishing ✅';
  card.addSection(CardService.newCardSection()
    .addWidget(CardService.newDecoratedText()
      .setText('<b>Classification:</b> ' + classification)
      .setWrapText(true)));

  // Add explanation section with flexible display
  var explanationSection = CardService.newCardSection()
    .addWidget(CardService.newDecoratedText()
      .setText('<b>Explanation:</b>')
      .setWrapText(true))
    .addWidget(CardService.newTextParagraph()
      .setText(formatExplanation(result.explanation)));

  card.addSection(explanationSection);

  return card.build();
}

/**
 * Formats the explanation text for cleaner display, with line breaks added for readability.
 * @param {string} explanation - The explanation text from the analysis result.
 * @return {string} - Formatted explanation text with line breaks.
 */
function formatExplanation(explanation) {
  // Apply basic sanitation and formatting for readability
  var sanitizedExplanation = explanation
    .replace(/(?:\r\n|\r|\n)/g, '<br>')  // Replace line breaks with HTML breaks for clean display
    .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')  // Bold any text surrounded by **
    .replace(/(?:- |• )/g, '• ');  // Ensure bullet points are consistent

  return sanitizedExplanation;
}

