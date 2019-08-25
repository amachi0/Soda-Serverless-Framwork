import unittest
import json

import boto3
from moto import mock_dynamodb2

from test.utility import init_db, lambda_gateway_event_base

from app.functions.api_gateway.created_event.created_event import created_event


class MyTestCase(unittest.TestCase):

    @mock_dynamodb2
    def test_created_event(self):
        dynamodb = boto3.resource('dynamodb')

        # ------------------------------------------------------------
        # テストデータ投入
        # ------------------------------------------------------------
        init_db()
        table = dynamodb.Table('profile')
        item = {
            'identityId': 'testIdentityId',
            'sodaId': 'testSodaId',
            'email': 'test@test.com',
            'urlData': 'testUrlData',
            'name': 'testName',
            'universities': [
                '立命館大学'
            ],
            'myEvent': [1, 2],
            'favoriteEvent': [1]
        }
        table.put_item(Item=item)

        table = dynamodb.Table('event')
        item = {
            'eventId': 1,
            'identityId': 'testIdentityId',
            'eventName': 'イベント名',
            'urlData': 'https://nangngnainil34982379gsesssgg',
            'university': '立命館大学',
            'price': '500円',
            'location': 'BKC アクロスウィング',
            'start': 1526000000,
            'end': 1528000000,
            'updateTime': 1628000000,
            'qualification': '初心者でもOK!',
            'detail': 'テスト',
            'contact': 'test@test.com',
            'isPrivate': False,
            'sponsor': 'なんとかサークル',
            'entry': 'こちらのURLまで',
            'favorite': ['testIdentityId'],
            'countOfLike': 1
        }
        table.put_item(Item=item)

        item = {
            'eventId': 2,
            'identityId': 'testIdentityId',
            'eventName': 'イベント名２',
            'urlData': 'https://nangngnainil34982379gsesssgs',
            'university': '立命館大学',
            'price': '1000円',
            'location': 'BKC 噴水前',
            'start': 1526000000,
            'end': 1528000000,
            'updateTime': 1628000000,
            'qualification': '初心者でもOK!',
            'detail': 'テスト',
            'contact': 'test@test.com',
            'isPrivate': False,
            'sponsor': 'なんとかサークル',
            'entry': 'こちらのURLまで',
            'countOfLike': 0
        }
        table.put_item(Item=item)

        event = lambda_gateway_event_base()
        event['queryStringParameters'] = {
            'sodaId': 'testSodaId',
            'page': 0
        }

        # ------------------------------------------------------------
        # execute
        # ------------------------------------------------------------
        response = created_event(event, {})

        # ------------------------------------------------------------
        # TEST
        # ------------------------------------------------------------
        self.assertEqual(200, response['statusCode'], 'ステータスコード')


    @mock_dynamodb2
    def test_created_event_no_event(self):
        dynamodb = boto3.resource('dynamodb')

        # ------------------------------------------------------------
        # テストデータ投入
        # ------------------------------------------------------------
        init_db()
        table = dynamodb.Table('profile')
        item = {
            'identityId': 'testIdentityId',
            'sodaId': 'testSodaId',
            'email': 'test@test.com',
            'urlData': 'testUrlData',
            'name': 'testName',
            'universities': [
                '立命館大学'
            ],
            'myEvent': [],
            'favoriteEvent': [1]
        }
        table.put_item(Item=item)

        event = lambda_gateway_event_base()
        event['queryStringParameters'] = {
            'sodaId': 'testSodaId',
            'page': 0
        }

        # ------------------------------------------------------------
        # execute
        # ------------------------------------------------------------
        response = created_event(event, {})

        # ------------------------------------------------------------
        # TEST
        # ------------------------------------------------------------
        self.assertEqual(json.dumps({}), response['body'])


    @mock_dynamodb2
    def test_created_event_invalid(self):
        # pageの値が不正な時

        dynamodb = boto3.resource('dynamodb')

        # ------------------------------------------------------------
        # テストデータ投入
        # ------------------------------------------------------------
        init_db()
        table = dynamodb.Table('profile')
        item = {
            'identityId': 'testIdentityId',
            'sodaId': 'testSodaId',
            'email': 'test@test.com',
            'urlData': 'testUrlData',
            'name': 'testName',
            'universities': [
                '立命館大学'
            ],
            'myEvent': [1, 2],
            'favoriteEvent': [1]
        }
        table.put_item(Item=item)

        table = dynamodb.Table('event')
        item = {
            'eventId': 1,
            'identityId': 'testIdentityId',
            'eventName': 'イベント名',
            'urlData': 'https://nangngnainil34982379gsesssgg',
            'university': '立命館大学',
            'price': '500円',
            'location': 'BKC アクロスウィング',
            'start': 1526000000,
            'end': 1528000000,
            'updateTime': 1628000000,
            'qualification': '初心者でもOK!',
            'detail': 'テスト',
            'contact': 'test@test.com',
            'isPrivate': False,
            'sponsor': 'なんとかサークル',
            'entry': 'こちらのURLまで',
            'favorite': ['testIdentityId'],
            'countOfLike': 1
        }
        table.put_item(Item=item)

        item = {
            'eventId': 2,
            'identityId': 'testIdentityId',
            'eventName': 'イベント名２',
            'urlData': 'https://nangngnainil34982379gsesssgs',
            'university': '立命館大学',
            'price': '1000円',
            'location': 'BKC 噴水前',
            'start': 1526000000,
            'end': 1528000000,
            'updateTime': 1628000000,
            'qualification': '初心者でもOK!',
            'detail': 'テスト',
            'contact': 'test@test.com',
            'isPrivate': False,
            'sponsor': 'なんとかサークル',
            'entry': 'こちらのURLまで',
            'countOfLike': 0
        }
        table.put_item(Item=item)

        event = lambda_gateway_event_base()
        event['queryStringParameters'] = {
            'sodaId': 'testSodaId',
            'page': 1
        }

        # ------------------------------------------------------------
        # execute
        # ------------------------------------------------------------
        response = created_event(event, {})

        # ------------------------------------------------------------
        # TEST
        # ------------------------------------------------------------
        self.assertEqual(json.dumps({}), response['body'])

if __name__ == '__main__':
    unittest.main()
