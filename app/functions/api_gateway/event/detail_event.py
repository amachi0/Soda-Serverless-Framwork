from app.data.profile import Profile
from app.data.source.profile_table import ProfileTable
from app.data.source.event_table import EventTable
from app.util.return_dict import Successed, Failured

def detail_event(event, context):
    try:
        param = event['queryStringParameters']
        eventId = int(param['eventId'])
        identityId = param['identityId']

        listFavorite = []
        if(identityId != "null"):
            profileTable = ProfileTable(event)
            profile = profileTable.getFromIdentityId(identityId, "favoriteEvent")
            listFavorite = profile.favoriteEvent
            
        eventTable = EventTable(event)
        event = eventTable.getForEventDetail(eventId)

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
            "isFavorite": isFavorite
        }

        return Successed(res)
    
    except:
        import  traceback
        return Failured(traceback.format_exc())
