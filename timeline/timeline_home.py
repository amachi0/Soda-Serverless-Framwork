import json
import boto3
import os
from decimalencoder import DecimalEncoder
from boto3.dynamodb.conditions import Key, Attr
from timeline.model_timeline import Query

dynamodb = boto3.resource('dynamodb')
endPoint = os.environ['CLOUD_SEARCH_ENDPOINT']
cloudSearch = boto3.client('cloudsearchdomain', endpoint_url = endPoint)
profileTableName = os.environ['PROFILE_TABLE']
eventTableName = os.environ['EVENT_TABLE']
statusStartIndex = os.environ['EVENT_STATUS_START_INDEX']

def timeline_home(event, context):
    try:
        identityId = event['queryStringParameters']['identityId']
        startIndex = int(event['queryStringParameters']['startIndex'])
        favoriteList = []

        #identityIdがあった場合
        if (identityId != "null"):
            profileTable = dynamodb.Table(profileTableName)
            itemProfile = profileTable.get_item(
                Key = {
                    "identityId" : identityId
                },
                ProjectionExpression = "universities, favoriteEvent"
            )

            if not ("Item" in itemProfile):
                pass

            elif not (itemProfile['Item']['universities']):
                pass
        
            else:
                universities = itemProfile['Item']['universities']

            #いいねを今現在押しているイベントかどうかを判定したい
            if('favoriteEvent' in itemProfile['Item']):
                favoriteList = itemProfile['Item']['favoriteEvent']
        
        if startIndex == 0 and identityId == "null":
            model = Query(statusStartIndex)
            result = model.queryFirstNoUniversity()
        
        elif startIndex == 0 and identityId != "null":
            model = Query(statusStartIndex)
            result = model.queryFirst(universities)

        elif startIndex != 0 and identityId == "null":
            lastEventId = event['queryStringParameters']['lastEventId']
            lastStart = event['queryStringParameters']['lastStartTime']
            startKey = {
                "eventId" : int(lastEventId),
                "start" : int(lastStart),
                "status" : "0_false"
            }
            model = Query(statusStartIndex)
            result = model.queryNextNoUniversity(startKey)
        
        elif startIndex != 0 and identityId != "null":
            lastEventId = event['queryStringParameters']['lastEventId']
            lastStart = event['queryStringParameters']['lastStartTime']
            startKey = {
                "eventId" : int(lastEventId),
                "start" : int(lastStart),
                "status" : "0_false"
            }
            model = Query(statusStartIndex)
            result = model.queryNext(universities, startKey)
        
        print(result)
        res = {}
        i = startIndex
        for hit in result:
            res[i] = {}
            res[i]["eventId"] = int(hit['eventId'])
            res[i]["eventName"] = hit['eventName']
            res[i]["updateTime"] = int(hit['updateTime'])
            res[i]["startTime"] = int(hit['start'])
            if(hit['end']):
                res[i]["endTime"] = int(hit['end'])
            else:
                res[i]["endTime"] = None
            res[i]["location"] = hit['location']
            res[i]["urlData"] = hit['urlData']
            res[i]["university"] = hit['university']
            res[i]["countOfLike"] = int(hit['countOfLike'])
            
            if(int(res[i]["eventId"]) in favoriteList):
                res[i]["isFavorite"] = True
            else:
                res[i]["isFavorite"] = False

            i += 1

        return {
            "statusCode": 200,
            'headers' : {
                'content-type' : 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps(res, cls = DecimalEncoder)
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