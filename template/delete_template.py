import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
profileTableName = os.environ['PROFILE_TABLE']

def delete_template(event, context):
    try:
        param = json.loads(event['body'])
        identityId = param["identityId"]
        templateId = param['templateId']

        profileTable = dynamodb.Table(profileTableName)
        item = profileTable.get_item(
            Key = {
                "identityId" : identityId
            }
        )

        #テンプレートが登録されてない時
        if('templates' not in item['Item']):
            res = {
                "result" : 0
            }
            return {
                'statusCode' : 200,
                'headers' : {
                    'content-type' : 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body' : json.dumps(res)
            }

        templateList = item['Item']['templates']

        for i, template in enumerate(templateList):
            if str(templateId) in template:
                print(i)
                del templateList[i]
                break

        profileTable.update_item(
            Key = {
                "identityId" : identityId
            },
            UpdateExpression = "set templates=:a",
            ExpressionAttributeValues = {
                ":a" : templateList
            }
        )

        res = {
            "result" : 1
        }
        return {
            'statusCode' : 200,
            'headers' : {
                'content-type' : 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body' : json.dumps(res)
        }

    except:
        import  traceback
        traceback.print_exc()
        res_error = {
            "result" : 0
        }
        return {
            'statusCode' : 500,
            'headers' : {
                'content-type' : 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body' : json.dumps(res_error)
        }