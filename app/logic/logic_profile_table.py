from app.data.profile import Profile


def getListKeysForBatchGet(self, listIdentityId):
    listKeys = []
    for identityId in listIdentityId:
        dic = {
            "identityId": {
                "S": identityId
            }
        }
        listKeys.append(dic)

    return listKeys


def getProfilesFromBatchGetResponse(response, tableName):
    profiles = []
    for profile in response['Responses'][tableName]:
        mProfile = Profile()
        mProfile.email = profile['email']['S']
        mProfile.isAcceptMail = profile['isAcceptMail']['BOOL']
        profiles.append(mProfile)

    return profiles


def getProfilesFromResponse(response):
    profiles = []
    for profile in response:
        mProfile = Profile(**profile)
        profiles.append(mProfile)

    return profiles


def hasNoItemInResponse(response):
    if (response['Count'] == 0):
        return True
    else:
        return False
