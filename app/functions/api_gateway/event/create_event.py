import os
import json
import boto3
import time
from app.data.event import Event
from app.data.source.sequence_table import SequenceTable
from app.data.source.event_table import EventTable
from app.data.source.profile_table import ProfileTable
from app.util.return_dict import Successed, Failured

def create_event(event, context):
    try:
        param = json.loads(event['body'])

        identityId = param['identityId']

        mEvent = Event(**param)
        mEvent.createStatusFromIsPrivate()

        sequenceTable = SequenceTable(event)
        nextseq = sequenceTable.next_seq()
        mEvent.eventId = nextseq

        now = int(time.time())
        mEvent.updateTime = now

        eventTable = EventTable(event)
        eventTable.insert(mEvent)

        profileTable = ProfileTable(event)
        item = profileTable.getFromIdentityId(identityId, "myEvent")
        listMyEvent = []
        if("myEvent" in item):
            listMyEvent = item['myEvent']
        listMyEvent.append(mEvent.eventId)

        profileTable.changeMyEvent(identityId, listMyEvent)
        
        res = {
            "eventId" : mEvent.eventId
        }
        return Successed(res)
    
    except:
        import  traceback
        traceback.print_exc()
        return Failured()