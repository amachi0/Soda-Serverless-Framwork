import json
import boto3
import os

bucket = os.environ['S3_JSON_BUCKET']
file = os.environ['UNIVERSITY_JSON']

def university(event, context):
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket, file)
    content = obj.get()['Body'].read().decode('utf-8')
    content_json = json.loads(content)
    return {
        'statusCode' : 200,
        'headers' : {
            'content-type' : 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body' : json.dumps(content_json)
    }