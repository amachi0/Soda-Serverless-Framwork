import boto3
import os


class SequenceTable():
    # 連番を作るためのテーブル

    def __init__(self, event):
        dynamodb = boto3.resource('dynamodb')
        tableName = os.environ['SEQUENCE_TABLE']

        if 'isOffline' in event and event['isOffline']:
            dynamodb = boto3.resource(
                'dynamodb', endpoint_url='http://localhost:8000')
            tableName = "dev-sequence"

        self.table = dynamodb.Table(tableName)

    def next_seq(self):
        res = self.table.update_item(
            Key={
                'tableName': "event"
            },
            UpdateExpression="set seq = seq + :val",
            ExpressionAttributeValues={
                ':val': 1
            },
            ReturnValues="UPDATED_NEW"
        )
        return res['Attributes']['seq']
