import os
import json
import boto3
import time
from app.util.decimalencoder import DecimalEncoder
from datetime import datetime as dt

dynamodb = boto3.resource('dynamodb')
endpointUrl = os.environ['CLOUD_SEARCH_DOC_ENDPOINT']
sequenceTableName = os.environ['SEQUENCE_TABLE']
eventTableName = os.environ['EVENT_TABLE']
profileTableName = os.environ['PROFILE_TABLE']
cloudSearch = boto3.client('cloudsearchdomain', endpoint_url = endpointUrl)

def next_seq(table, tableName):
    res = table.update_item(
        Key = {
            'tableName' : tableName
        },
        UpdateExpression = "set seq = seq + :val",
        ExpressionAttributeValues = {
            ':val' : 1
        },
        ReturnValues="UPDATED_NEW"
    )
    return res['Attributes']['seq']

def create_event(event, context):
    try:
        param = json.loads(event['body'])
        seqtable = dynamodb.Table(sequenceTableName)
        nextseq = next_seq(seqtable, 'event')
        identityId = param['identityId']

        if not("end" in param):
            end = None
        else:
            end = param['end']
        
        now = int(time.time())

        isPrivate = param['isPrivate']
        if(isPrivate is False):
            status = "0_false"
        else:
            status = "0_true"

        eventTable = dynamodb.Table(eventTableName)
        eventTable.put_item(
            Item = {
                'identityId' : identityId,
                'eventId' : nextseq,
                'eventName' : param['eventName'],
                'urlData' : param['urlData'],
                'university' : param['university'],
                'price' : param['price'],
                'location' : param['location'],
                'start' : param['start'],
                'end' : end,
                'qualification' : param['qualification'],
                'detail' : param['detail'],
                'contact' : param['contact'],
                'entry' : param['entry'],
                'sponsor' : param['sponsor'],
                'status' : status,
                'updateTime' : now,
                'countOfLike' : 0
            }
        )
        
        profileTable = dynamodb.Table(profileTableName)
        itemProfile = profileTable.get_item(
            Key = {
                "identityId" : identityId
            }
        )
        
        listMyevent = []
        if("myEvent" in itemProfile['Item']):
            listMyevent = itemProfile['Item']['myEvent']
            
        listMyevent.append(nextseq)
        profileTable.update_item(
            Key = {
                "identityId" : identityId
            },
            UpdateExpression = "set myEvent=:x",
            ExpressionAttributeValues = {
                ':x' : listMyevent
            }
        )

        res = {
            "eventId" : nextseq
        }
        return {
            'statusCode' : 200,
            'headers' : {
                'content-type' : 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body' : json.dumps(res,cls=DecimalEncoder)
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