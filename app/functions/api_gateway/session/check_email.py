from botocore.exceptions import ClientError
from app.data.source.profile_table import ProfileTable
from app.util.return_dict import Successed, Failured


def check_email(event, context):
    try:
        email = event['queryStringParameters']['email']

        profileTable = ProfileTable(event)
        isValidEmail = profileTable.isValidEmail(email)

        if isValidEmail:
            res = {"result": True}
        else:
            res = {"result": False}

        return Successed(res)

    except ClientError:
        import traceback
        return Failured(traceback.format_exc())
