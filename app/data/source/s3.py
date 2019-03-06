import json
import boto3
import os

class S3():
    def __init__(self):
        self.s3 = boto3.resource('s3')
    
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