import unittest
import json

import boto3
from moto import mock_dynamodb2

from test.utility import init_db, lambda_gateway_event_base

from app.functions.api_gateway.id.get_soda_id import get_soda_id


class MyTestCase(unittest.TestCase):

    @mock_dynamodb2
    def test_something(self):
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
            'identityId': 'testIdentityId'
        }

        # ------------------------------------------------------------
        # execute
        # ------------------------------------------------------------
        response = get_soda_id(event, {})

        # ------------------------------------------------------------
        # TEST
        # ------------------------------------------------------------
        res_body = json.loads(response.get('body'))
        self.assertEqual('testSodaId', res_body.get('sodaId'))


if __name__ == '__main__':
    unittest.main()
