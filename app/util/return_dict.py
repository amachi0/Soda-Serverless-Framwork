import json
import os
import requests
from app.util.decimalencoder import DecimalEncoder

def Successed(body):
    return {
            'statusCode' : 200,
            'headers' : {
                'content-type' : 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body' : json.dumps(body, cls=DecimalEncoder)
        }

def Failured(error):

    #暇やったらここにslackに通知する処理を追加
    slackWebHookUrl = os.environ['SLACK_WEB_HOOK_URL']
    requests.post(slackWebHookUrl, data=json.dumps({"text" : error}))
    return {
            'statusCode' : 500,
            'headers' : {
                'content-type' : 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body' : json.dumps({"result" : 0})
        }