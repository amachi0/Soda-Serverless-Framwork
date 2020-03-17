import unittest
import json

import boto3
from moto import mock_dynamodb2

from test.utility import init_db, lambda_gateway_event_base
from app.util.decimalencoder import DecimalEncoder

from app.functions.api_gateway.profile.create_user import create_user
from app.functions.api_gateway.profile.change_profile import change_profile
from app.functions.api_gateway.profile.get_profile import get_profile


class MyTestCase(unittest.TestCase):

    @mock_dynamodb2
    def test_create_user(self):
        # ------------------------------------------------------------
        # テストデータ投入
        # ------------------------------------------------------------
        init_db()

        event = lambda_gateway_event_base()
        body = {
            'identityId': 'testIdentityId',
            'sodaId': 'testSodaId',
            'email': 'test@test.com',
            'urlData': 'testUrlData',
            'name': 'testName',
            'universities': ['立命館大学']
        }
        event['body'] = json.dumps(body, cls=DecimalEncoder)

        # ------------------------------------------------------------
        # execute
        # ------------------------------------------------------------
        response = create_user(event, {})

        # ------------------------------------------------------------
        # TEST
        # ------------------------------------------------------------
        self.assertEqual(200, response['statusCode'], 'ステータスコード')

    @mock_dynamodb2
    def test_create_user_no_name(self):
        # ------------------------------------------------------------
        # テストデータ投入
        # ------------------------------------------------------------
        init_db()

        event = lambda_gateway_event_base()
        body = {
            'identityId': 'testIdentityId',
            'sodaId': 'testSodaId',
            'email': 'test@test.com',
            'urlData': 'testUrlData',
            'universities': ['立命館大学']
        }
        event['body'] = json.dumps(body, cls=DecimalEncoder)

        # ------------------------------------------------------------
        # execute
        # ------------------------------------------------------------
        response = create_user(event, {})

        # ------------------------------------------------------------
        # TEST
        # ------------------------------------------------------------
        self.assertEqual(200, response['statusCode'], 'ステータスコード')

    @mock_dynamodb2
    def test_change_profile(self):
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

        event = lambda_gateway_event_base()
        body = {
          "identityId": "testIdentityId",
          "urlData": "testUrlData",
          "name": "testName",
          "universities": [
            "立命館大学"
          ],
          "isAcceptMail" : True,
          "profile": "よろしく",
          "twitter": "testTwitter",
          "facebook": "testFacebook",
          "instagram": "testInstagram"
        }
        event['body'] = json.dumps(body, cls=DecimalEncoder)

        # ------------------------------------------------------------
        # execute
        # ------------------------------------------------------------
        response = change_profile(event, {})

        # ------------------------------------------------------------
        # TEST
        # ------------------------------------------------------------
        self.assertEqual(200, response['statusCode'], 'ステータスコード')

    @mock_dynamodb2
    def test_get_profile(self):
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

        event = lambda_gateway_event_base()
        event['queryStringParameters'] = {
            'sodaId': 'testSodaId'
        }

        # ------------------------------------------------------------
        # execute
        # ------------------------------------------------------------
        response = get_profile(event, {})

        # ------------------------------------------------------------
        # TEST
        # ------------------------------------------------------------
        self.assertEqual(200, response['statusCode'], 'ステータスコード')


if __name__ == '__main__':
    unittest.main()
