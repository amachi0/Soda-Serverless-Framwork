import json
import boto3
import os
from app.data.profile import Profile

dynamodb = boto3.resource('dynamodb')
profileTableName = os.environ['PROFILE_TABLE']

def create_user(event, context):
    try:
        param = json.loads(event['body'])
        #param = event['body']
        identityId = param['identityId']

        #すでにユーザーがいた場合
        profileTable = dynamodb.Table(profileTableName)
        user = profileTable.get_item(
            Key = {
                "identityId" : identityId
            }
        )
        if ("Item" in user):
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

        sodaId = param['sodaId']
        email = param['email']
        universities = param['universities']
        name = param['name']
        urlData = param['urlData']
        if not (name):
            emailSplit = email.rsplit("@")
            name = emailSplit[0]
        if not (urlData):
            urlData = None
        
        profileTable.put_item(
            Item = {
                "identityId" : identityId,
                "sodaId" : sodaId,
                "email" : email,
                "universities" : universities,
                "urlData" : urlData,
                "name" : name,
                "isAcceptMail" : True
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