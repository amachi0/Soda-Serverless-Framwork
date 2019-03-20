import json
import boto3
import os
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
profileTableName = os.environ['PROFILE_TABLE']


def change_template(event, context):
    try:
        param = json.loads(event['body'])
        identityId = param['identityId']
        templateId = param['templateId']

        profileTable = dynamodb.Table(profileTableName)
        item = profileTable.get_item(
            Key={
                "identityId": identityId
            }
        )

        templateList = item['Item']['templates']
        for i, template in enumerate(templateList):
            if str(templateId) in template:
                index = i
                break

        templateList[index] = {
            str(templateId): {
                'eventName': param['eventName'],
                'urlData': param['urlData'],
                'university': param['university'],
                'price': param['price'],
                'location': param['location'],
                'qualification': param['qualification'],
                'detail': param['detail'],
                'contact': param['contact'],
                'entry': param['entry'],
                'sponsor': param['sponsor'],
                'isPrivate': param['isPrivate']
            }
        }

        profileTable.update_item(
            Key={
                "identityId": identityId
            },
            UpdateExpression="set templates=:a",
            ExpressionAttributeValues={
                ":a": templateList
            }
        )

        res = {
            "result": 1
        }
        return {
            'statusCode': 200,
            'headers': {
                'content-type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(res)
        }

    except ClientError:
        import traceback
        traceback.print_exc()
        res_error = {
            "result": 0
        }
        return {
            'statusCode': 500,
            'headers': {
                'content-type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(res_error)
        }
