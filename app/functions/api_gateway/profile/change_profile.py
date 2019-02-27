import json
import boto3
import os
from app.util.emptystr_to_none import emptystrToNoneInDict

dynamodb = boto3.resource('dynamodb')
profileTableName = os.environ['PROFILE_TABLE']

def null_default(param, item):
    if(item in param):
        res = param[item]
        if(res == ""):
            res = None
        return res
    else:
        return None
    
def change_profile(event, context):
    try:
        param = json.loads(event['body'])
        identityId = param['identityId']

        table = dynamodb.Table(profileTableName)
        user = table.get_item(
            Key = {
                "identityId" : identityId
            },
            ProjectionExpression = "identityId"
        )
        print(user)


        urlData = null_default(param, "urlData")
        name = null_default(param, "name")
        universities = null_default(param, "universities")
        isAcceptMail = null_default(param, "isAcceptMail")
        profile = null_default(param, "profile")
        twitter = null_default(param, "twitter")
        facebook = null_default(param, "facebook")
        instagram = null_default(param, "instagram")
        
        table.update_item(
            Key = {
                "identityId" : identityId
            },
            UpdateExpression = "set urlData=:b,#a=:c,universities=:d,isAcceptMail=:e,profile=:f,twitter=:g,facebook=:h,instagram=:i",
            ExpressionAttributeNames = {
                '#a' : "name"
            },
            ExpressionAttributeValues = {
                ':b' : urlData,
                ':c' : name,
                ':d' : universities,
                ':e' : isAcceptMail,
                ':f' : profile,
                ':g' : twitter,
                ':h' : facebook,
                ':i' : instagram
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