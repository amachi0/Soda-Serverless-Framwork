from app.data.source.profile_table import ProfileTable
from app.data.source.event_table import EventTable
from app.util.return_dict import Successed, Failured
from app.util.change_none_and_emptystr import NoneToEmptystrInDict


def detail_event(event, context):
    try:
        param = event['queryStringParameters']
        eventId = int(param['eventId'])
        identityId = param['identityId']

        listFavorite = []
        if(identityId != "null"):
            profileTable = ProfileTable(event)
            profile = profileTable.getFromIdentityId(
                identityId, "favoriteEvent")
            listFavorite = profile.favoriteEvent

        eventTable = EventTable(event)
        event = eventTable.getForEventDetail(eventId)

        if event is None:
            res = {"result": 0}
            return Successed(res)

        isFavorite = False
        if(event.eventId in listFavorite):
            isFavorite = True

        res = {
            "eventId": event.eventId,
            "eventName": event.eventName,
            "detail": event.detail,
            "location": event.location,
            "university": event.university,
            "contact": event.contact,
            "urlData": event.urlData,
            "qualification": event.qualification,
            "updateTime": event.updateTime,
            "countOfLike": event.countOfLike,
            "end": event.end,
            "price": event.price,
            "start": event.start,
            "isPrivate": event.isPrivate,
            "sponsor": event.sponsor,
            "entry": event.entry,
            "isFavorite": isFavorite
        }

        NoneToEmptystrInDict(res)

        return Successed(res)

    except Exception:
        import traceback
        return Failured(traceback.format_exc())
