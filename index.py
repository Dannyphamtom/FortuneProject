import json
import boto3
import random

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb')

# Handler function
def handler(event, context):
    try:
        if event['httpMethod'] == 'GET':
            # Retrieve a random item from the DynamoDB table
            response = dynamodb.scan(
                TableName='Fortunes-Table'
            )
            items = response['Items']
            if len(items) > 0:
                random_fortune = random.choice(items)['Fortunes']['S']
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': 'https://dpfortuneprojectaws.com',
                    },
                    'body': json.dumps({'message': 'Fortune retrieved successfully', 'Fortunes': random_fortune})
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': 'https://dpfortuneprojectaws.com',
                    },
                    'body': json.dumps({'error': 'No fortunes available'})
                }
            
        elif event['httpMethod'] == 'POST':
            # Handle POST request
            data = json.loads(event['body'])
            fortune = data.get('Fortunes')
            
            # Write the received fortune to DynamoDB
            response = dynamodb.put_item(
                TableName='Fortunes-Table',
                Item={
                    'Fortunes': {'S': fortune}
                }
            )
            
            # Check if the item was successfully written to DynamoDB
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': 'https://dpfortuneprojectaws.com',
                    },
                    'body': json.dumps({'message': 'Fortune submitted successfully', 'Fortunes': fortune})
                }
            else:
                return {
                    'statusCode': 500,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': 'https://dpfortuneprojectaws.com',
                    },
                    'body': json.dumps({'error': 'Failed to submit Fortune to DynamoDB'})
                }
                
        else:
            return {
                'statusCode': 405,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': 'https://dpfortuneprojectaws.com',
                },
                'body': json.dumps({'error': 'Method Not Allowed'})
            }
    except Exception as e:
        print('Error:', e)
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': 'https://dpfortuneprojectaws.com',
            },
            'body': json.dumps({'error': 'Internal Server Error'})
        }


