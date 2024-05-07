import json
import boto3

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb')

# Handler function for fetching a fortune
def get_fortune(event, context):
    try:
        # Query DynamoDB to get a random fortune
        response = dynamodb.scan(
            TableName='Fortunes-Table',
            Select='ALL_ATTRIBUTES',
            ScanIndexForward=False,  # Get items in descending order
            Limit=1  # Limit to 1 item
        )
        fortune = response['Items'][0]['fortune']

        return {
            'statusCode': 200,
            'body': json.dumps({'fortune': fortune})
        }
    except Exception as e:
        print('Error fetching fortune:', e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to fetch fortune'})
        }

# Handler function for submitting a fortune
def submit_fortune(event, context):
    try:
        request_body = json.loads(event['body'])
        fortune = request_body['fortune']

        # Put the new fortune into DynamoDB
        dynamodb.put_item(
            TableName='Fortunes-Table',
            Item={'fortune': {'S': fortune}}
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Fortune submitted successfully'})
        }
    except Exception as e:
        print('Error submitting fortune:', e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to submit fortune'})
        }


