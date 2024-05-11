import json
import boto3

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb')

# Handler function
def handler(event, context):
    try:
        if event['httpMethod'] == 'GET':
            # Your existing GET request handling code
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': 'https://dpfortuneprojectaws.com',
                },
                'body': json.dumps({'message': 'GET request received'})
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
