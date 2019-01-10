import json
import boto3
import base64
import uuid
import os

s3 = boto3.resource('s3')
bucketName = os.environ["S3_IMAGE_BUCKET"]
arnS3 = os.environ['ARN_S3']

def upload_binary(event, context):
    try:
        print(event)
        bucket = s3.Bucket(bucketName)
        #param = json.loads(event['body'])
        imageBody = base64.b64decode(event['body'])
        imageId = str(uuid.uuid4())
        key = imageId + ".png"
        url = arnS3 + "/" + bucketName + "/" + key
        bucket.put_object(
            ACL = "public-read",
            Body = imageBody,
            Key = key,
            ContentType = "image/png"
            )
        
        res = {
            "url" : url
        }
        print(url)
        return{
            'statusCode' : 200,
            'headers' : {
                'content-type' : 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body' : json.dumps(res)
        }
    
    except:
        import traceback
        traceback.print_exc()
        res_error = {
            "result" : 0
        }
        return {
            'statusCode' : 500,
            'headers' : {
                'content-type' : 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body' : json.dumps(res_error)
        }