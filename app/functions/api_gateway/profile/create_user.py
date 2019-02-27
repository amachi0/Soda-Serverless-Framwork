import json
import boto3
import os
from app.data.profile import Profile
from app.data.source.profile_table import ProfileTable
from app.util.emptystr_to_none import emptystrToNoneInDict

def create_user(event, context):
    try:
        param = json.loads(event['body'])
        emptystrToNoneInDict(param)
        profile = Profile(**param)
        
        if not profile.hasName():
            profile.createNameFromEmail()
        
        profileTable = ProfileTable()
        profileTable.insertProfile(profile)

        return {
            'statusCode' : 200,
            'headers' : {
                'content-type' : 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body' : json.dumps({"result" : 1})
        }
        
    except:
        import  traceback
        traceback.print_exc()
        return {
            'statusCode' : 500,
            'headers' : {
                'content-type' : 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body' : json.dumps({"result" : 0})
        }