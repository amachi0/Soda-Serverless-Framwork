import os
import time
import decimal
from app.data.source.profile_table import ProfileTable
from app.data.source.event_table import EventTable
from app.data.sns import Sns
from app.util.return_dict import Successed, Failured

TOPIC_NAME = os.environ['SNS_SEND_WEEK_MAIL']
SECOND_OF_ONE_WEEK = 604800


def prepare_week_mail(event, context):
    try:
        now = time.time()
        nowDecimal = decimal.Decimal(str(now))
        # 一週間の秒すう
        timeAfterWeek = nowDecimal + SECOND_OF_ONE_WEEK

        eventTable = EventTable(event)
        events = eventTable.queryForWeekMail(timeAfterWeek)
        if len(events) == 0:
            return Successed({'result': 1})
        message = {'events': events}

        profileTable = ProfileTable(event)
        profiles = profileTable.scanForWeekMail()

        dividedProfiles = [profiles[idx:idx + 10]
                           for idx in range(0, len(profiles), 10)]

        sns = Sns(TOPIC_NAME)
        for partOfProfile in dividedProfiles:
            message['profiles'] = partOfProfile
            sns.publishFromDictiorary(message)

        res = {'result': 1}
        return Successed(res)

    except Exception:
        import traceback
        return Failured(traceback.format_exc())
