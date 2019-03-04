import boto3
import os
from boto3.dynamodb.conditions import Key, Attr
from app.data.event import Event

class EventTable(Event):
    def __init__(self, event):
        dynamodb = boto3.resource('dynamodb')
        tableName = os.environ['EVENT_TABLE']

        if 'isOffline' in event and event['isOffline']:
            dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
            tableName = "dev-event"
        
        self.table = dynamodb.Table(tableName)
    
    def insert(self, event=Event):
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
                # 'entry' : param['entry'],
                # 'sponsor' : param['sponsor'],
                'status' : event.status,
                'updateTime' : event.updateTime,
                'countOfLike' : 0
            }
        )
    
    def change(self, event=Event):
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