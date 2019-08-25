import unittest
import json

import boto3
from moto import mock_s3

from test.utility import init_db, lambda_gateway_event_base, create_image_bucket
from app.util.decimalencoder import DecimalEncoder

from app.functions.api_gateway.upload_binary.upload_binary import upload_binary


class MyTestCase(unittest.TestCase):

    @mock_s3
    def test_upload_binary(self):
        create_image_bucket()

        event = lambda_gateway_event_base()
        event['body'] = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAZIAAAGSCAYAAADJgkf6AAAAAXNSR0I' \
                        'Ars4c6QAAAAlwSFlzAAAXEgAAFxIBZ5/SUgAAN8dJREFUeAHt3Qt8XFWdwPFz7kzSNi1QWN5QykJ9' \
                        'UYFiJZOZFLDuosCCy0NYV3bxxWNxV0Vp0gKKgwi0SRFXwF3AxyIPFRZFRLpQtEjNZJJSKPhBBYpAeQlS6'

        # ------------------------------------------------------------
        # execute
        # ------------------------------------------------------------
        response = upload_binary(event, {})

        # ------------------------------------------------------------
        # TEST
        # ------------------------------------------------------------
        self.assertEqual(200, response['statusCode'], 'ステータスコード')


if __name__ == '__main__':
    unittest.main()
