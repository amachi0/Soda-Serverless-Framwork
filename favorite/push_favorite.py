import json
import boto3
import os
from decimalencoder import DecimalEncoder

dynamodb = boto3.resource('dynamodb')
profileTableName = os.environ['PROFILE_TABLE']
eventTableName = os.environ['EVENT_TABLE']

def push_favorite(event, context):
    try:
        body = json.loads(event['body'])
        eventId = int(body["eventId"])
        identityId = body["identityId"]
        profileTable = dynamodb.Table(profileTableName)
        itemsProfile = profileTable.get_item(
            Key = {
                "identityId" : identityId
            }
        )
        listEventId = []
        if("favoriteEvent" in itemsProfile['Item']):
            listEventId = itemsProfile['Item']['favoriteEvent']

        listEventId.append(eventId)
        
        profileTable.update_item(
            Key = {
                "identityId" : identityId
            },
            UpdateExpression = "set favoriteEvent=:x",
            ExpressionAttributeValues = {
                ':x' : listEventId
            }
        )
        
        eventTable = dynamodb.Table(eventTableName)
        itemsEvent = eventTable.get_item(
            Key = {
                "eventId" : eventId
            }
        )
        listIdentityId = []
        if('favorite' in itemsEvent['Item']):
            listIdentityId = itemsEvent['Item']['favorite']
        listIdentityId.append(identityId)
        
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
        import traceback
        traceback.print_exc()
        resError = {
            "result" : 0
        }
        return {
            'statusCode' : 500,
            'headers' : {
                'content-type' : 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body' : json.dumps(resError)
        }