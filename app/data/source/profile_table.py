import boto3
import os
from app.data.profile import Profile

class ProfileTable(Profile):
    def __init__(self):
        dynamodb = boto3.resource('dynamodb')
        tableName = os.environ['PROFILE_TABLE']
        self.table = dynamodb.Table(tableName)
        self.sodaIdIndex = os.environ['PROFILE_SODA_ID_INDEX']
    
    def insertProfile(self, profile=Profile):
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
                "favoriteEvent" : profile.favoriteEvent,
                "myEvent" : profile.myEvent,
                "templates" : profile.templates,
                "isAcceptMail" : profile.isAcceptMail,
            }
        )
    
    def changeProfile(self, profile=Profile):
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