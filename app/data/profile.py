class Profile:
    def __init__(self, identityId=None, sodaId=None, email=None, universities=[], name=None, 
                    urlData=None, profile=None, twitter=None, facebook=None, instagram=None, 
                    favoriteEvent=[], myEvent=[], templates=[], isAcceptMail=True):
        
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

        self.paramListOfStr = [self.identityId, self.sodaId, self.email, self.name, self.urlData, 
                                self.profile, self.twitter, self.facebook, self.instagram]

    def hasName(self):
        if self.name:
            return True
        else:
            return False
    
    def createNameFromEmail(self):
        emailSplit = self.email.rsplit("@")
        self.name = emailSplit[0]
    
    def emptystrToNone(self):
        i = 0
        for param in self.paramListOfStr:
            if(param == ""): 
                self.paramListOfStr[i] = None
            i += 1
        self.identityId = self.paramListOfStr[0]
        self.sodaId = self.paramListOfStr[1]
        self.email = self.paramListOfStr[2]
        self.name = self.paramListOfStr[3]
        self.urlData = self.paramListOfStr[4]
        self.profile = self.paramListOfStr[5]
        self.twitter = self.paramListOfStr[6]
        self.facebook = self.paramListOfStr[7]
        self.instagram = self.paramListOfStr[8]

    def noneToEmptystr(self):
        i = 0
        for param in self.paramListOfStr:
            if param is None:
                self.paramListOfStr[i] = ""
            i += 1
        self.identityId = self.paramListOfStr[0]
        self.sodaId = self.paramListOfStr[1]
        self.email = self.paramListOfStr[2]
        self.name = self.paramListOfStr[3]
        self.urlData = self.paramListOfStr[4]
        self.profile = self.paramListOfStr[5]
        self.twitter = self.paramListOfStr[6]
        self.facebook = self.paramListOfStr[7]
        self.instagram = self.paramListOfStr[8]
