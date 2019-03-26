import time
import decimal
from botocore.exceptions import ClientError
from app.data.twitter import Twitter
from app.data.source.event_table import EventTable
from app.util.return_dict import Successed, Failured

SECOND_OF_ONE_DAY = 86400


def tweet_event_info(event, context):
    try:
        now = time.time()
        nowDecimal = decimal.Decimal(str(now))
        timeAfterDay = nowDecimal + SECOND_OF_ONE_DAY

        eventTable = EventTable(event)
        events = eventTable.queryForTweet(timeAfterDay)

        twitter = Twitter()
        twitter.tweetEventInfoFromEvents(events)

        res = {'result': 1}
        return Successed(res)

    except ClientError:
        import traceback
        return Failured(traceback.format_exc())
