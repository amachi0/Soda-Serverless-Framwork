import json
import boto3
import os

MAILFROM = os.environ['MAIL_ADRESS_CONTACT']
sesRegion = os.environ['SES_REGION']

def sendmail(to, subject, body):
    client = boto3.client('ses', region_name = sesRegion)
    response = client.send_email(
        Source = MAILFROM,
        ReplyToAddresses = [MAILFROM],
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
    print(response)
        
def contact(event, context):
    try:
        print(event)
        param = json.loads(event['body'])
        email = param['email']
        title = param['title']
        description = param['description']
        mailbody = description + email
        sendmail(MAILFROM, title, mailbody)
        
        res = {
            "result" : 1
        }
        
        return {
            'statusCode' : 200,
            'headers' : {
                'context-type' : 'application/json',
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
                'context-type' : 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body' : json.dumps(res_error)
        }