import unittest
from unittest import mock
import json
import os

import boto3
from moto import mock_dynamodb2, mock_sns

from test.utility import init_db, lambda_gateway_event_base, create_sns_topic, mock_failed
from app.util.decimalencoder import DecimalEncoder

from app.functions.api_gateway.event.create_event import create_event
from app.functions.api_gateway.event.change_event import change_event
from app.functions.api_gateway.event.detail_event import detail_event
from app.functions.api_gateway.event.delete_event import delete_event


class MyTestCase(unittest.TestCase):

    @mock_dynamodb2
    def test_create_event(self):
        dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')

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
            'universities': ['立命館大学']
        }
        table.put_item(Item=item)

        event = lambda_gateway_event_base()
        body = {
            'identityId': 'testIdentityId',
            'eventName': 'イベント名',
            'urlData': 'https://nangngnainil34982379gsesssgg',
            'university': '立命館大学',
            'price': '500円',
            'location': 'BKC アクロスウィング',
            'start': 1526000000,
            'end': 1528000000,
            'qualification': '初心者でもOK!',
            'detail': 'テスト',
            'contact': 'amachi@gmail.com',
            'isPrivate': False,
            'sponsor': 'なんとかサークル',
            'entry': 'こちらのURLまで'
        }
        event['body'] = json.dumps(body, cls=DecimalEncoder)

        # ------------------------------------------------------------
        # execute
        # ------------------------------------------------------------
        response = create_event(event, {})

        # ------------------------------------------------------------
        # TEST
        # ------------------------------------------------------------
        self.assertEqual(200, response['statusCode'], 'ステータスコード')

    @mock_dynamodb2
    def test_change_event(self):
        dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')

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
            'universities': ['立命館大学'],
            'myEvent': [1]
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

        event = lambda_gateway_event_base()
        body = {
            'eventId': 1,
            'identityId': 'testIdentityId',
            'eventName': '変更',
            'urlData': 'https://nangngnainil34982379gsesssgg',
            'university': '立命館大学',
            'price': '1000円',
            'location': 'BKC アクロスウィング',
            'start': 1526000000,
            'end': 1528000000,
            'qualification': '初心者でもOK!',
            'detail': 'テスト',
            'contact': 'amachi@gmail.com',
            'isPrivate': False,
            'sponsor': 'なんとかサークル',
            'entry': 'こちらのURLまで'
        }
        event['body'] = json.dumps(body, cls=DecimalEncoder)

        # ------------------------------------------------------------
        # execute
        # ------------------------------------------------------------
        response = change_event(event, {})

        # ------------------------------------------------------------
        # TEST
        # ------------------------------------------------------------
        self.assertEqual(200, response['statusCode'], 'ステータスコード')

    @mock_dynamodb2
    def test_detail_event(self):
        dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')

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
            'universities': ['立命館大学'],
            'myEvent': [1]
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

        event = lambda_gateway_event_base()
        event['queryStringParameters'] = {
            'eventId': 1,
            'identityId': 'testIdentityId'
        }

        # ------------------------------------------------------------
        # execute
        # ------------------------------------------------------------
        response = detail_event(event, {})

        # ------------------------------------------------------------
        # TEST
        # ------------------------------------------------------------
        self.assertEqual(200, response['statusCode'], 'ステータスコード')

    @mock_dynamodb2
    def test_detail_event_favorite(self):
        dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')

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
            'universities': ['立命館大学'],
            'myEvent': [1],
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

        event = lambda_gateway_event_base()
        event['queryStringParameters'] = {
            'eventId': 1,
            'identityId': 'testIdentityId'
        }

        # ------------------------------------------------------------
        # execute
        # ------------------------------------------------------------
        response = detail_event(event, {})

        # ------------------------------------------------------------
        # TEST
        # ------------------------------------------------------------
        self.assertEqual(200, response['statusCode'], 'ステータスコード')

    @mock_dynamodb2
    def test_detail_event_guest(self):
        dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')

        # ------------------------------------------------------------
        # テストデータ投入
        # ------------------------------------------------------------
        init_db()

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

        event = lambda_gateway_event_base()
        event['queryStringParameters'] = {
            'eventId': 1,
            'identityId': 'null'
        }

        # ------------------------------------------------------------
        # execute
        # ------------------------------------------------------------
        response = detail_event(event, {})

        # ------------------------------------------------------------
        # TEST
        # ------------------------------------------------------------
        self.assertEqual(200, response['statusCode'], 'ステータスコード')

    @mock_dynamodb2
    @mock_sns
    @mock.patch('app.functions.api_gateway.event.delete_event.ProfileTable.deleteListItemInProfileTable')
    def test_delete_event(self, mock1):
        topic_arn = create_sns_topic('cancel_event')
        os.environ['SNS_CANCEL_TOPIC'] = topic_arn

        dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')
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
            'universities': ['立命館大学'],
            'myEvent': [1],
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

        event = lambda_gateway_event_base()
        body = {
            'identityId': 'testIdentityId',
            'eventId': 1
        }
        event['body'] = json.dumps(body, cls=DecimalEncoder)

        # ------------------------------------------------------------
        # execute
        # ------------------------------------------------------------
        response = delete_event(event, {})

        # ------------------------------------------------------------
        # TEST
        # ------------------------------------------------------------
        self.assertEqual(200, response['statusCode'], 'ステータスコード')

    @mock_dynamodb2
    @mock_sns
    @mock.patch('app.functions.api_gateway.event.delete_event.ProfileTable.deleteListItemInProfileTable')
    @mock.patch('app.functions.api_gateway.event.delete_event.Failured', side_effect=mock_failed)
    def test_delete_event_invalid_identityId(self, mock1, mock2):
        topic_arn = create_sns_topic('cancel_event')
        os.environ['SNS_CANCEL_TOPIC'] = topic_arn

        dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')
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
            'universities': ['立命館大学'],
            'myEvent': [1],
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

        event = lambda_gateway_event_base()
        body = {
            'identityId': 'testIdentityId2',
            'eventId': 1
        }
        event['body'] = json.dumps(body, cls=DecimalEncoder)

        # ------------------------------------------------------------
        # execute
        # ------------------------------------------------------------
        response = delete_event(event, {})

        # ------------------------------------------------------------
        # TEST
        # ------------------------------------------------------------
        self.assertEqual(500, response['statusCode'], 'ステータスコード')

    @mock_dynamodb2
    @mock_sns
    @mock.patch('app.functions.api_gateway.event.delete_event.ProfileTable.deleteListItemInProfileTable')
    def test_delete_event_no_favorite(self, mock1):
        topic_arn = create_sns_topic('cancel_event')
        os.environ['SNS_CANCEL_TOPIC'] = topic_arn

        dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')
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
            'universities': ['立命館大学'],
            'myEvent': [1]
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
        }
        table.put_item(Item=item)

        event = lambda_gateway_event_base()
        body = {
            'identityId': 'testIdentityId',
            'eventId': 1
        }
        event['body'] = json.dumps(body, cls=DecimalEncoder)

        # ------------------------------------------------------------
        # execute
        # ------------------------------------------------------------
        response = delete_event(event, {})

        # ------------------------------------------------------------
        # TEST
        # ------------------------------------------------------------
        self.assertEqual(200, response['statusCode'], 'ステータスコード')


if __name__ == '__main__':
    unittest.main()
