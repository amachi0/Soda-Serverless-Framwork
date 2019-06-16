import os
import boto3
from boto3.dynamodb.conditions import Key, Attr


class Query:
    def __init__(self, indexName):
        dynamodb = boto3.resource('dynamodb')
        eventTableName = os.environ['EVENT_TABLE']
        self.eventTable = dynamodb.Table(eventTableName)
        self.indexName = indexName

        # 昇順か降順かを場合分けする
        # timeline_homeの時だけクエリ結果が昇順でソートされるようにする
        if(self.indexName == os.environ['EVENT_STATUS_START_INDEX']):
            self.isIndexForward = True
        else:
            self.isIndexForward = False

        if(self.indexName == os.environ['EVENT_STATUS_UPDATETIME_INDEX']):
            self.keyConditionExpression = Key('indexKey').eq(1)
        else:
            self.keyConditionExpression = Key('status').eq('0_false')

    def queryFirstNoUniversity(self):
        result = []
        print(self.indexName)
        response = self.eventTable.query(
            IndexName=self.indexName,
            KeyConditionExpression=self.keyConditionExpression,
            ScanIndexForward=self.isIndexForward,
            Limit=3
        )
        result.extend(response['Items'])

        return result

    def queryNextNoUniversity(self, startKey):
        result = []
        response = self.eventTable.query(
            IndexName=self.indexName,
            KeyConditionExpression=self.keyConditionExpression,
            ExclusiveStartKey=startKey,
            ScanIndexForward=self.isIndexForward,
            Limit=5
        )
        result.extend(response['Items'])

        return result

    def queryFirst(self, universities):
        result = []
        response = self.eventTable.query(
            IndexName=self.indexName,
            KeyConditionExpression=self.keyConditionExpression,
            FilterExpression=Attr('university').is_in(universities),
            ScanIndexForward=self.isIndexForward,
            Limit=3
        )
        print(response)
        result.extend(response['Items'])

        while len(result) < 3:
            if("LastEvaluatedKey" in response):
                startKey = response['LastEvaluatedKey']
            else:
                break

            response = self.eventTable.query(
                IndexName=self.indexName,
                KeyConditionExpression=self.keyConditionExpression,
                FilterExpression=Attr('university').is_in(universities),
                ExclusiveStartKey=startKey,
                ScanIndexForward=self.isIndexForward,
                Limit=3
            )
            result.extend(response['Items'])

        if(len(result) > 3):
            del result[3:]

        return result

    def queryNext(self, universities, startKey):
        result = []
        response = self.eventTable.query(
            IndexName=self.indexName,
            KeyConditionExpression=self.keyConditionExpression,
            FilterExpression=Attr('university').is_in(universities),
            ExclusiveStartKey=startKey,
            ScanIndexForward=self.isIndexForward,
            Limit=5
        )
        result.extend(response['Items'])

        while len(result) < 5 and "LastEvaluatedKey" in response:
            startKey = response['LastEvaluatedKey']
            response = self.eventTable.query(
                IndexName=self.indexName,
                KeyConditionExpression=self.keyConditionExpression,
                FilterExpression=Attr('university').is_in(universities),
                ExclusiveStartKey=startKey,
                ScanIndexForward=self.isIndexForward,
                Limit=5
            )
            result.extend(response['Items'])

        if(len(result) > 5):
            del result[5:]

        return result
