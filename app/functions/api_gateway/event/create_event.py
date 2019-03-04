import json
import time
from app.data.event import Event
from app.data.source.sequence_table import SequenceTable
from app.data.source.event_table import EventTable
from app.data.source.profile_table import ProfileTable
from app.util.return_dict import Successed, Failured

''' パラメーター
{
    "identityId": "amachi1",
    "eventName": "イベント名",
    "urlData": "https://nangngnainil34982379gsesssgg",
    "university": "立命館大学",
    "price": "500円",
    "location": "BKC アクロスウィング",
    "start": 1526000000,
    "end": 1528000000,
    "qualification": "初心者でもOK!",
    "detail": "テスト",
    "contact": "amachi@gmail.com",
    "isPrivate": false
}
'''

def create_event(event, context):
    try:
        param = json.loads(event['body'])

        identityId = param['identityId']

        mEvent = Event(**param)

        sequenceTable = SequenceTable(event)
        nextseq = sequenceTable.next_seq()
        mEvent.eventId = nextseq

        now = int(time.time())
        mEvent.updateTime = now

        eventTable = EventTable(event)
        eventTable.insert(mEvent)

        profileTable = ProfileTable(event)
        profile = profileTable.getFromIdentityId(identityId, "myEvent")
        listMyEvent = []
        if profile.myEvent != []:
            listMyEvent = profile.myEvent
        listMyEvent.append(mEvent.eventId)

        profileTable.changeMyEvent(identityId, listMyEvent)
        
        res = { "eventId" : mEvent.eventId }
        return Successed(res)
    
    except:
        import  traceback
        traceback.print_exc()
        return Failured()