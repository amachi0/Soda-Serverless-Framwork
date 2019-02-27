import json
import boto3
import os
from app.util.return_dict import *
from app.util.emptystr_to_none import emptystrToNoneInDict
from app.data.profile import Profile
from app.data.source.profile_table import ProfileTable


def create_user(event, context):
    try:
        param = json.loads(event['body'])
        param = emptystrToNoneInDict(param)
        profile = Profile(**param)
        
        if not profile.hasName():
            profile.createNameFromEmail()
        
        profileTable = ProfileTable()
        profileTable.insertProfile(profile)

        return Successed
        
    except:
        import  traceback
        traceback.print_exc()
        return Failured