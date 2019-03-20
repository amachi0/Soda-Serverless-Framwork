import json
import os
import traceback
from botocore.exceptions import ClientError
from app.data.source.event_table import EventTable
from app.data.source.profile_table import ProfileTable
from app.data.sns import Sns
from app.util.return_dict import Successed, Failured

TOPIC_NAME = os.environ['SNS_CANCEL_TOPIC']


def delete_event(event, context):
    try:
        param = json.loads(event["body"])
        eventId = param['eventId']
        identityId = param['identityId']

        eventTable = EventTable(event)
        mEvent = eventTable.getFromEventId(
            eventId, "identityId, favorite, eventName")

        if identityId != mEvent.identityId:
            return Failured(traceback.format_exc())

        eventTable.delete(eventId)

        listItem = [eventId]

        profileTable = ProfileTable(event)
        profileTable.deleteListItemInProfileTable(
            mEvent.identityId, "myEvent", listItem)

        if not mEvent.hasfavorite:
            res = {"result": 1}
            return Successed(res)

        message = {
            'eventId': eventId,
            'title': mEvent.eventName,
            'listFavorite': list(mEvent.favorite)
        }

        sns = Sns(TOPIC_NAME)
        sns.publishFromDictiorary(message)

        res = {"result": 1}
        return Successed(res)

    except ClientError:
        return Failured(traceback.format_exc())
