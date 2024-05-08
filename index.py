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
                TableName='Fortunes-Table',
                Select='ALL_ATTRIBUTES',
                Limit=1
            )
            if 'Items' in response and len(response['Items']) > 0:
                fortune = response['Items'][0].get('Fortunes')  # Change from 'fortune' to 'fortunes'
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': 'https://dannypham.w3spaces.com',
                    },
                    'body': json.dumps({'Fortunes': fortune})
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': 'https://dannypham.w3spaces.com',
                    },
                    'body': json.dumps({'error': 'No fortunes found'})
                }
        elif event['httpMethod'] == 'POST':
            if 'body' not in event or not event['body']:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': 'https://dannypham.w3spaces.com',
                    },
                    'body': json.dumps({'error': 'Missing request body'})
                }

            try:
                request_body = json.loads(event['body'])
                fortune = request_body.get('Fortunes')  # Change from 'fortune' to 'fortunes'
                if not fortune:
                    return {
                        'statusCode': 400,
                        'headers': {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': 'https://dannypham.w3spaces.com',
                        },
                        'body': json.dumps({'error': 'Missing fortune in request body'})
                    }

                # Put the new fortune into DynamoDB
                dynamodb.put_item(
                    TableName='Fortunes-Table',
                    Item={'Fortunes': {'S': fortune}}  # Change from 'fortune' to 'fortunes'
                )

                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': 'https://dannypham.w3spaces.com',
                    },
                    'body': json.dumps({'message': 'Fortune submitted successfully'})
                }
            except Exception as e:
                print('Error:', e)
                return {
                    'statusCode': 500,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': 'https://dannypham.w3spaces.com',
                    },
                    'body': json.dumps({'error': 'Internal Server Error'})
                }
        else:
            return {
                'statusCode': 405,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': 'https://dannypham.w3spaces.com',
                },
                'body': json.dumps({'error': 'Method Not Allowed'})
            }
    except Exception as e:
        print('Error:', e)
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': 'https://dannypham.w3spaces.com',
            },
            'body': json.dumps({'error': 'Internal Server Error'})
        }
