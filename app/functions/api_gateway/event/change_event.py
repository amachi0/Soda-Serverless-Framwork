import json
import boto3
import os
from app.util.decimalencoder import DecimalEncoder

dynamodb = boto3.resource('dynamodb')
eventTableName = os.environ['EVENT_TABLE']

def change_event(event, context):
    try:
        param = json.loads(event["body"])
        eventId = param['eventId']

        if not(param['end']):
            end = None
        else:
            end = int(param['end'])

        table = dynamodb.Table(eventTableName)
        table.update_item(
            Key = {
                "eventId" : eventId
            },
            UpdateExpression = "set urlData=:a,#s=:b,#e=:c,university=:d,eventName=:e,price=:f,#l=:g,qualification=:h,detail=:i,contact=:j,entry=:k,sponsor=:l,isPrivate=:m",
            ExpressionAttributeNames = {
                '#s' : "start",
                '#e' : "end",
                '#l' : "location"
            },
            ExpressionAttributeValues = {
                ':a' : param['urlData'],
                ':b' : param['start'],
                ':c' : end,
                ':d' : param['university'],
                ':e' : param['eventName'],
                ':f' : param['price'],
                ':g' : param['location'],
                ':h' : param['qualification'],
                ':i' : param['detail'],
                ':j' : param['contact'],
                ':k' : param['entry'],
                ':l' : param['sponsor'],
                ':m' : param['isPrivate']
            }
        )

        res = {
            "eventId" : eventId
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