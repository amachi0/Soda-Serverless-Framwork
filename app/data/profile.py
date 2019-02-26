class Profile:
    def __init__(self):
        self.identityId = ""
        self.sodaId = ""
        self.email = ""
        self.universities = []
        self.name = ""
        self.urlData = ""
        self.isAcceptMail = True
        self.profile = ""
        self.twitter = ""
        self.facebook = ""
        self.instagram = ""
        self.favoriteEvent = []
        self.myEvent = []
        self.templates = []
        
    def hasName(self):
        if not self.name:
            return False
        else:
            return True