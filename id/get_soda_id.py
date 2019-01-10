import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
profileTableName = os.environ['PROFILE_TABLE']

def get_soda_id(event, context):
	try:
		param = event["queryStringParameters"]
		identityId = param['identityId']

		table = dynamodb.Table(profileTableName)
		item = table.get_item(
		    Key = {
		        "identityId" : identityId
		    }
		)

		if("Item" in item):
			sodaId = item['Item']['sodaId']
			res = {
			    "sodaId" : sodaId
			}
			return {
			    'statusCode' : 200,
			    'headers' : {
			        'content-type' : 'application/json',
			        'Access-Control-Allow-Origin': '*'
			    },
			    'body' : json.dumps(res)
			}

		else:
			res_error = {
			    "result" : 0
			}
			return {
			    'statusCode' : 200,
			    'headers' : {
			        'content-type' : 'application/json',
			        'Access-Control-Allow-Origin': '*'
			    },
			    'body' : json.dumps(res_error)
			}

	except:
		import  traceback
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
