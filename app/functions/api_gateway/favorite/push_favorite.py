import json
from app.data.source.profile_table import ProfileTable
from app.data.source.event_table import EventTable
from app.util.return_dict import Successed, Failured

''' パラメーター
{
    "identityId": "amachi1",
    "eventId" : 1 
}
'''

def push_favorite(event, context):
    try:
        body = json.loads(event['body'])
        eventId = int(body["eventId"])
        identityId = body["identityId"]
        listEventId = [eventId]
        listIdentityId = [identityId]

        profileTable = ProfileTable(event)
        profileTable.addListItemInProfileTable(identityId, 'favoriteEvent', listEventId)

        eventTable = EventTable(event)
        eventTable.addFavorite(eventId, listIdentityId)

        res = { "result" : 1 }
        return Successed(res)
        
    except:
        import traceback
        traceback.print_exc()
        Failured()