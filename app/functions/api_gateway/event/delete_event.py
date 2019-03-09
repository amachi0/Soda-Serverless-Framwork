import json
import os
from app.data.source.event_table import EventTable
from app.data.source.profile_table import ProfileTable
from app.util.return_dict import Successed, Failured

'''
sns = boto3.resource('sns')
topic_name = os.environ['SNS_CANCEL_TOPIC']
topic = sns.Topic(topic_name)
'''

def delete_event(event, context):
    try:
        param = json.loads(event["body"])
        eventId = param['eventId']
        identityId = param['identityId']

        eventTable = EventTable(event)
        mEvent = eventTable.getFromEventId(eventId, "identityId")

        if identityId != mEvent.identityId:
            return Failured()

        eventTable.delete(eventId)
        
        listItem = [eventId]

        profileTable = ProfileTable(event)
        profileTable.deleteListItemInProfileTable(mEvent.identityId, "myEvent", listItem)

        ''' キャンセルされたらいいねをしていた人にお知らせを送る
        message = {
            'eventId' : int(event.eventId),
            'title' : event.eventName
        }

        if("favorite" in itemEvent['Item']):
            list = itemEvent['Item']['favorite']
            message['list'] = list
            messageJson = json.dumps(message)
            topic.publish(
                Message = messageJson
            )
        '''

        res = { "result" : 1 }
        return Successed(res)
    
    except:
        import traceback
        traceback.print_exc()
        return Failured()