import boto3
import os
from boto3.dynamodb.conditions import Key, Attr
from app.data.profile import Profile


class ProfileTable(Profile):
    def __init__(self, event):
        dynamodb = boto3.resource('dynamodb')
        tableName = os.environ['PROFILE_TABLE']

        if 'isOffline' in event and event['isOffline']:
            dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
            tableName = "dev-profile"
        
        self.table = dynamodb.Table(tableName)
        self.sodaIdIndex = os.environ['PROFILE_SODA_ID_INDEX']
        self.checkEmailIndex = os.environ['PROFILE_CHECK_Email_INDEX']
        self.checkSodaIdIndex = os.environ['PROFILE_CHECK_SODA_ID_INDEX']

    def insert(self, profile=Profile):
        self.table.put_item(
            Item = {
                "identityId" : profile.identityId,
                "sodaId" : profile.sodaId,
                "email" : profile.email,
                "universities" : profile.universities,
                "urlData" : profile.urlData,
                "name" : profile.name,
                "profile" : profile.profile,
                "twitter" : profile.twitter,
                "facebook" : profile.facebook,
                "instagram" : profile.instagram,
                "isAcceptMail" : profile.isAcceptMail
            },
            ConditionExpression = "attribute_not_exists(identityId)"
        )
    
    def change(self, profile=Profile):
        self.table.update_item(
            Key = {
                "identityId" : profile.identityId
            },
            UpdateExpression = "set urlData=:b,#a=:c,universities=:d,isAcceptMail=:e,profile=:f,twitter=:g,facebook=:h,instagram=:i",
            ExpressionAttributeNames = {
                '#a' : "name"
            },
            ExpressionAttributeValues = {
                ':b' : profile.urlData,
                ':c' : profile.name,
                ':d' : profile.universities,
                ':e' : profile.isAcceptMail,
                ':f' : profile.profile,
                ':g' : profile.twitter,
                ':h' : profile.facebook,
                ':i' : profile.instagram
            }
        )
    
    def addListItemInProfileTable(self, identityId, setName, listItem):
        self.table.update_item(
            Key = {
                "identityId" : identityId
            },
            UpdateExpression = "ADD #attribute :x",
            ExpressionAttributeNames= {
                '#attribute': setName
            },
            ExpressionAttributeValues = {
                ':x' : set(listItem)
            }
        )
    
    def deleteListItemInProfileTable(self, identityId, setName, listItem):
        self.table.update_item(
            Key = {
                "identityId" : identityId
            },
            UpdateExpression = "DELETE #attribute :x",
            ExpressionAttributeNames= {
                '#attribute': setName
            },
            ExpressionAttributeValues = {
                ':x' : set(listItem)
            }
        )
    
    def getFromSodaId(self, sodaId):
        itemList = self.table.query(
            IndexName = self.sodaIdIndex,
            KeyConditionExpression = Key('sodaId').eq(sodaId)
        )
        item = itemList['Items'][0]
        profile = Profile(**item)
        return profile
    
    def getFromIdentityId(self, identityId, projectionExpression=None):
        item = self.table.get_item(
            Key = {
                "identityId" : identityId
            },
            ExpressionAttributeNames = {
                '#name' : "name"
            },
            ProjectionExpression = projectionExpression
        )
        param = item['Item']
        profile = Profile(**param)
        return profile
    
    def isValidEmail(self, email):
        itemList = self.table.query(
			IndexName = self.checkEmailIndex,
			KeyConditionExpression = Key('email').eq(email)
		)
        if (itemList['Count'] == 0):
            return True
        else:
            return False
    
    def isValidSodaId(self, sodaId):
        itemList = self.table.query(
            IndexName = self.checkSodaIdIndex,
            KeyConditionExpression = Key('sodaId').eq(sodaId)
        )
        if (itemList['Count'] == 0):
            return True
        else:
            return False