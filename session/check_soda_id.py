import json
import boto3
import os
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
profileTableName = os.environ['PROFILE_TABLE']
checkSodaIdIndex = os.environ['PROFILE_CHECK_SODA_ID_INDEX']

def check_soda_id(event, context):
	try:
		sodaId = event['queryStringParameters']['sodaId']

		table = dynamodb.Table(profileTableName)
		items = table.query(
			IndexName = checkSodaIdIndex,
			KeyConditionExpression = Key('sodaId').eq(sodaId)
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

