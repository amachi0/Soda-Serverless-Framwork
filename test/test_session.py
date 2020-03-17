import unittest
import json

import boto3
from moto import mock_dynamodb2

from test.utility import init_db, lambda_gateway_event_base

from app.functions.api_gateway.session.check_email import check_email
from app.functions.api_gateway.session.check_soda_id import check_soda_id


class MyTestCase(unittest.TestCase):

    @mock_dynamodb2
    def test_check_email(self):

        # ------------------------------------------------------------
        # テストデータ投入
        # ------------------------------------------------------------
        init_db()

        event = lambda_gateway_event_base()
        event['queryStringParameters'] = {
            'email': 'test@test.com'
        }

        # ------------------------------------------------------------
        # execute
        # ------------------------------------------------------------
        response = check_email(event, {})

        # ------------------------------------------------------------
        # TEST
        # ------------------------------------------------------------
        res_body = json.loads(response['body'])
        self.assertTrue(res_body['result'])
        self.assertEqual(200, response['statusCode'], 'ステータスコード')

    @mock_dynamodb2
    def test_check_email_invalid(self):
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
        event['queryStringParameters'] = {
            'email': 'test@test.com'
        }

        # ------------------------------------------------------------
        # execute
        # ------------------------------------------------------------
        response = check_email(event, {})

        # ------------------------------------------------------------
        # TEST
        # ------------------------------------------------------------
        res_body = json.loads(response['body'])
        self.assertFalse(res_body['result'])
        self.assertEqual(200, response['statusCode'], 'ステータスコード')

    @mock_dynamodb2
    def test_check_sodaId(self):

        # ------------------------------------------------------------
        # テストデータ投入
        # ------------------------------------------------------------
        init_db()

        event = lambda_gateway_event_base()
        event['queryStringParameters'] = {
            'sodaId': 'testSodaId'
        }

        # ------------------------------------------------------------
        # execute
        # ------------------------------------------------------------
        response = check_soda_id(event, {})

        # ------------------------------------------------------------
        # TEST
        # ------------------------------------------------------------
        res_body = json.loads(response['body'])
        self.assertTrue(res_body['result'])
        self.assertEqual(200, response['statusCode'], 'ステータスコード')

    @mock_dynamodb2
    def test_check_sodaId_invalid(self):
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
        event['queryStringParameters'] = {
            'sodaId': 'testSodaId'
        }

        # ------------------------------------------------------------
        # execute
        # ------------------------------------------------------------
        response = check_soda_id(event, {})

        # ------------------------------------------------------------
        # TEST
        # ------------------------------------------------------------
        res_body = json.loads(response['body'])
        self.assertFalse(res_body['result'])
        self.assertEqual(200, response['statusCode'], 'ステータスコード')


if __name__ == '__main__':
    unittest.main()
