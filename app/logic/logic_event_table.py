from app.data.event import Event
from app.util.change_unix_to_datetime import changeStartInEvent


def getEventIdListFromTwoResponse(itemsNotPrivate, itemsPrivate):
    eventIdList = []
    if itemsNotPrivate["Count"] == 0 and itemsPrivate["Count"] == 0:
        return eventIdList

    for event in itemsNotPrivate['Items']:
        eventIdList.append(event['eventId'])

    for event in itemsPrivate['Items']:
        eventIdList.append(event['eventId'])

    return eventIdList


def getListKeysForBatchGet(listEventId):
    listKeys = []
    for eventId in listEventId:
        dic = {
            "eventId": {
                "N": str(eventId)
            }
        }
        listKeys.append(dic)

    return listKeys


def getEventsFromBatchGetResponse(response, tableName):
    events = []
    for event in response['Responses'][tableName]:
        myEvent = Event()
        myEvent.eventId = int(event['eventId']['N'])
        myEvent.eventName = event['eventName']['S']
        myEvent.updateTime = int(event['updateTime']['N'])
        myEvent.start = int(event['start']['N'])
        if('N' in event['end']):
            myEvent.end = int(event['end']['N'])
        else:
            myEvent.end = None
        myEvent.location = event['location']['S']
        myEvent.urlData = event['urlData']['S']
        myEvent.university = event['university']['S']
        myEvent.countOfLike = int(event['countOfLike']['N'])
        events.append(myEvent)

    return events


def getEventsForWeekMailFromResponse(response):
    events = []
    items = response['Items']
    for event in items:
        mEvent = Event(**event)
        startDateStr = changeStartInEvent(mEvent)
        mEvent.start = startDateStr
        events.append(mEvent)
    events.sort(key=lambda x: x.countOfLike, reverse=True)
    eventsOfTop = events[:20]

    return eventsOfTop


def getEventsFromResponse(response):
    items = response['Items']
    events = []
    for event in items:
        mEvent = Event(**event)
        events.append(mEvent)

    return events
