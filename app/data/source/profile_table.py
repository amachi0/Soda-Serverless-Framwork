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