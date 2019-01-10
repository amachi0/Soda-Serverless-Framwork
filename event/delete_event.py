import json
import boto3
import traceback
import os

dynamodb = boto3.resource('dynamodb')
sns = boto3.resource('sns')
topic_name = os.environ['SNS_CANCEL_TOPIC']
topic = sns.Topic(topic_name)
event_table_name = os.environ['EVENT_TABLE']
profile_table_name = os.environ['PROFILE_TABLE']
endPoint = os.environ['CLOUD_SEARCH_DOC_ENDPOINT']
cloudSearch = boto3.client('cloudsearchdomain', endpoint_url = endPoint)

def delete_event(event, context):
    try:
        param = json.loads(event["body"])
        eventId = param['eventId']
        identityId = param['identityId']
        eventTable = dynamodb.Table(event_table_name)
        itemEvent = eventTable.get_item(
            Key = {
                "eventId" : eventId
            }
        )
        if (identityId != itemEvent['Item']['identityId']):
            res = {
                "result" : 0
            }
            return {
                'statusCode' : 200,
                'headers' : {
                    'content-type' : 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body' : json.dumps(res)
            }
        message = {
            'eventId' : int(itemEvent['Item']['eventId']),
            'title' : itemEvent['Item']['eventName']
        }
        if("favorite" in itemEvent['Item']):
            list = itemEvent['Item']['favorite']
            message['list'] = list
            messageJson = json.dumps(message)
            topic.publish(
                Message = messageJson
            )

        eventTable.delete_item(
            Key = {
                'eventId' : eventId
            }
        )
        
        profileTable = dynamodb.Table(profile_table_name)
        item_profile = profileTable.get_item(
            Key = {
                'identityId' : identityId
            }
        )
        myEvent = item_profile['Item']['myEvent']
        myEvent.remove(eventId)
        
        profileTable.update_item(
            Key = {
                'identityId' : identityId
            },
            UpdateExpression = "set myEvent=:x",
            ExpressionAttributeValues = {
                ':x' : myEvent
            }
        )
        
        res = {
            "result" : 1
        }
        return {
            'statusCode' : 200,
            'headers' : {
                'content-type' : 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body' : json.dumps(res)
        }
    
    except:
        import traceback
        traceback.print_exc()
        res_error = {
            "result" : 0
        }
        return {
            'statusCode' : 500,
            'headers' : {
                'content-type' : 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body' : json.dumps(res_error)
        }