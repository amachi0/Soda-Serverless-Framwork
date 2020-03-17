import unittest

from moto import mock_s3

from test.utility import lambda_gateway_event_base, create_json_bucket

from app.functions.api_gateway.get_json.faqs import faqs
from app.functions.api_gateway.get_json.terms import terms
from app.functions.api_gateway.get_json.university import university


class MyTestCase(unittest.TestCase):

    @mock_s3
    def test_faqs(self):
        create_json_bucket()

        event = lambda_gateway_event_base()

        # ------------------------------------------------------------
        # execute
        # ------------------------------------------------------------
        response = faqs(event, {})

        # ------------------------------------------------------------
        # TEST
        # ------------------------------------------------------------
        self.assertEqual(200, response['statusCode'], 'ステータスコード')

    @mock_s3
    def test_terms(self):
        create_json_bucket()

        event = lambda_gateway_event_base()

        # ------------------------------------------------------------
        # execute
        # ------------------------------------------------------------
        response = terms(event, {})

        # ------------------------------------------------------------
        # TEST
        # ------------------------------------------------------------
        self.assertEqual(200, response['statusCode'], 'ステータスコード')

    @mock_s3
    def test_university(self):
        create_json_bucket()

        event = lambda_gateway_event_base()

        # ------------------------------------------------------------
        # execute
        # ------------------------------------------------------------
        response = university(event, {})

        # ------------------------------------------------------------
        # TEST
        # ------------------------------------------------------------
        self.assertEqual(200, response['statusCode'], 'ステータスコード')


if __name__ == '__main__':
    unittest.main()
