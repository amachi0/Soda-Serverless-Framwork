class Event():
    def __init__(self, identityId, eventName, urlData, university, price, location, start, 
                    qualification, detail, contact, countOfLike=0, end=None, eventId=0, 
                    status="0_false", isPrivate=False ,updateTime="",  favorite=[]):
        self.contact = contact
        self.countOfLike = countOfLike
        self.detail = detail
        self.end = end
        self.eventId = eventId
        self.eventName = eventName
        self.favorite = favorite
        self.identityId = identityId
        self.location = location
        self.price = price
        self.qualification = qualification
        self.start = start
        self.status = status
        self.isPrivate = isPrivate
        self.university = university
        self.updateTime = updateTime
        self.urlData = urlData
    
    def createStatusFromIsPrivate(self):
        if self.isPrivate == True:
            self.status = "0_true"
        else:
            self.status = "0_false"