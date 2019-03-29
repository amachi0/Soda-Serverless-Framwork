import json
import boto3
import os
import base64
from app.logic.logic_s3 \
    import setBucketAndFileName, makeImageUrl


class S3():
    def __init__(self):
        self.s3 = boto3.resource('s3')
        self.imageBucketName = os.environ["S3_IMAGE_BUCKET"]
        self.arnS3 = os.environ['ARN_S3']

    def getJson(self, file):
        bucket, fileName = setBucketAndFileName(file)
        obj = self.s3.Object(bucket, fileName)
        content = obj.get()['Body'].read().decode('utf-8')
        contentJson = json.loads(content)
        return contentJson

    def uploadBinary(self, binary):
        imageBody = base64.b64decode(binary)
        imageBucket = self.s3.Bucket(self.imageBucketName)

        key, url = makeImageUrl(self.arnS3, self.imageBucketName)
        imageBucket.put_object(
            ACL="public-read",
            Body=imageBody,
            Key=key,
            ContentType="image/png"
        )
        return url
