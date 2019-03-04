import json
import boto3
import os
from app.util.return_dict import *
from app.util.change_none_and_emptystr import NoneToEmptystrInDict
from app.data.profile import Profile
from app.data.source.profile_table import ProfileTable

def get_profile(event, context):
    try:
        sodaId = event['queryStringParameters']['sodaId']
        profileTable = ProfileTable(event)
        profile = profileTable.getProfileFromSodaId(sodaId)
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

        NoneToEmptystrInDict(res)

        return Successed(res)
    
    except:
        import traceback
        traceback.print_exc()
        return Failured()