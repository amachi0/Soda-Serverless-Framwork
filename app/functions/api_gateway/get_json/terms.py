from app.data.source.s3 import S3
from app.util.return_dict import Successed


def terms(event, context):
    s3 = S3()
    res = s3.getJson('terms')

    return Successed(res)
