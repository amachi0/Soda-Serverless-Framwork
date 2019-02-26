import json
import boto3
import traceback
import os
from app.util.decimalencoder import DecimalEncoder

dynamodb = boto3.resource('dynamodb')
profileTableName = os.environ['PROFILE_TABLE']
eventTableName = os.environ['EVENT_TABLE']

def cancel_favorite(event, context):
    try:
        param = json.loads(event['body'])
        eventId = int(param["eventId"])
        identityId = param["identityId"]

        #ProfileTableからいいねを解除したeventIdをremoveして更新する
        profileTable = dynamodb.Table(profileTableName)
        itemsProfile = profileTable.get_item(
            Key = {
                "identityId" : identityId
            }
        ) 
        listEventId = []
        if("favoriteEvent" in itemsProfile['Item']):
            listEventId = itemsProfile['Item']['favoriteEvent']
            listEventId.remove(eventId)
        profileTable.update_item(
            Key = {
                "identityId" : identityId
            },
            UpdateExpression = "set favoriteEvent=:x",
            ExpressionAttributeValues = {
                ':x' : listEventId
            }
        )
        
        #イベントテーブルのfavorite, countOfLikeを更新
        eventTable = dynamodb.Table(eventTableName)
        itemsEvent = eventTable.get_item(
            Key = {
                "eventId" : eventId
            }
        )
        
        listIdentityId = []
        if('favorite' in itemsEvent['Item']):
            listIdentityId = itemsEvent['Item']['favorite']
            listIdentityId.remove(identityId)
            
        else:
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
        
        countOfLike = len(listIdentityId)
        eventTable.update_item(
            Key = {
                "eventId" : eventId
            },
            UpdateExpression = "set favorite=:x, countOfLike=:y",
            ExpressionAttributeValues = {
                ':x' : listIdentityId,
                ':y' : countOfLike
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
        traceback.print_exc()
        res = {
            "result" : 0
        }
        return {
            'statusCode' : 500,
            'headers' : {
                'content-type' : 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body' : json.dumps(res)
        }