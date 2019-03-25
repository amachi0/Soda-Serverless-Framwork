from app.data.event import Event
import datetime

dayOfTheWeek = ["(月)", "(火)", "(水)", "(木)", "(金)", "(土)", "(日)"]


def changeStartInEvent(event=Event):
    unixTime = event.start
    print(unixTime)
    dateTime = datetime.date.fromtimestamp(unixTime)
    month = dateTime.month
    date = dateTime.day

    weekday = dateTime.weekday()
    strWeekDay = dayOfTheWeek[weekday]

    date = str(month) + '/' + str(date) + strWeekDay
    print(date)
    event.start = date
