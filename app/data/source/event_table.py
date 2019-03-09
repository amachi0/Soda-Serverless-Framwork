import boto3
import os
from boto3.dynamodb.conditions import Key, Attr
from app.data.event import Event

class EventTable(Event):
    def __init__(self, event):
        dynamodb = boto3.resource('dynamodb')
        self.client = boto3.client('dynamodb')
        self.tableName = os.environ['EVENT_TABLE']

        if 'isOffline' in event and event['isOffline']:
            dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
            self.client = boto3.client('dynamodb', endpoint_url='http://localhost:8000')
            self.tableName = "dev-event"
        
        self.table = dynamodb.Table(self.tableName)
        self.statusStartIndex = os.environ['EVENT_STATUS_START_INDEX']
    
    def insert(self, event=Event):
        event.createStatusFromIsPrivate()
        self.table.put_item(
            Item = {
                'identityId' : event.identityId,
                'eventId' : event.eventId,
                'eventName' : event.eventName,
                'urlData' : event.urlData,
                'university' : event.university,
                'price' : event.price,
                'location' : event.location,
                'start' : event.start,
                'end' : event.end,
                'qualification' : event.qualification,
                'detail' : event.detail,
                'contact' : event.contact,
                'status' : event.status,
                'updateTime' : event.updateTime,
                'countOfLike' : 0
            },
            ConditionExpression = "attribute_not_exists(eventId)"
        )
    
    def change(self, event=Event):
        event.createStatusFromIsPrivate()
        self.table.update_item(
            Key = {
                "eventId" : event.eventId
            },
            UpdateExpression = "set urlData=:a,#a=:b,#b=:c,university=:d,eventName=:e,price=:f,#c=:g,qualification=:h,detail=:i,contact=:j,#d=:k",
            ExpressionAttributeNames = {
                '#a' : "start",
                '#b' : "end",
                '#c' : "location",
                '#d' : "status"
            },
            ExpressionAttributeValues = {
                ':a' : event.urlData,
                ':b' : event.start,
                ':c' : event.end,
                ':d' : event.university,
                ':e' : event.eventName,
                ':f' : event.price,
                ':g' : event.location,
                ':h' : event.qualification,
                ':i' : event.detail,
                ':j' : event.contact,
                ':k' : event.status
            }
        )
    
    def addFavorite(self, eventId, listItem):
        identityId = listItem[0]
        self.table.update_item(
            Key = {
                "eventId" : eventId
            },
            UpdateExpression = "ADD favorite :x SET countOfLike = countOfLike + :val",
            ExpressionAttributeValues = {
                ':x' : set(listItem),
                ':y' : identityId,
                ':val' : 1
            },
            ConditionExpression = "NOT (contains(favorite, :y))"
        )
    
    def removeFavorite(self, eventId, listItem):
        identityId = listItem[0]
        self.table.update_item(
            Key = {
                "eventId" : eventId
            },
            UpdateExpression = "DELETE favorite :x SET countOfLike = countOfLike - :val",
            ExpressionAttributeValues = {
                ':x' : set(listItem),
                ':y' : identityId,
                ':val' : 1
            },
            ConditionExpression = "contains(favorite, :y)"
        )
    
    def getForEventDetail(self, eventId):
        item = self.table.get_item(
            Key = {
                'eventId' : eventId
            },
            ExpressionAttributeNames = {
                    '#a' : "end",
                    '#b' : 'location',
                    '#c' : 'start',
                    '#d' : 'status'
                },
            ProjectionExpression = "identityId, eventId, sodaId, contact, countOfLike, detail, #a, eventName, #b, price, qualification, #c, university, updateTime, urlData, #d"
        )
        item = item['Item']
        event = Event(**item)
        event.createIsPrivateFromStatus()
        return event
    
    def getFromEventId(self, eventId, projectionExpression=None):
        item = self.table.get_item(
            Key = {
                'eventId' : eventId
            },
            ProjectionExpression = projectionExpression
        )
        item = item['Item']
        event = Event(**item)
        return event
    
    def batchGetFromListEventId(self, listEventId):
        listKeys = []
        for eventId in listEventId:
            dic = {
                "eventId" : {
                    "N" : str(eventId)
                }
            }
            listKeys.append(dic)
        res = self.client.batch_get_item(
            RequestItems = {
                self.tableName : {
                    'Keys' : listKeys,
                    'ExpressionAttributeNames' : {
                        '#e' : "end",
                        '#l' : 'location',
                        '#s' : 'start'
                    },
                    'ProjectionExpression' : 'eventId, eventName, updateTime, #s, #e, #l, urlData, university, countOfLike'
                }
            }
        )
        events = []
        for event in res['Responses'][self.tableName]:
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
    
    def delete(self, eventId):
        self.table.delete_item(
            Key = {
                'eventId' : eventId
            }
        )
