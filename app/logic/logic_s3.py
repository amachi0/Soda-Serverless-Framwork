import os
import uuid


def setBucketAndFileName(file):
    if file == 'faqs':
        bucket = os.environ['S3_JSON_BUCKET']
        fileName = os.environ['FAQS_JSON']
    elif file == 'terms':
        bucket = os.environ['S3_JSON_BUCKET']
        fileName = os.environ['TERMS_JSON']
    elif file == 'university':
        bucket = os.environ['S3_JSON_BUCKET']
        fileName = os.environ['UNIVERSITY_JSON']

    return bucket, fileName


def makeImageUrl(arnS3, imageBucketName):
    imageId = str(uuid.uuid4())
    key = imageId + ".png"
    url = arnS3 + "/" + imageBucketName + "/" + key

    return key, url
