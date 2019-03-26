import tweepy
import os
from app.logic.change_start_in_event import getStrFromStartAndEndInEvent


class Twitter():
    def __init__(self):
        CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
        CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
        ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
        ACCESS_SECRET = os.environ['ACCESS_SECRET']
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        self.api = tweepy.API(auth)

    def tweetEventInfoFromEvents(self, events):
        for event in events:
            # url = "https://sodaevent.com/event/" + str(event.eventId)
            url = "https://sodaevent.com/event/28"
            # eventName = event.eventName
            eventName = "🌸【watnow】新歓お花見イベント"
            # location = event.location
            location = "梅小路公園(集合は京都駅)"
            timeStr = getStrFromStartAndEndInEvent(event)

            self.api.update_status(
                status="本日のイベント | " + eventName + "  場所："
                + location + "  時間：" + timeStr + " " + url
            )
