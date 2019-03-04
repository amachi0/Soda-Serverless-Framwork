import json
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

def Failured():
    #暇やったらここにslackに通知する処理を追加
    return {
            'statusCode' : 500,
            'headers' : {
                'content-type' : 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body' : json.dumps({"result" : 0})
        }