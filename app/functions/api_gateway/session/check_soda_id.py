from app.data.source.profile_table import ProfileTable
from app.util.return_dict import Successed, Failured

def check_soda_id(event, context):
	try:
		sodaId = event['queryStringParameters']['sodaId']

		profileTable = ProfileTable(event)
		isValidSodaId = profileTable.isValidSodaId(sodaId)

		if isValidSodaId:
			res = { "result" : True }
		else:
			res = { "result" : False }

		return Successed(res)

	except:
		import  traceback
		return Failured(traceback.format_exc())