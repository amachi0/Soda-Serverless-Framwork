import json
import boto3
import os
from app.util.return_dict import *
from app.util.emptystr_to_none import emptystrToNoneInDict
from app.data.profile import Profile
from app.data.source.profile_table import ProfileTable

''' パラメーター
{
  "body": {
    "identityId": "amachi1",
    "sodaId": "amachi1",
    "email": "shunsuke-1103@ezweb.ne.jp",
    "urlData": "test",
    "name": "test",
    "universities": [
      "立命館"
    ]
  }
}
'''

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