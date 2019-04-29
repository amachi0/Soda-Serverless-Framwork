from app.data.source.event_table import EventTable
from app.data.source.profile_table import ProfileTable
from app.util.return_dict import Successed, Failured
from app.util.change_none_and_emptystr import NoneToEmptystrInDict


def organizer_info(event, context):
    try:
        eventId = int(event['queryStringParameters']['eventId'])

        eventTable = EventTable(event)
        mEvent = eventTable.getFromEventId(eventId, 'identityId')

        if mEvent is None:
            res = {"result": 0}
            return Successed(res)

        identityId = mEvent.identityId

        profileTable = ProfileTable(event)
        organizer = profileTable.getOrganizerInfo(identityId)

        info = {
            "sodaId": organizer.sodaId,
            "name": organizer.name,
            "urlData": organizer.urlData,
            "profile": organizer.profile,
            "twitter": organizer.twitter,
            "facebook": organizer.facebook,
            "instagram": organizer.instagram
        }

        NoneToEmptystrInDict(info)

        res = {
            'organizer': info
        }

        return Successed(res)

    except Exception:
        import traceback
        return Failured(traceback.format_exc())
