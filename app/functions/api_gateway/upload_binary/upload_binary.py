from app.data.source.s3 import S3
from app.util.return_dict import Successed, Failured

def upload_binary(event, context):
    try:
        binary = event['body']
        s3 = S3()
        url = s3.uploadBinary(binary)
        res = { "url" : url }

        return Successed(res)
    
    except:
        import  traceback
        return Failured(traceback.format_exc())