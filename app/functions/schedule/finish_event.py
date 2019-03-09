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

        eventTable = EventTable(event)
        listEventId = eventTable.getFinishedEventIdList(nowDecimal)

        if len(listEventId) == 0:
            return Successed({ "result" : 1 })
        
        eventTable.updateStatuses(listEventId)
        return Successed({ "result" : 1 })

    except:
        import traceback
        traceback.print_exc()
