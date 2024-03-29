import json
from app.util.return_dict import Successed, Failured
from app.util.change_none_and_emptystr import emptystrToNoneInDict
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
  "isAcceptMail" : true,
  "profile" : "よろしく",
  "twitter" : "hfnn",
  "facebook" : "hnkjfn",
  "instagram" : "nknfa"
}
'''


def change_profile(event, context):
    try:
        param = json.loads(event['body'])
        emptystrToNoneInDict(param)
        profile = Profile(**param)

        profileTable = ProfileTable(event)
        profileTable.change(profile)

        returnBody = {
            "result": 1
        }
        return Successed(returnBody)

    except Exception:
        import traceback
        return Failured(traceback.format_exc())
