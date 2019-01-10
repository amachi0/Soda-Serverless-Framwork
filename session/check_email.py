import json
import boto3
import os
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
profileTableName = os.environ['PROFILE_TABLE']
checkEmailIndex = os.environ['PROFILE_CHECK_Email_INDEX']

def check_email(event, context):
	try:
		email = event['queryStringParameters']['email']

		table = dynamodb.Table(profileTableName)
		items = table.query(
			IndexName = checkEmailIndex,
			KeyConditionExpression = Key('email').eq(email)
		)
		
		if (items['Count'] == 0):
			res = {
				"result" : True
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
			res = {
				"result" : False
			}
			return {
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