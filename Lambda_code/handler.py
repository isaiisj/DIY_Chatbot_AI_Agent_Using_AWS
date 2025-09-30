import json
import boto3
import os
from botocore.exceptions import ClientError

# Initialize clients
bedrock_runtime = boto3.client('bedrock-runtime')
kendra = boto3.client('kendra')
lex = boto3.client('lexv2-runtime')

# Environment variables
KENDRA_INDEX_ID = os.environ.get('KENDRA_INDEX_ID')
BEDROCK_MODEL_ID = os.environ.get('BEDROCK_MODEL_ID', 'anthropic.claude-v2')
MAX_KENDRA_RESULTS = int(os.environ.get('MAX_KENDRA_RESULTS', '3'))

def lambda_handler(event, context):
    """
    Main Lambda handler function that orchestrates the chatbot flow.

    Args:
        event: The event from Lex
        context: Lambda context

    Returns:
        Response to be sent back to Lex
    """
    try:
        # Extract the query from Lex event
        intent_name = event['sessionState']['intent']['name']
        query = event['inputTranscript'] if 'inputTranscript' in event else event.get('text', '')

        # Get session attributes or initialize empty dict
        session_attributes = event.get('sessionAttributes', {})

        # Query Kendra for relevant information
        kendra_response = query_kendra(query)

        # Generate context from Kendra results
        context_from_kendra = format_kendra_results(kendra_response)

        # Generate response using Bedrock
        bedrock_response = generate_bedrock_response(query, context_from_kendra)

        # Format response for Lex
        lex_response = format_lex_response(bedrock_response, intent_name, session_attributes)

        return lex_response

    except Exception as e:
        print(f"Error: {str(e)}")
        # Return a fallback response
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "ElicitIntent"
                },
                "intent": {
                    "name": intent_name,
                    "state": "Failed"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "I'm sorry, I encountered an error processing your request. Please try again."
                }
            ]
        }

def query_kendra(query):
    """
    Query Kendra index for relevant information.

    Args:
        query: User query string

    Returns:
        Kendra query results
    """
    if not KENDRA_INDEX_ID:
        return {"ResultItems": []}

    try:
        response = kendra.query(
            IndexId=KENDRA_INDEX_ID,
            QueryText=query,
            AttributeFilter={
                "EqualsTo": {
                    "Key": "_language_code",
                    "Value": {"StringValue": "en"}
                }
            },
            PageSize=MAX_KENDRA_RESULTS
        )
        return response
    except ClientError as e:
        print(f"Error querying Kendra: {str(e)}")
        return {"ResultItems": []}

def format_kendra_results(kendra_response):
    """
    Format Kendra results into context for Bedrock.

    Args:
        kendra_response: Response from Kendra query

    Returns:
        Formatted context string
    """
    context = ""

    if "ResultItems" in kendra_response and kendra_response["ResultItems"]:
        context = "Based on the following information:\n\n"

        for i, result in enumerate(kendra_response["ResultItems"]):
            if "DocumentTitle" in result:
                context += f"Document: {result['DocumentTitle']['Text']}\n"

            if "DocumentExcerpt" in result:
                context += f"Excerpt: {result['DocumentExcerpt']['Text']}\n\n"

    return context

def generate_bedrock_response(query, context):
    """
    Generate a response using Bedrock model.

    Args:
        query: User query
        context: Context from Kendra

    Returns:
        Generated response from Bedrock
    """
    prompt = f"{context}\n\nUser question: {query}\n\nPlease provide a helpful response:"

    try:
        # For Claude model
        if BEDROCK_MODEL_ID.startswith('anthropic'):
            request_body = {
                "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
                "max_tokens_to_sample": 500,
                "temperature": 0.7,
                "top_p": 0.9,
            }
        # For Amazon Titan models
        elif BEDROCK_MODEL_ID.startswith('amazon'):
            request_body = {
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": 500,
                    "temperature": 0.7,
                    "topP": 0.9,
                }
            }
        # For other models, adjust as needed
        else:
            request_body = {
                "prompt": prompt,
                "max_tokens": 500,
                "temperature": 0.7,
                "top_p": 0.9,
            }

        response = bedrock_runtime.invoke_model(
            modelId=BEDROCK_MODEL_ID,
            body=json.dumps(request_body)
        )

        response_body = json.loads(response['body'].read())

        # Extract the completion based on model type
        if BEDROCK_MODEL_ID.startswith('anthropic'):
            return response_body.get('completion', '')
        elif BEDROCK_MODEL_ID.startswith('amazon'):
            return response_body.get('results', [{}])[0].get('outputText', '')
        else:
            return response_body.get('generated_text', '')

    except Exception as e:
        print(f"Error generating Bedrock response: {str(e)}")
        return "I'm sorry, I couldn't generate a response at this time."

def format_lex_response(response_text, intent_name, session_attributes):
    """
    Format the response for Lex.

    Args:
        response_text: Generated response text
        intent_name: Current intent name
        session_attributes: Current session attributes

    Returns:
        Formatted Lex response
    """
    return {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                "name": intent_name,
                "state": "Fulfilled"
            },
            "sessionAttributes": session_attributes
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": response_text
            }
        ]
    }
