def createResponseFromEvents(events, startNum, favoriteEvents):
    res = {}
    for event in events:
        if favoriteEvents == "ALL":
            isFavorite = True
        elif(event.eventId in favoriteEvents):
            isFavorite = True
        else:
            isFavorite = False

        res[startNum] = {
            'eventId': event.eventId,
            'eventName': event.eventName,
            'updateTime': event.updateTime,
            'startTime': event.start,
            'endTime': event.end,
            'location': event.location,
            'urlData': event.urlData,
            'university': event.university,
            'countOfLike': event.countOfLike,
            'isFavorite': isFavorite
        }
        startNum += 1

    return res


def createStartNumAndSize(page):
    if page == 0:
        startNum = 0
        size = 3
    else:
        startNum = 3 + (page - 1) * 5
        size = 5

    return startNum, size
