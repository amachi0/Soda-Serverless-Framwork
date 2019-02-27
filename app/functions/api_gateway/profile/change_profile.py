import json
import boto3
import os
from app.util.return_dict import *
from app.util.emptystr_to_none import emptystrToNoneInDict
from app.data.profile import Profile
from app.data.source.profile_table import ProfileTable

''' パラメーター
{  
  "identityId": "amachi2",
  "urlData": "test",
  "name": "test",
  "universities": [
    "立命館"
  ],
  "isAccepyMail" : true,
  "profile" : "よろしく",
  "twitter" : "hfnn",
  "facebook" : "hnkjfn",
  "instagram" : "nknfa"
}
'''

def change_profile(event, context):
    try:
        param = json.loads(event['body'])
        param = emptystrToNoneInDict(param)
        profile = Profile(**param)
        profileTable = ProfileTable()
        profileTable.changeProfile(profile)
        
        return Successed()
    
    except:
        import  traceback
        traceback.print_exc()
        return Failured()