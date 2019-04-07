from app.data.source.profile_table import ProfileTable
from app.data.source.event_table import EventTable
from app.util.return_dict import Successed, Failured
from app.logic.logic_timeline \
    import createStartNumAndSize, createResponseFromEvents


def timeline_favorite(event, context):
    try:
        sodaId = event["queryStringParameters"]["sodaId"]
        page = int(event['queryStringParameters']['page'])

        if(sodaId == "null"):
            return Successed({})

        profileTable = ProfileTable(event)
        profile = profileTable.getFromSodaId(sodaId)

        if(len(profile.favoriteEvent) == 0):
            Successed({})

        listEventId = list(profile.favoriteEvent)
        # 新しい順番から表示させたいので配列を逆にする
        listEventId.reverse()

        startNum, size = createStartNumAndSize(page)

        # 配列長以上の要素を要求されたときはここで処理を終わる
        # 配列の１ページ分を切り取る
        if(len(listEventId) <= startNum):
            return Successed({})

        listEventIdInPage = listEventId[startNum:startNum + size]

        eventTable = EventTable(event)
        events = eventTable.batchGetFromListEventId(listEventIdInPage)

        events = sorted(events)

        res = createResponseFromEvents(events, startNum, "ALL")
        return Successed(res)

    except Exception:
        import traceback
        return Failured(traceback.format_exc())
