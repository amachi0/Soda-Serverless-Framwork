import json
import boto3
import os
from app.util.decimalencoder import DecimalEncoder
import os
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
profileTableName = os.environ['PROFILE_TABLE']
sodaIdIndex = os.environ['PROFILE_SODA_ID_INDEX']

def get_info_from_dict(field, dic):
    if(field in dic):
        info = dic[field]
        if(info == None):
            info = ""

    else:
        if(field == 'templates'):
            info = []
        else:
            info = ""
        
    return info


def get_profile(event, context):
    try:
        sodaId = event['queryStringParameters']['sodaId']
        table = dynamodb.Table(profileTableName)
        items = table.query(
            IndexName = sodaIdIndex,
            KeyConditionExpression = Key('sodaId').eq(sodaId)
        )
        print(items)
        dic = items['Items'][0]
        name = get_info_from_dict('name', dic)
        imgUrl = get_info_from_dict('urlData', dic)
        profile = get_info_from_dict('profile', dic)
        twitter = get_info_from_dict('twitter', dic)
        facebook = get_info_from_dict('facebook', dic)
        instagram = get_info_from_dict('instagram', dic)
        isAcceptMail = get_info_from_dict('isAcceptMail', dic)
        universities = get_info_from_dict('universities', dic)
        templates = get_info_from_dict('templates', dic)
        
        res = {
            "name" : name,
            "imgUrl" : imgUrl,
            "profile" : profile,
            "twitter" : twitter,
            "facebook" : facebook,
            "instagram" : instagram,
            "isAcceptMail" : isAcceptMail,
            "universities" : universities,
            "templates" : templates
        }
        return {
            'statusCode' : 200,
            'headers' : {
                'content-type' : 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body' : json.dumps(res, cls = DecimalEncoder)
        }
    
    except:
        import traceback
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