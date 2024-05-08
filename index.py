import json
import boto3

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb')

# Handler function
def handler(event, context):
    try:
        if event['httpMethod'] == 'GET':
            # Query DynamoDB to get a random fortune
            response = dynamodb.scan(
                TableName='Fortunes-Table', # Your table name, in this case mine was "Fortunes-Table" case sensitive
                Select='ALL_ATTRIBUTES',
                Limit=1
            )
            if 'Items' in response and len(response['Items']) > 0:
                fortune = response['Items'][0].get('Fortunes')  # Your partition key name, mine was "Fortunes" case sensitive
                return {
                    'statusCode': 200,
                    'body': json.dumps({'Fortunes': fortune})
                }
            else:
                return {
                    'statusCode': 404,
                    'body': json.dumps({'error': 'No fortunes found'})
                }
        elif event['httpMethod'] == 'POST':
            request_body = json.loads(event['body'])
            fortune = request_body.get('Fortunes')  
            if not fortune:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Missing fortune in request body'})
                }

            # Put the new fortune into DynamoDB
            dynamodb.put_item(
                TableName='Fortunes-Table',
                Item={'Fortunes': {'S': fortune}}  
            )

            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Fortune submitted successfully'})
            }
        else:
            return {
                'statusCode': 405,
                'body': json.dumps({'error': 'Method Not Allowed'})
            }
    except Exception as e:
        print('Error:', e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error'})
        }

