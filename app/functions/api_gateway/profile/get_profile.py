import json
import boto3
import os
from app.util.return_dict import *
from app.util.decimalencoder import DecimalEncoder
from app.data.profile import Profile
from app.data.source.profile_table import ProfileTable

def get_profile(event, context):
    try:
        sodaId = event['queryStringParameters']['sodaId']
        profileTable = ProfileTable(event)
        profile = profileTable.getProfileFromSodaId(sodaId)
        profile.noneToEmptystr()
        res = {
            "name" : profile.name,
            "urlData" : profile.urlData,
            "profile" : profile.profile,
            "twitter" : profile.twitter,
            "facebook" : profile.facebook,
            "instagram" : profile.instagram,
            "isAcceptMail" : profile.isAcceptMail,
            "universities" : profile.universities,
            "templates" : profile.templates
        }
        print(res)
        return Successed(res)
    
    except:
        import traceback
        traceback.print_exc()
        return Failured()