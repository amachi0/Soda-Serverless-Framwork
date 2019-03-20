import json
import boto3
import os
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
profileTableName = os.environ['PROFILE_TABLE']
sequenceTableName = os.environ['SEQUENCE_TABLE']


def next_seq(table, tableName):
    res = table.update_item(
        Key={
            'tableName': tableName
        },
        UpdateExpression="set seq = seq + :val",
        ExpressionAttributeValues={
            ':val': 1
        },
        ReturnValues="UPDATED_NEW"
    )
    return res['Attributes']['seq']


def create_template(event, context):
    try:
        param = json.loads(event['body'])
        identityId = param["identityId"]

        profileTable = dynamodb.Table(profileTableName)
        item = profileTable.get_item(
            Key={
                "identityId": identityId
            }
        )

        templateList = []
        if 'templates' in item['Item']:
            templateList = item['Item']['templates']

        seqtable = dynamodb.Table(sequenceTableName)
        templateId = next_seq(seqtable, 'event')
        dic = {
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
        templateList.append(dic)
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
