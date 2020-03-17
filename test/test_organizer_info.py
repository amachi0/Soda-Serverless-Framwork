import unittest
from unittest import mock
import json

import boto3
from moto import mock_dynamodb2

from test.utility import init_db, lambda_gateway_event_base
from app.util.decimalencoder import DecimalEncoder

from app.functions.api_gateway.organizer_info.organizer_info import organizer_info


class MyTestCase(unittest.TestCase):

    @mock_dynamodb2
    def test_organizer_info(self):
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
            'countOfLike': 0
        }
        table.put_item(Item=item)

        event = lambda_gateway_event_base()
        event['queryStringParameters'] = {'eventId': 1}

        # ------------------------------------------------------------
        # execute
        # ------------------------------------------------------------
        response = organizer_info(event, {})

        # ------------------------------------------------------------
        # TEST
        # ------------------------------------------------------------
        self.assertEqual(200, response['statusCode'], 'ステータスコード')


if __name__ == '__main__':
    unittest.main()
