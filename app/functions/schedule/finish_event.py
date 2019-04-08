import time
import decimal
from app.data.source.event_table import EventTable
from app.util.return_dict import Successed, Failured


def finish_event(event, context):
    try:
        now = time.time()
        nowDecimal = decimal.Decimal(str(now))

        eventTable = EventTable(event)
        listEventId = eventTable.getFinishedEventIdList(nowDecimal)

        if len(listEventId) == 0:
            return Successed({"result": 1})

        eventTable.updateStatuses(listEventId)
        return Successed({"result": 1})

    except Exception:
        import traceback
        return Failured(traceback.format_exc())
