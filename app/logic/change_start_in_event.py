from app.data.event import Event
from datetime import datetime, timezone, timedelta

dayOfTheWeek = ['(月)', '(火)', '(水)', '(木)', '(金)', '(土)', '(日)']


def changeStartInEvent(event=Event):
    unixTime = event.start
    print(unixTime)
    dateTime = datetime.fromtimestamp(unixTime)
    month = dateTime.month
    date = dateTime.day

    weekday = dateTime.weekday()
    strWeekDay = dayOfTheWeek[weekday]

    date = str(month) + '/' + str(date) + strWeekDay
    print(date)
    event.start = date


def getStrFromStartAndEndInEvent(event=Event):
    JST = timezone(timedelta(hours=+9), 'JST')
    startDateTime = datetime.fromtimestamp(event.start, JST)

    startStrHour = str(startDateTime.hour)
    startStrMinute = str(startDateTime.minute)
    if len(startStrMinute) < 2:
        startStrMinute = '0' + startStrMinute

    timeStr = startStrHour + ':' + startStrMinute + '〜'

    if event.end:
        endDateTime = datetime.fromtimestamp(event.end, JST)

        endStrHour = str(endDateTime.hour)
        endStrMinute = str(endDateTime.minute)
        if len(endStrMinute) < 2:
            endStrMinute = '0' + endStrMinute

        timeStr += endStrHour + ":" + endStrMinute

    return timeStr
