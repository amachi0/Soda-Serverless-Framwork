import json
import boto3
import time
from boto3.dynamodb.conditions import Key, Attr
import decimal
import os

from app.data.source.event_table import EventTable
from app.data.source.profile_table import ProfileTable
from app.util.return_dict import Successed, Failured

dynamodb = boto3.resource('dynamodb')
profileTableName = os.environ['PROFILE_TABLE']
profileTable = dynamodb.Table(profileTableName)
eventTableName = os.environ['EVENT_TABLE']
eventTable = dynamodb.Table(eventTableName)
client = boto3.client('dynamodb')
statusStartIndex = os.environ['EVENT_STATUS_START_INDEX']

def finish_event(event, context):
    try:
        now = time.time()
        nowDecimal = decimal.Decimal(str(now))
        #0で始まるイベントでクエリしたい
        items = eventTable.query(
            IndexName = statusStartIndex,
            KeyConditionExpression = Key('status').eq("0_false") & Key('start').lt(nowDecimal)
        )

        if(items['Count'] == 0):
            res_error = {
                "result" : 0
            }
            return {
                'statusCode' : 200,
                'headers' : {
                    'content-type' : 'application/json'
                },
                'body' : json.dumps(res_error)
            }
            
        for item in items['Items']:
            #終了時刻が未来の場合ループを抜ける
            if item['end'] != None:
                if int(item['end']) >= now:
                    continue
            
            #イベントテーブルのfinishを1に変更
            eventTable.update_item(
                Key = {
                    'eventId' : item['eventId']
                },
                UpdateExpression = "set #name=:x",
                ExpressionAttributeNames = {
                    '#name' : "status"
                },
                ExpressionAttributeValues = {
                    ':x' : "1"
                }

            )
        
        res = {
            "result" : 1
        }
        return {
            "statusCode": 200,
            "body": json.dumps(res)
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
                'content-type' : 'application/json'
            },
            'body' : json.dumps(res_error)
        }