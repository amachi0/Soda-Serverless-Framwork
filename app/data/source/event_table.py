import boto3
import os
from boto3.dynamodb.conditions import Key, Attr
from app.data.event import Event
from app.logic.logic_event_table \
    import getEventIdListFromTwoResponse, getListKeysForBatchGet, \
    getEventsFromBatchGetResponse, getEventsForWeekMailFromResponse, \
    getEventsFromResponse


class EventTable(Event):
    def __init__(self, event):
        dynamodb = boto3.resource('dynamodb')
        self.client = boto3.client('dynamodb')
        self.tableName = os.environ['EVENT_TABLE']

        if 'isOffline' in event and event['isOffline']:
            dynamodb = boto3.resource(
                'dynamodb', endpoint_url='http://localhost:8000')
            self.client = boto3.client(
                'dynamodb', endpoint_url='http://localhost:8000')
            self.tableName = "dev-event"

        self.table = dynamodb.Table(self.tableName)
        self.statusStartIndex = os.environ['EVENT_STATUS_START_INDEX']

    def insert(self, event=Event):
        event.createStatusFromIsPrivate()
        self.table.put_item(
            Item={
                'identityId': event.identityId,
                'eventId': event.eventId,
                'eventName': event.eventName,
                'urlData': event.urlData,
                'university': event.university,
                'price': event.price,
                'location': event.location,
                'start': event.start,
                'end': event.end,
                'qualification': event.qualification,
                'detail': event.detail,
                'contact': event.contact,
                'status': event.status,
                'updateTime': event.updateTime,
                'sponsor': event.sponsor,
                'entry': event.entry,
                'countOfLike': 0
            },
            ConditionExpression="attribute_not_exists(eventId)"
        )

    def change(self, event=Event):
        event.createStatusFromIsPrivate()
        self.table.update_item(
            Key={
                "eventId": event.eventId
            },
            UpdateExpression="set urlData=:a,#a=:b,#b=:c,university=:d, \
                eventName=:e,price=:f,#c=:g,qualification=:h,detail=:i, \
                contact=:j,#d=:k, sponsor=:l, entry=:m",
            ExpressionAttributeNames={
                '#a': "start",
                '#b': "end",
                '#c': "location",
                '#d': "status"
            },
            ExpressionAttributeValues={
                ':a': event.urlData,
                ':b': event.start,
                ':c': event.end,
                ':d': event.university,
                ':e': event.eventName,
                ':f': event.price,
                ':g': event.location,
                ':h': event.qualification,
                ':i': event.detail,
                ':j': event.contact,
                ':k': event.status,
                ':l': event.sponsor,
                ':m': event.entry
            }
        )

    def addFavorite(self, eventId, listItem):
        identityId = listItem[0]
        self.table.update_item(
            Key={
                "eventId": eventId
            },
            UpdateExpression="ADD favorite :x SET countOfLike \
                = countOfLike + :val",
            ExpressionAttributeValues={
                ':x': set(listItem),
                ':y': identityId,
                ':val': 1
            },
            ConditionExpression="NOT (contains(favorite, :y))"
        )

    def removeFavorite(self, eventId, listItem):
        identityId = listItem[0]
        self.table.update_item(
            Key={
                "eventId": eventId
            },
            UpdateExpression="DELETE favorite :x SET countOfLike \
                = countOfLike - :val",
            ExpressionAttributeValues={
                ':x': set(listItem),
                ':y': identityId,
                ':val': 1
            },
            ConditionExpression="contains(favorite, :y)"
        )

    def updateStatuses(self, listEventId):
        for eventId in listEventId:
            self.table.update_item(
                Key={
                    'eventId': eventId
                },
                UpdateExpression="set #name=:x",
                ExpressionAttributeNames={
                    '#name': "status"
                },
                ExpressionAttributeValues={
                    ':x': "1"
                }
            )

    def getForEventDetail(self, eventId):
        item = self.table.get_item(
            Key={
                'eventId': eventId
            },
            ExpressionAttributeNames={
                '#a': "end",
                '#b': 'location',
                '#c': 'start',
                '#d': 'status'
            },
            ProjectionExpression="identityId, eventId, sodaId, contact, \
                countOfLike, detail, #a, eventName, #b, price, qualification, \
                #c, university, updateTime, urlData, #d, sponsor, entry"
        )

        item = item['Item']
        event = Event(**item)
        event.createIsPrivateFromStatus()
        return event

    def getFromEventId(self, eventId, projectionExpression=None):
        item = self.table.get_item(
            Key={
                'eventId': eventId
            },
            ProjectionExpression=projectionExpression
        )

        item = item['Item']
        event = Event(**item)
        return event

    def getFinishedEventIdList(self, unixTime):
        itemsNotPrivate = self.table.query(
            IndexName=self.statusStartIndex,
            KeyConditionExpression=Key('status').eq(
                '0_false') & Key('start').lt(unixTime),
            FilterExpression=Attr('end').lt(unixTime) | Attr(
                'end').attribute_type("NULL")
        )

        itemsPrivate = self.table.query(
            IndexName=self.statusStartIndex,
            KeyConditionExpression=Key('status').eq(
                '0_true') & Key('start').lt(unixTime),
            FilterExpression=Attr('end').lt(unixTime) | Attr(
                'end').attribute_type("NULL")
        )

        eventIdList = getEventIdListFromTwoResponse(
            itemsNotPrivate, itemsPrivate)
        return eventIdList

    def batchGetFromListEventId(self, listEventId):
        listKeys = getListKeysForBatchGet(listEventId)

        res = self.client.batch_get_item(
            RequestItems={
                self.tableName: {
                    'Keys': listKeys,
                    'ExpressionAttributeNames': {
                        '#e': "end",
                        '#l': 'location',
                        '#s': 'start'
                    },
                    'ProjectionExpression': 'eventId, eventName, updateTime, \
                        #s, #e, #l, urlData, university, countOfLike'
                }
            }
        )

        events = getEventsFromBatchGetResponse(res, self.tableName)
        return events

    def queryForWeekMail(self, unixTime):
        res = self.table.query(
            IndexName=self.statusStartIndex,
            KeyConditionExpression=Key('status').eq(
                '0_false') & Key('start').lt(unixTime),
            ExpressionAttributeNames={
                '#start': 'start',
                '#location': 'location'
            },
            ProjectionExpression='eventName, eventId, \
                #start, #location, countOfLike'
        )

        events = getEventsForWeekMailFromResponse(res)
        return events

    def queryForTweet(self, unixTime):
        res = self.table.query(
            IndexName=self.statusStartIndex,
            KeyConditionExpression=Key('status').eq(
                '0_false') & Key('start').lt(unixTime),
            ExpressionAttributeNames={
                '#start': 'start',
                '#end': 'end',
                '#location': 'location'
            },
            ProjectionExpression='eventName, eventId, \
                #start, #end, #location, university'
        )

        events = getEventsFromResponse(res)
        return events

    def delete(self, eventId):
        self.table.delete_item(
            Key={
                'eventId': eventId
            }
        )
