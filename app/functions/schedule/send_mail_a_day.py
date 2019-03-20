import json
import boto3
import time
from boto3.dynamodb.conditions import Key
import os

dynamodb = boto3.resource('dynamodb')
eventTableName = os.environ['EVENT_TABLE']
eventTable = dynamodb.Table(eventTableName)
profileTableName = os.environ['PROFILE_TABLE']
profileTable = dynamodb.Table(profileTableName)
sesRegion = os.environ['SES_REGION']
MAILFROM = os.environ['MAIL_ADRESS_FROM_SODA']
finishIndex = os.environ['EVENT_FINISH_EVENT_INDEX']
iconURL = "https://s3-ap-northeast-1.amazonaws.com/soda-image/61dd3033-94f9-47b8-9f2c-4bbd1d68ca0f.png"


def get_user_info(identityId):
    res = profileTable.get_item(
        Key={
            'identityId': identityId
        },
        ProjectionExpression="email, isAcceptMail"
    )
    return res['Item']


def body_html(item):
    eventId = str(item['eventId'])
    eventName = item['eventName']
    urlData = item['urlData']
    body = """
        <html lang="ja">
            <head>
                <title></title>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
            </head>
            <body>
                <div class="mx-auto" style="width: 50px;">
                    <img class="mt-0 mb-2" src=""" + '"' + iconURL + '"' + """ alt="" title="">
                </div>

                <div class="card">
                    <img class="card-img-top mx-auto mt-0" src=""" + '"' + urlData + '"' + """alt="">
                    <div class="card-body">
                        <h5>""" + eventName + """</h5>
                        <a href="https://sodaevent.com/event?id=""" + eventId + '"' + """class="btn btn-primary float-right">サイトへ行く</a>
                    </div>
                </div>

                <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
                <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
            </body>
        </html>"""

    return body


def send_mail(to, item):
    ses = boto3.client('ses', region_name=sesRegion)
    eventName = item['eventName']
    eventId = item['eventId']
    ses.send_email(
        Source=MAILFROM,
        Destination={
            'ToAddresses': [
                to
            ]
        },
        Message={
            'Subject': {
                'Data': '本日のイベント',
                'Charset': 'UTF-8'
            },
            'Body': {
                'Text': {
                    'Data': "本日、" + eventName + "が開催されます。\n詳しくはこちら\nhttps://sodaevent.com/event?id=" + str(eventId),
                    'Charset': 'UTF-8'
                },
                'Html': {
                    'Data': body_html(item),
                    'Charset': 'UTF-8'
                }
            }
        }
    )


def send_mail_a_day(event, context):
    try:
        # 開始時間が一日以内のイベントをクエリで検索
        dayOfSecond = 86400
        now = int(time.time())
        day_end = now + dayOfSecond
        items = eventTable.query(
            IndexName=finishIndex,
            KeyConditionExpression=Key('finish').eq(
                0) & Key('start').lt(day_end)
        )
        print(items)
        for res in items['Items']:
            if not ("favorite" in res):
                continue
            favorite = res['favorite']
            for user in favorite:
                userData = get_user_info(user)
                if not ("isAcceptMail" in userData):
                    continue

                if not ("email" in userData):
                    continue

                if(userData['isAcceptMail']):
                    send_mail(userData['email'], res)

        res = {
            "result": 1
        }
        return {
            'statusCode': 200,
            'headers': {
                'content-type': 'application/json'
            },
            'body': json.dumps(res)
        }

    except:
        import traceback
        traceback.print_exc()
        res = {
            "result": 0
        }
        return {
            'statusCode': 500,
            'headers': {
                'content-type': 'application/json'
            },
            'body': json.dumps(res)
        }
