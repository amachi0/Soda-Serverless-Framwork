import json
from app.util.return_dict import Successed, Failured
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
      "立命館大学"
    ]
  }
}
'''

def create_user(event, context):
  try:
    param = json.loads(event['body'])
    profile = Profile(**param)

    if not profile.hasName():
      profile.createNameFromEmail()
    
    if not profile.hasUrlData():
      profile.urlData = None
    
    profileTable = ProfileTable(event)
    profileTable.insert(profile)

    returnBody = {
      "result" : 1
    }
    return Successed(returnBody)
        
  except:
    import  traceback
    traceback.print_exc()
    return Failured