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
