from app.data.source.profile_table import ProfileTable
from app.util.return_dict import Successed, Failured


def get_soda_id(event, context):
    try:
        param = event["queryStringParameters"]
        identityId = param['identityId']

        profileTable = ProfileTable(event)
        profile = profileTable.getFromIdentityId(identityId, 'sodaId')

        res = {
            "sodaId": profile.sodaId
        }
        return Successed(res)

    except Exception:
        import traceback
        return Failured(traceback.format_exc())
