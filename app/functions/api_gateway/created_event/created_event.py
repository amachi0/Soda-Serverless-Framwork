from app.data.source.profile_table import ProfileTable
from app.data.source.event_table import EventTable
from app.util.return_dict import Successed, Failured
from app.logic.logic_created_event import createResponseFromEvents

def created_event(event, context):
    try:
        sodaId = event["queryStringParameters"]["sodaId"]
        page = int(event['queryStringParameters']['page'])

        profileTable = ProfileTable(event)
        profile = profileTable.getFromSodaId(sodaId)

        if len(profile.myEvent) <= 0:
            return Successed({})

        myEvents = list(profile.myEvent)
        favoriteEvents = list(profile.favoriteEvent)

        #新しい順番から表示させたいので配列を降順にソートする
        myEvents.reverse()

        if(page == 0):
            startNum = 0
            size = 3
        else:
            startNum = 3 + (page -1) * 5
            size = 5
        
        # 配列長以上の要素を要求されたときはここで処理を終わる
        if(len(myEvents) <= startNum):
            return Successed({})
        
        # 配列の１ページ分を切り取る
        myEventsIdInPage = myEvents[startNum:startNum + size]

        eventTable = EventTable(event)
        events = eventTable.batchGetFromListEventId(myEventsIdInPage)

        events = sorted(events)

        res = createResponseFromEvents(events, startNum, favoriteEvents)
        return Successed(res)

    except:
        import  traceback
        traceback.print_exc()
        return Failured()