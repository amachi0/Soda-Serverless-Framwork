import tweepy
import os
from app.util.change_unix_to_datetime import getStrFromStartAndEndInEvent


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
            url = "https://sodaevent.com/event/" + str(event.eventId)
            eventName = event.eventName
            location = event.location
            timeStr = getStrFromStartAndEndInEvent(event)

            self.api.update_status(
                status="本日のイベント | " + eventName + "  場所："
                + location + "  時間：" + timeStr + " " + url
            )
