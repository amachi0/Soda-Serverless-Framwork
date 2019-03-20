class Profile:
    def __init__(self, identityId=None, sodaId=None, email=None,
                 universities=[], name=None, urlData=None, profile=None,
                 twitter=None, facebook=None, instagram=None,
                 favoriteEvent=set(), myEvent=set(), templates=[],
                 isAcceptMail=True):

        self.identityId = identityId
        self.sodaId = sodaId
        self.email = email
        self.universities = universities
        self.name = name
        self.urlData = urlData
        self.profile = profile
        self.twitter = twitter
        self.facebook = facebook
        self.instagram = instagram
        self.favoriteEvent = favoriteEvent
        self.myEvent = myEvent
        self.templates = templates
        self.isAcceptMail = isAcceptMail

    def hasName(self):
        if self.name:
            return True
        else:
            return False

    def hasUrlData(self):
        if self.urlData:
            return True
        else:
            return False

    def hasMyEvent(self):
        if self.name:
            return True
        else:
            return False

    def createNameFromEmail(self):
        emailSplit = self.email.rsplit("@")
        self.name = emailSplit[0]
