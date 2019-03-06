import json
import boto3
import os
import base64
import uuid

class S3():
    def __init__(self):
        self.s3 = boto3.resource('s3')
        self.imageBucketName = os.environ["S3_IMAGE_BUCKET"]
        self.arnS3 = os.environ['ARN_S3']
    
    def getJson(self, file):
        if file == 'faqs':
            bucket = os.environ['S3_JSON_BUCKET']
            fileName = os.environ['FAQS_JSON']
        elif file == 'terms':
            bucket = os.environ['S3_JSON_BUCKET']
            fileName = os.environ['TERMS_JSON']
        elif file == 'university':
            bucket = os.environ['S3_JSON_BUCKET']
            fileName = os.environ['UNIVERSITY_JSON']
        
        obj = self.s3.Object(bucket, fileName)
        content = obj.get()['Body'].read().decode('utf-8')
        contentJson = json.loads(content)
        return contentJson
    
    def uploadBinary(self, binary):
        imageBody = base64.b64decode(binary)
        imageBucket = self.s3.Bucket(self.imageBucketName)
        imageId = str(uuid.uuid4())
        key = imageId + ".png"
        url = self.arnS3 + "/" + self.imageBucketName + "/" + key
        imageBucket.put_object(
            ACL = "public-read",
            Body = imageBody,
            Key = key,
            ContentType = "image/png"
            )
        return url