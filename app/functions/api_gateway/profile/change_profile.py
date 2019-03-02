import json
import boto3
import os
from app.util.return_dict import *
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
    profile = Profile(**param)
    profile.emptystrToNone()
    profileTable = ProfileTable(event)
    profileTable.changeProfile(profile)
    
    returnBody = {
      "result" : 1
    }
    return Successed(returnBody)
  
  except:
    import  traceback
    traceback.print_exc()
    return Failured()