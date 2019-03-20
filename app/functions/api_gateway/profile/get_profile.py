from botocore.exceptions import ClientError
from app.util.return_dict import Successed, Failured
from app.util.change_none_and_emptystr import NoneToEmptystrInDict
from app.data.source.profile_table import ProfileTable


def get_profile(event, context):
    try:
        sodaId = event['queryStringParameters']['sodaId']
        profileTable = ProfileTable(event)
        profile = profileTable.getFromSodaId(sodaId)
        res = {
            "name": profile.name,
            "urlData": profile.urlData,
            "profile": profile.profile,
            "twitter": profile.twitter,
            "facebook": profile.facebook,
            "instagram": profile.instagram,
            "isAcceptMail": profile.isAcceptMail,
            "universities": profile.universities
        }
        print(res)

        NoneToEmptystrInDict(res)

        return Successed(res)

    except ClientError:
        import traceback
        return Failured(traceback.format_exc())
