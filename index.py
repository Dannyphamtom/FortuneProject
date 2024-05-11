import json
import boto3
import random

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb')

# Handler function
def handler(event, context):
    try:
        if event['httpMethod'] == 'GET':
            # Scan DynamoDB to get all items
            response = dynamodb.scan(
                TableName='Fortunes-Table',
                Select='ALL_ATTRIBUTES',
            )
            # Check if any items are found
            if 'Items' in response and len(response['Items']) > 0:
                # Get a random index within the range of items
                random_index = random.randint(0, len(response['Items']) - 1)
                # Get the fortune at the random index
                fortune = response['Items'][random_index].get('Fortunes')
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': 'https://www.dpfortuneprojectaws.com',
                    },
                    'body': json.dumps({'Fortunes': fortune})
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': 'https://www.dpfortuneprojectaws.com',
                    },
                    'body': json.dumps({'error': 'No fortunes found'})
                }
        # Handle other HTTP methods (POST, etc.) as needed
        else:
            return {
                'statusCode': 405,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': 'https://www.dpfortuneprojectaws.com',
                },
                'body': json.dumps({'error': 'Method Not Allowed'})
            }
    except Exception as e:
        print('Error:', e)
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': 'https://www.dpfortuneprojectaws.com',
            },
            'body': json.dumps({'error': 'Internal Server Error'})
        }
