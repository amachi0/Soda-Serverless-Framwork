from app.data.source.profile_table import ProfileTable
from app.data.source.event_table import EventTable
from app.util.return_dict import Successed, Failured
from app.logic.logic_timeline \
    import createStartNumAndSize, createResponseFromEvents


def created_event(event, context):
    try:
        sodaId = event["queryStringParameters"]["sodaId"]
        page = int(event['queryStringParameters']['page'])

        profileTable = ProfileTable(event)
        profile = profileTable.getFromSodaId(sodaId)

        if len(profile.myEvent) <= 0:
            return Successed({})

        myEvents = list(profile.myEvent)
        intMyEvent = [int(x) for x in myEvents]
        favoriteEvents = list(profile.favoriteEvent)

        # 新しい順番から表示させたいので配列を降順にソートする
        intMyEvent.reverse()

        startNum, size = createStartNumAndSize(page)

        # 配列長以上の要素を要求されたときはここで処理を終わる
        if(len(intMyEvent) <= startNum):
            return Successed({})

        # 配列の１ページ分を切り取る
        myEventsIdInPage = intMyEvent[startNum:startNum + size]

        eventTable = EventTable(event)
        events = eventTable.batchGetFromListEventId(myEventsIdInPage)

        events = sorted(events)

        res = createResponseFromEvents(events, startNum, favoriteEvents)
        return Successed(res)

    except Exception:
        import traceback
        return Failured(traceback.format_exc())
