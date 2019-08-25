import unittest
from unittest import mock
import json

import boto3
from moto import mock_dynamodb2

from test.utility import init_db, lambda_gateway_event_base
from app.util.decimalencoder import DecimalEncoder

from app.functions.api_gateway.favorite.push_favorite import push_favorite
from app.functions.api_gateway.favorite.cancel_favorite import cancel_favorite

class MyTestCase(unittest.TestCase):

    @mock_dynamodb2
    def test_push_favorite(self):
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
            'universities': ['立命館大学']
        }
        table.put_item(Item=item)

        table = dynamodb.Table('event')
        item = {
            'eventId': 1,
            'identityId': 'testIdentityId2',
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
            'countOfLike': 0
        }
        table.put_item(Item=item)

        event = lambda_gateway_event_base()
        body = {
            'eventId': 1,
            'identityId': 'testIdentityId'
        }
        event['body'] = json.dumps(body, cls=DecimalEncoder)

        # ------------------------------------------------------------
        # execute
        # ------------------------------------------------------------
        response = push_favorite(event, {})

        # ------------------------------------------------------------
        # TEST
        # ------------------------------------------------------------
        self.assertEqual(200, response['statusCode'], 'ステータスコード')

    @mock_dynamodb2
    @mock.patch('app.functions.api_gateway.favorite.cancel_favorite.EventTable.removeFavorite')
    @mock.patch('app.functions.api_gateway.favorite.cancel_favorite.ProfileTable.deleteListItemInProfileTable')
    def test_cancel_favorite(self, mock1, mock2):
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
            'universities': ['立命館大学'],
            'favoriteEvent': [1]
        }
        table.put_item(Item=item)

        table = dynamodb.Table('event')
        item = {
            'eventId': 1,
            'identityId': 'testIdentityId2',
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
            'countOfLike': 1,
            'favorite': ['testIdentityId']
        }
        table.put_item(Item=item)

        event = lambda_gateway_event_base()
        body = {
            'eventId': 1,
            'identityId': 'testIdentityId'
        }
        event['body'] = json.dumps(body, cls=DecimalEncoder)

        # ------------------------------------------------------------
        # execute
        # ------------------------------------------------------------
        response = cancel_favorite(event, {})

        # ------------------------------------------------------------
        # TEST
        # ------------------------------------------------------------
        self.assertEqual(200, response['statusCode'], 'ステータスコード')


if __name__ == '__main__':
    unittest.main()
