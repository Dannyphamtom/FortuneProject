import json
import boto3

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb')

# Handler function
def handler(event, context):
    try:
        if event.get('httpMethod') == 'GET':
            # Query DynamoDB to get a random fortune
            response = dynamodb.scan(
                TableName='FortunesTable',
                Select='ALL_ATTRIBUTES',
                ScanIndexForward=False,  # Get items in descending order
                Limit=1  # Limit to 1 item
            )
            fortune = response['Items'][0]['fortune']

            return {
                'statusCode': 200,
                'body': json.dumps({'fortune': fortune})
            }
        elif event.get('httpMethod') == 'POST':
            request_body = json.loads(event['body'])
            fortune = request_body['fortune']

            # Put the new fortune into DynamoDB
            dynamodb.put_item(
                TableName='FortunesTable',
                Item={'fortune': {'S': fortune}}
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

