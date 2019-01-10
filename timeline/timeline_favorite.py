import json
import boto3
import traceback
import os
from boto3.dynamodb.conditions import Key, Attr

client = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')
profileTableName = os.environ['PROFILE_TABLE']
eventTableName = os.environ['EVENT_TABLE']
sodaIdIndex = os.environ['PROFILE_SODA_ID_INDEX']

def timeline_favorite(event, context):
    try:
        sodaId = event["queryStringParameters"]["sodaId"]
        page = int(event['queryStringParameters']['page'])

        if(sodaId == "null"):
            res = {}
            return {
                "statusCode": 200,
                'headers' : {
                    'content-type' : 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                "body": json.dumps(res)
            }

        profileTable = dynamodb.Table(profileTableName)
        items = profileTable.query(
            IndexName = sodaIdIndex,
            KeyConditionExpression = Key('sodaId').eq(sodaId)
        )
        dic = items['Items'][0]

        if("favoriteEvent" not in dic):
            res = {}
            return {
                "statusCode": 200,
                'headers' : {
                    'content-type' : 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                "body": json.dumps(res)
            }
        
        if(dic['favoriteEvent']):
            listEventId = dic['favoriteEvent']

        else:
            res = {}
            return {
                "statusCode": 200,
                'headers' : {
                    'content-type' : 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                "body": json.dumps(res)
            }

        if(page == 0):
            startNum = 0
            size = 3
        else:
            startNum = 3 + (page -1) * 5
            size = 5

        #新しい順番から表示させたいので配列を逆にする
        listEventId.reverse()
        print(listEventId)

        # 配列長以上の要素を要求されたときはここで処理を終わる
        # 配列の１ページ分を切り取る
        if(len(listEventId) <= startNum):
            res = {}
            return {
                'statusCode' : 200,
                'headers' : {
                    'content-type' : 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body' : json.dumps(res)
            }
        
        listEventIdInPage = listEventId[startNum:startNum + size]
        listKey = []
        for eventId in listEventIdInPage:
            dic = {
                "eventId" : {
                    "N" : str(eventId)
                }
            }
            listKey.append(dic)

        res = client.batch_get_item(
            RequestItems = {
                eventTableName : {
                    'Keys' : listKey,
                    'ExpressionAttributeNames' : {
                        '#e' : "end",
                        '#l' : 'location',
                        '#s' : 'start'
                    },
                    'ProjectionExpression' : 'eventId, eventName, updateTime, #s, #e, #l, urlData, university, countOfLike'
                }
            }
        )
        
        #それぞれのeventIdをint型に変換
        for event in res['Responses'][eventTableName]:
            event['eventId']['N'] = int(event['eventId']['N'])

        response = {}
        i = startNum
        eventList = res['Responses'][eventTableName]
        #元のeventIdの配列の順番に並び替える
        eventList = sorted(eventList, key=lambda data: listEventId.index(data["eventId"]["N"]))

        for event in eventList:
            response[i] = {}
            eventId = event['eventId']['N']
            eventName = event['eventName']['S']
            updateTime = int(event['updateTime']['N'])
            start = int(event['start']['N'])
            if('N' in event['end']):
                end = int(event['end']['N'])
            else:
                end = None
            location = event['location']['S']
            urlData = event['urlData']['S']
            university = event['university']['S']
            countOfLike = int(event['countOfLike']['N'])
            
            response[i]["eventId"] = eventId
            response[i]["eventName"] = eventName
            response[i]["updateTime"] = updateTime
            response[i]["startTime"] = start
            response[i]["endTime"] = end
            response[i]["location"] = location
            response[i]["urlData"] = urlData
            response[i]["university"] = university
            response[i]["countOfLike"] = countOfLike
            response[i]["isFavorite"] = True
            i += 1
        
        return {
            "statusCode": 200,
            'headers' : {
                'content-type' : 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps(response)
        }

    except:
        traceback.print_exc()
        res = {
            "result" : 0
        }
        return {
            "statusCode": 500,
            'headers' : {
                'content-type' : 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps(res)
        }