import json
from app.data.event import Event
from app.data.source.event_table import EventTable
from app.util.return_dict import Successed, Failured
from botocore.exceptions import ClientError

''' パラメーター
{
    "eventId" : 263,
    "identityId" : "amachi",
    "urlData" : "https://nangngnainil34982379gsesssgg",
    "start" : 1526000000,
    "end" : 1526800000,
    "university" : "立命館",
    "eventName" : "プログラミング教室",
    "price" : "500円",
    "location" : "BKC アクロスウィング",
    "qualification" : "初心者でもOK!",
    "detail" : "Djangoを勉強しよう",
    "contact" : "amachi@gmail.com",
    "isPrivate" : false
}
'''


def change_event(event, context):
    try:
        param = json.loads(event["body"])
        eventId = param['eventId']

        mEvent = Event(**param)

        eventTable = EventTable(event)
        eventTable.change(mEvent)

        res = {"eventId": eventId}
        return Successed(res)

    except ClientError:
        import traceback
        return Failured(traceback.format_exc())
