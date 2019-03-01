import os
import json
import boto3
from app.util.decimalencoder import DecimalEncoder

dynamodb = boto3.resource('dynamodb')
eventTableName = os.environ['EVENT_TABLE']
profileTableName = os.environ['PROFILE_TABLE']

def detail_event(event, context):
    try:
        eventId = int(event['queryStringParameters']['eventId'])
        identityId = event['queryStringParameters']['identityId']
        listFavorite = []
        isFavorite = False
        
        if(identityId != "null"):
            profileTable = dynamodb.Table(profileTableName)
            user = profileTable.get_item(
                Key = {
                    'identityId' : identityId
                },
                ProjectionExpression = "favoriteEvent"
            )

            if("favoriteEvent" in user['Item']):
                listFavorite.extend(user['Item']['favoriteEvent'])
        
        table = dynamodb.Table(eventTableName)
        content = table.get_item(
            Key = {
                'eventId' : eventId
            },
            ExpressionAttributeNames = {
                    '#a' : "end",
                    '#b' : 'location',
                    '#c' : 'start',
                    '#d' : 'status'
                },
            ProjectionExpression = "eventId, sodaId, contact, countOfLike, detail, #a, eventName, #b, price, qualification, #c, university, updateTime, urlData, #d"
        )
        
        item = content['Item']

        status = item['status']
        if(status == "0_false"):
            item['isPrivate'] = False
        else:
            item['isPrivate'] = True

        if(item['eventId'] in listFavorite):
            isFavorite = True
        item['isFavorite'] = isFavorite

        return {
            'statusCode' : 200,
            'headers' : {
                'content-type' : 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body' : json.dumps(item, cls=DecimalEncoder)
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