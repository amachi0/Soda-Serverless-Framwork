class Event():
    def __init__(self, identityId=None, eventName=None, urlData=None,
                 university=None, price=None, location=None, start=None,
                 qualification=None, detail=None, contact=None, countOfLike=0,
                 end=None, eventId=0, status="", isPrivate=False, updateTime=0,
                 favorite=set(), sponsor=None, entry=None):
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
        self.sponsor = sponsor
        self.entry = entry

    def __lt__(self, other):
        return self.eventId > other.eventId

    def createStatusFromIsPrivate(self):
        if self.isPrivate:
            self.status = "0_true"
        else:
            self.status = "0_false"

    def createIsPrivateFromStatus(self):
        if(self.status == "0_false"):
            self.isPrivate = False
        else:
            self.isPrivate = True

    def hasfavorite(self):
        if len(self.favorite) != 0:
            return True
        else:
            return False
