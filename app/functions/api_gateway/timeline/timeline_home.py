import boto3
import os
from botocore.exceptions import ClientError
from app.util.return_dict import Successed, Failured
from app.data.model_timeline import Query

dynamodb = boto3.resource('dynamodb')
profileTableName = os.environ['PROFILE_TABLE']
eventTableName = os.environ['EVENT_TABLE']
statusStartIndex = os.environ['EVENT_STATUS_START_INDEX']


def timeline_home(event, context):
    try:
        identityId = event['queryStringParameters']['identityId']
        startIndex = int(event['queryStringParameters']['startIndex'])
        favoriteList = []

        # identityIdがあった場合
        if (identityId != "null"):
            profileTable = dynamodb.Table(profileTableName)
            itemProfile = profileTable.get_item(
                Key={
                    "identityId": identityId
                },
                ProjectionExpression="universities, favoriteEvent"
            )

            if not ("Item" in itemProfile):
                pass

            elif not (itemProfile['Item']['universities']):
                pass

            else:
                universities = itemProfile['Item']['universities']

            # いいねを今現在押しているイベントかどうかを判定したい
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
                "eventId": int(lastEventId),
                "start": int(lastStart),
                "status": "0_false"
            }
            model = Query(statusStartIndex)
            result = model.queryNextNoUniversity(startKey)

        elif startIndex != 0 and identityId != "null":
            lastEventId = event['queryStringParameters']['lastEventId']
            lastStart = event['queryStringParameters']['lastStartTime']
            startKey = {
                "eventId": int(lastEventId),
                "start": int(lastStart),
                "status": "0_false"
            }
            model = Query(statusStartIndex)
            result = model.queryNext(universities, startKey)

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

        return Successed(res)

    except ClientError:
        import traceback
        return Failured(traceback.format_exc())
