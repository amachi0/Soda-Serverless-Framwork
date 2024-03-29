import boto3
import os
from boto3.dynamodb.conditions import Key, Attr
from app.data.profile import Profile
from app.logic.logic_profile_table \
    import getListKeysForBatchGetProfile, getProfilesFromBatchGetResponse, \
    getProfilesFromResponse, hasNoItemInResponse


class ProfileTable(Profile):
    def __init__(self, event):
        dynamodb = boto3.resource('dynamodb')
        self.client = boto3.client('dynamodb')
        self.tableName = os.environ['PROFILE_TABLE']

        if 'isOffline' in event and event['isOffline']:
            dynamodb = boto3.resource(
                'dynamodb', endpoint_url='http://localhost:8000')
            self.client = boto3.client(
                'dynamodb', endpoint_url='http://localhost:8000')
            self.tableName = "dev-profile"

        self.table = dynamodb.Table(self.tableName)
        self.sodaIdIndex = os.environ['PROFILE_SODA_ID_INDEX']
        self.checkEmailIndex = os.environ['PROFILE_CHECK_Email_INDEX']
        self.checkSodaIdIndex = os.environ['PROFILE_CHECK_SODA_ID_INDEX']

    def insert(self, profile=Profile):
        self.table.put_item(
            Item={
                "identityId": profile.identityId,
                "sodaId": profile.sodaId,
                "email": profile.email,
                "universities": profile.universities,
                "urlData": profile.urlData,
                "name": profile.name,
                "profile": profile.profile,
                "twitter": profile.twitter,
                "facebook": profile.facebook,
                "instagram": profile.instagram,
                "isAcceptMail": profile.isAcceptMail
            },
            ConditionExpression="attribute_not_exists(identityId)"
        )

    def change(self, profile=Profile):
        self.table.update_item(
            Key={
                "identityId": profile.identityId
            },
            UpdateExpression="set urlData=:b,#a=:c,universities=:d,\
                isAcceptMail=:e,profile=:f,\
                twitter=:g,facebook=:h,instagram=:i",
            ExpressionAttributeNames={
                '#a': "name"
            },
            ExpressionAttributeValues={
                ':b': profile.urlData,
                ':c': profile.name,
                ':d': profile.universities,
                ':e': profile.isAcceptMail,
                ':f': profile.profile,
                ':g': profile.twitter,
                ':h': profile.facebook,
                ':i': profile.instagram
            }
        )

    def addListItemInProfileTable(self, identityId, setName, listItem):
        self.table.update_item(
            Key={
                "identityId": identityId
            },
            UpdateExpression="ADD #attribute :x",
            ExpressionAttributeNames={
                '#attribute': setName
            },
            ExpressionAttributeValues={
                ':x': set(listItem)
            },
            ConditionExpression=Attr('identityId').eq(identityId)
        )

    def deleteListItemInProfileTable(self, identityId, setName, listItem):
        self.table.update_item(
            Key={
                "identityId": identityId
            },
            UpdateExpression="DELETE #attribute :x",
            ExpressionAttributeNames={
                '#attribute': setName
            },
            ExpressionAttributeValues={
                ':x': set(listItem)
            }
        )

    def getFromSodaId(self, sodaId):
        itemList = self.table.query(
            IndexName=self.sodaIdIndex,
            KeyConditionExpression=Key('sodaId').eq(sodaId)
        )
        item = itemList['Items'][0]
        profile = Profile(**item)
        return profile

    def getOrganizerInfo(self, identityId):
        item = self.table.get_item(
            Key={
                "identityId": identityId
            },
            ProjectionExpression='sodaId, #attributeName, urlData, profile, \
                twitter, facebook, instagram',
            ExpressionAttributeNames={
                '#attributeName': 'name'
            }
        )

        param = item['Item']
        profile = Profile(**param)
        return profile

    def getFromIdentityId(self, identityId, projectionExpression=None):
        item = self.table.get_item(
            Key={
                "identityId": identityId
            },
            ProjectionExpression=projectionExpression
        )

        param = item['Item']
        profile = Profile(**param)
        return profile

    def batchGetFromListIdentityId(self, listIdentityId):
        listKeys = getListKeysForBatchGetProfile(listIdentityId)

        res = self.client.batch_get_item(
            RequestItems={
                self.tableName: {
                    'Keys': listKeys,
                    'ProjectionExpression': 'email, isAcceptMail'
                }
            }
        )

        profiles = getProfilesFromBatchGetResponse(res, self.tableName)
        return profiles

    def scanForWeekMail(self):
        res = self.table.scan(
            FilterExpression=Attr('isAcceptMail').eq(True),
            ProjectionExpression='email'
        )
        items = res['Items']
        while 'LastEvaluatedKey' in res:
            res = self.table.scan(
                ExclusiveStartKey=res['LastEvaluatedKey'])
            items.extend(res['Items'])

        profiles = getProfilesFromResponse(items)
        return profiles

    def isValidEmail(self, email):
        res = self.table.query(
            IndexName=self.checkEmailIndex,
            KeyConditionExpression=Key('email').eq(email)
        )

        hasItem = hasNoItemInResponse(res)
        return hasItem

    def isValidSodaId(self, sodaId):
        res = self.table.query(
            IndexName=self.checkSodaIdIndex,
            KeyConditionExpression=Key('sodaId').eq(sodaId)
        )

        hasItem = hasNoItemInResponse(res)
        return hasItem
