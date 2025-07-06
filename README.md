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
  <li><strong>Lambda Initial Processing:</strong></li>
  <li><strong>Kendra Search:</strong></li>
  <li><strong>Response Generation:</strong></li>
  <li><strong>Response Delivery</strong></li>
</ol>
<img src="Congnito_user_access.png">
