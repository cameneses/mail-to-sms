import boto3
import json
import os
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Load the SNS topic name from environment variables
TOPIC_ARN = os.getenv('TOPIC_NAME')


def lambda_handler(event, context):
    # Logging the incoming event for debugging
    logger.info(f"Received event: {event}")

    # Parsing the SES event
    try:
        message = event['Records'][0]['ses']['mail']
        subject = message['commonHeaders']['subject']
        # Assuming the email body is plain text; adjust as needed if the format differs
        # This might need parsing or decoding based on your setup
        body = message['content']
    except KeyError as e:
        logger.error(f"Error parsing the SES message: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps('Error processing the email')
        }

    # Send SMS via SNS
    try:
        sns = boto3.client('sns')
        response = sns.publish(
            TopicArn=TOPIC_ARN,
            Message=f"Subject: {subject}\nContent: {body}",
            Subject='Update'
        )
        logger.info(f"Message sent to SNS: {response}")
        return {
            'statusCode': 200,
            'body': json.dumps('Email processed and SMS sent successfully')
        }
    except Exception as e:
        logger.error(f"Error sending SMS via SNS: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error sending SMS')
        }
