<h1>Chatbot AI Agent Using AWS</h1>
<h2>Problem or Challenge</h2>
<p>Applications/services must be protected in case of a disaster or emergency. to design the architecture of this applications employees often need access to critical information related to disaster recovery, business continuity, and safety recommendations. However, this information is currently scattered across various resources, wikis, and documentation. Employees often struggle to find the right information when they need it the most.</p>
<h2>Proposed Solution</h2>
<h3>Final Architecture</h3>
<img src= "Chatbot_AI_Agent.png">
<ol>
  <li><strong>Initial User Interaction:</strong></li>
  <ul>
    <li>User accesses website through CloudFront</li>
    <li>CloudFront serves static website from S3 (HTML, CSS, JS files)</li>
    <li>Cognito handles user authentication/permissions and provide necessary AWS credentials</li>
    <li>Frontend sends query to Lex through authenticated connection</li>
  </ul>
  <li><strong>Lex Intent Check:</strong></li>
  <ul>
    <li>Lex analyzes query to identify intent</li>
    <li>Determines what kind of information user is seeking</li>
    <li>If Lex has matching intent → provides direct response</li>
    <li>If no matching intent → forwards to Lambda function</li>
  </ul>
  <li><strong>Lambda Initial Processing:</strong></li>
  <ul>
    <li>ConversationalRetrievalChain used</li>
    <li>Calls Bedrock (first LLM) to formulate search prompt</li>
    <li>Uses conversation history</li>
  </ul>
  <li><strong>Kendra Search:</strong></li>
  <ul>
    <li>Lambda sends prompt to Kendra retrieve API</li>
    <li>Kendra searches through documents in S3</li>
    <li>Kendra returns relevant context passages</li>
  </ul>
  <li><strong>Response Generation:</strong></li>
  <ul>
    <li>Lambda sends prompt + Kendra context to Bedrock (second LLM)</li>
    <li>Bedrock uses search results to generate natural response</li>
    <li>Different LLM used for response generation</li>
    <li>Optimized for cost/performance</li>
  </ul>
  <li><strong>Response Delivery</strong></li>
  <ul>
    <li>Lambda sends response back to Lex</li>
    <li>Lex stores conversation history in session</li>
    <li>Response displayed to user through frontend</li>
  </ul>
</ol>
<img src="Congnito_user_access.png">
<h2>AWS Lambda</h2>
<h3>Flow diagram of lambda code</h3>
<img src="FlowDiagram.png">
