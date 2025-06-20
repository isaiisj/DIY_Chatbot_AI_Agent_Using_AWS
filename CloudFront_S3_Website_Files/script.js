// AWS Configuration 
const BOT_ID = 'A7YUJSSPSB';
const BOT_ALIAS_ID = 'TSTALIASID';
const REGION = 'us-east-1';
const IDENTITY_POOL_ID = 'us-east-1:2c29cf8d-d8e4-4cb9-8161-55071ceff2aa';

// Initialize AWS configuration
AWS.config.region = REGION;
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId: IDENTITY_POOL_ID
});

// Initialize Lex Runtime
const lexRuntime = new AWS.LexRuntimeV2();

// Main function to send messages
function sendMessage() {
    const userInput = document.getElementById('user-input');
    const messagesDiv = document.getElementById('messages');
    
    // Don't send empty messages
    if (userInput.value.trim() === '') return;
    
    // Add user message to chat
    messagesDiv.innerHTML += '<p><strong>You:</strong> ' + userInput.value + '</p>';
    
    // Auto scroll to bottom when user sends message
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    
    // Prepare parameters for Lex
    const params = {
        botId: BOT_ID,
        botAliasId: BOT_ALIAS_ID,
        localeId: 'en_US',
        sessionId: 'testUser',
        text: userInput.value
    };
    
    // Send message to Lex
    lexRuntime.recognizeText(params, (err, data) => {
        if (err) {
            // Handle errors
            console.log(err, err.stack);
            messagesDiv.innerHTML += '<p><strong>Error:</strong> ' + err.message + '</p>';
        } else {
            // Add bot response to chat
            messagesDiv.innerHTML += '<p><strong>Bot:</strong> ' + data.messages[0].content + '</p>';
        }
        // Auto scroll to bottom after bot responds
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    });
    
    // Clear input field after sending
    userInput.value = '';
}

// Event listener for Enter key
document.getElementById('user-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});