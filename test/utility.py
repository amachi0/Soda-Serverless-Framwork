import json
import os

import boto3
from moto import mock_dynamodb2, mock_s3


@mock_dynamodb2
def init_db():
    """
    テスト用にDynamoDBのスキーマとデータを生成する。
    :return:
    """
    client = boto3.resource('dynamodb', region_name='ap-northeast-1')
    client.create_table(**{
        'TableName': 'profile',
        'AttributeDefinitions': [
            {
                'AttributeName': 'identityId',
                'AttributeType': 'S'
            }
        ],
        'KeySchema': [{
            'AttributeName': 'identityId',
            'KeyType': 'HASH'
        }],
        'ProvisionedThroughput': {
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        },
        'GlobalSecondaryIndexes': [
            {
                'IndexName': 'check-sodaId-index',
                'KeySchema': [
                    {
                        'AttributeName': 'sodaId',
                        'KeyType': 'HASH'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL',
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                }
            },
            {
                'IndexName': 'check-email-index',
                'KeySchema': [
                    {
                        'AttributeName': 'email',
                        'KeyType': 'HASH'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL',
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                }
            },
            {
                'IndexName': 'sodaId-index',
                'KeySchema': [
                    {
                        'AttributeName': 'sodaId',
                        'KeyType': 'HASH'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL',
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                }
            },
        ]
    })

    client.create_table(**{
        'TableName': 'event',
        'AttributeDefinitions': [
            {
                'AttributeName': 'eventId',
                'AttributeType': 'N'
            }
        ],
        'KeySchema': [{
            'AttributeName': 'eventId',
            'KeyType': 'HASH'
        }],
        'ProvisionedThroughput': {
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        },
        'GlobalSecondaryIndexes': [
            {
                'IndexName': 'indexKey-updateTime-index',
                'KeySchema': [
                    {
                        'AttributeName': 'indexKey',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'updateTime',
                        'KeyType': 'RANGE'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL',
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                }
            },
            {
                'IndexName': 'status-start-index',
                'KeySchema': [
                    {
                        'AttributeName': 'status',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'start',
                        'KeyType': 'RANGE'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL',
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                }
            },
            {
                'IndexName': 'status-updateTime-index',
                'KeySchema': [
                    {
                        'AttributeName': 'status',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'updateTime',
                        'KeyType': 'RANGE'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL',
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                }
            }, {
                'IndexName': 'status-countOfLike-index',
                'KeySchema': [
                    {
                        'AttributeName': 'status',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'countOfLike',
                        'KeyType': 'RANGE'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL',
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                }
            },

        ]
    })

    client.create_table(**{
        'TableName': 'sequence',
        'AttributeDefinitions': [
            {
                'AttributeName': 'tableName',
                'AttributeType': 'S'
            }
        ],
        'KeySchema': [
            {
                'AttributeName': 'tableName',
                'KeyType': 'HASH'
            }
        ],
        'ProvisionedThroughput': {
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    })

    sequenceTable = client.Table('sequence')
    item = {
        'tableName': 'event',
        'event': 0
    }
    sequenceTable.put_item(Item=item)


@mock_s3
def create_json_bucket():
    s3 = boto3.client('s3', region_name='ap-northeast-1')
    s3r = boto3.resource('s3', region_name='ap-northeast-1')
    s3.create_bucket(Bucket=os.environ['S3_JSON_BUCKET'])

    bucket = s3r.Bucket(os.environ['S3_JSON_BUCKET'])
    paths = ['faqs.json', 'terms.json', 'university.json']
    for path in paths:
        body = {
            "test_body":  'body_of_' + path
        }
        obj = bucket.Object(path)
        obj.put(Body=json.dumps(body), ContentType='application/json')


@mock_s3
def create_image_bucket():
    s3 = boto3.client('s3', region_name='ap-northeast-1')
    s3r = boto3.resource('s3', region_name='ap-northeast-1')
    s3.create_bucket(Bucket=os.environ['S3_IMAGE_BUCKET'])


def create_sns_topic(topic_name):
    sns = boto3.client("sns", region_name='ap-northeast-1')
    res = sns.create_topic(Name=topic_name)
    topic_arn = res.get('TopicArn')

    return topic_arn


def lambda_gateway_event_base():
    """
    API Gatewayからのlambdaのインタフェースとなるeventを作成する

    :return:
    """
    event = {
        'body': {},
        'queryStringParameters': {},
    }

    return event


def mock_failed(*args, **kwargs):
    return {
        'statusCode': 500,
        'headers': {
            'content-type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({"result": 0})
    }
