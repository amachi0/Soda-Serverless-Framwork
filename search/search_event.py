import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')

def search_event(event, context):
    try:
        keyword = event['queryStringParameters']['keyword']
        page = int(event['queryStringParameters']['page'])
        
        word = keyword.split()
        queryKeyword = ""
        for w in word:
            queryKeyword = queryKeyword + " '" + w + "'"
               
        querySearch = "(and" + queryKeyword + ")"
        
        #pageが０なら３件取得して、それ以外なら５件取得
        if(page == 0):
            startCostom = 0
            sizeCostom = 3
        
        else:
            startCostom = 3 + (page -1) * 5
            sizeCostom = 5
        
        results = cloudSearch.search(
            query = querySearch,
            size = sizeCostom,
            start = startCostom,
            sort = "start asc,updatetime desc",
            queryParser = "structured"
        )
        res = {}
        if(page == 0):
            i = 0
        else:
            i = (page-1) * 5 + 3
        for hit in results["hits"]["hit"]:
            res[str(i)] = {}
            eventId = int(hit['fields']['eventid'][0])
            title = hit['fields']['eventname'][0]
            updateTime = int(hit['fields']['updatetime'][0])
            start = int(hit['fields']['start'][0])
            if("end" in hit['fields']):
                end = int(hit['fields']['end'][0])
            else:
                end = None
            location = hit['fields']['location'][0]
            image = hit['fields']['urldata'][0]
            university = hit['fields']['university'][0]
            countOfLike = int(hit['fields']['countoflike'][0])
            
            res[str(i)]["eventId"] = int(eventId)
            res[str(i)]["title"] = title
            res[str(i)]["updateTime"] = int(updateTime)
            res[str(i)]["startTime"] = start
            res[str(i)]["endTime"] = end
            res[str(i)]["location"] = location
            res[str(i)]["image"] = image
            res[str(i)]["university"] = university
            res[str(i)]["countOfLike"] = int(countOfLike)
            i += 1
        
        return {
            "statusCode": 200,
            'headers' : {
                'content-type' : 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps(res)
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