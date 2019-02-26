import json
import boto3
from app.util.decimalencoder import DecimalEncoder
import os

dynamodb = boto3.resource('dynamodb')
eventTableName = os.environ['EVENT_TABLE']
profileTableName = os.environ['PROFILE_TABLE']

def get_item_in_dict(field, dic):
    if(field in dic):
        info = dic[field]
        if(info == None):
            info = ""

    else:
        info = ""
        
    return info

def organizer_info(event, context):
    try:
        eventId = event['queryStringParameters']['eventId']
        eventTable = dynamodb.Table(eventTableName)
        content = eventTable.get_item(
            Key = {
                "eventId" : int(eventId)
            }
        )
        
        identityId = content['Item']['identityId']
        
        profileTable = dynamodb.Table(profileTableName)
        organizer = profileTable.get_item(
            Key = {
                "identityId" : identityId
            }
        )
        
        item = organizer['Item']
        sodaId = item['sodaId']
        name = get_item_in_dict('name', item)
        urlData = get_item_in_dict('urlData', item)
        profile = get_item_in_dict('profile', item)
        twitter = get_item_in_dict('twitter', item)
        facebook = get_item_in_dict('facebook', item)
        instagram = get_item_in_dict('instagram', item)
        
        res = {
            "organizer" : {
                "sodaId" : sodaId,
                "name" : name,
                "urlData" : urlData,
                "profile" : profile,
                "twitter" : twitter,
                "facebook" : facebook,
                "instagram" : instagram
            }
        }
        
        return {
            'statusCode' : 200,
            'headers' : {
                'content-type' : 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps(res, cls = DecimalEncoder)
        }
        
    except:
        import traceback
        traceback.print_exc()
        res_error = {
            'result' : 0
        }
        return {
            'statusCode' : 500,
            'headers' : {
                'content-type' : 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps(res_error)
        }