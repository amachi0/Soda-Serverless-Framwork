import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')
profile_table_name = os.environ['PROFILE_TABLE']
table = dynamodb.Table(profile_table_name)
sesRegion = os.environ['SES_REGION']
ses = boto3.client('ses', region_name = sesRegion)
MAILFROM = os.environ['MAIL_ADRESS_FROM_SODA']

def sendmail(to, subject, body):
    client = boto3.client('ses', region_name = sesRegion)
    client.send_email(
        Source = MAILFROM,
        Destination = {
            'ToAddresses' : [
                    to
                ]
        },
        Message = {
            'Subject' : {
                'Data' : subject,
                'Charset' : 'UTF-8'
            },
            'Body' : {
                'Text' : {
                    'Data' : body,
                    'Charset' : 'UTF-8'
                }
            }
        }
    )

def cancel_sns(event, context):
    try:
        message = event['Records'][0]['Sns']['Message']
        d = json.loads(message)
        print(d)
        eventId = d['eventId']
        title = d['title']
        list = d['list']
        listKey = []
        for identityId in list:
            dic = {
                "identityId" : {
                    "S" : identityId
                }
            }
            listKey.append(dic)
            
            #それぞれのいいねをしていたユーザーのfavoriteEventから中止されたイベントを削除
            itemProfile = table.get_item(
                Key = {
                    'identityId' : identityId
                }
            )
            listEventId = itemProfile['Item']['favoriteEvent']
            listEventId.remove(eventId)
            table.update_item(
                Key = {
                    'identityId' : identityId
                },
                UpdateExpression = 'set favoriteEvent=:x',
                ExpressionAttributeValues = {
                    ':x' : listEventId
                }
            )
        
        res = client.batch_get_item(
            RequestItems = {
                profile_table_name : {
                    'Keys' : listKey
                }
            }
        )
        
        for user in res['Responses'][profile_table_name]:
            if not ("isAcceptMail" in user):
                continue
            
            if not ("email" in user):
                continue
            
            if(user['isAcceptMail']):
                email = user['email']['S']
                ses.send_email(
                    Source = MAILFROM,
                    Destination = {
                        'ToAddresses' : [
                            email
                        ]
                    },
                    Message = {
                        'Subject' : {
                            'Data' : 'イベント中止のお知らせ',
                            'Charset' : 'UTF-8'
                        },
                        'Body' : {
                            'Text' : {
                                'Data' : title + "が中止されました",
                                'Charset' : 'UTF-8'
                            }
                        }
                    }
                )
        res = {
            "result" : 1
        }
        return {
            'statusCode' : 200,
            'headers' : {
                'content-type' : 'application/json'
            },
            'body' : json.dumps(res)
        }
    
    except:
        import  traceback
        traceback.print_exc()
        res = {
            "result" : 0
        }
        return {
            'statusCode' : 500,
            'headers' : {
                'content-type' : 'application/json'
            },
            'body' : json.dumps(res)
        }