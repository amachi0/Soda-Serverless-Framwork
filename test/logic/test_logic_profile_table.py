import unittest
from app.data.profile import Profile
from app.logic.logic_profile_table \
    import getListKeysForBatchGetProfile, getProfilesFromBatchGetResponse, \
    getProfilesFromResponse, hasNoItemInResponse


class TestLogicProfileTable(unittest.TestCase):
    def testGetListKeysForBatchGet(self):
        listIdentityId = ['hoge', 'hage']
        listKeys = getListKeysForBatchGetProfile(listIdentityId)

        expected = [
            {
                "identityId": {
                    'S': 'hoge'
                }
            },
            {
                'identityId': {
                    'S': 'hage'
                }
            }
        ]

        self.assertEqual(listKeys, expected)

    def testGetProfilesFromBatchGetResponse(self):
        response = {
            'Responses': {
                'dev-profile': [
                    {
                        'email': {'S': 'test@test.com'},
                        'isAcceptMail': {'BOOL': True}
                    }
                ]
            }
        }

        profiles = getProfilesFromBatchGetResponse(response, 'dev-profile')
        profile = profiles[0]

        self.assertIsInstance(profile, Profile)
        self.assertEqual(profile.email, 'test@test.com')
        self.assertEqual(profile.isAcceptMail, True)

    def testGetProfilesFromResponse(self):
        res = [
            {
                'identityId': 'amachi1',
                'email': 'test@test.com'
            },
            {
                'identityId': 'amachi2',
                'email': 'testtest@testtest.com'
            }
        ]

        profiles = getProfilesFromResponse(res)
        profileTop = profiles[0]
        profileNext = profiles[1]

        self.assertIsInstance(profileTop, Profile)
        self.assertEqual(profileTop.identityId, 'amachi1')
        self.assertEqual(profileTop.email, 'test@test.com')
        self.assertEqual(profileNext.identityId, 'amachi2')
        self.assertEqual(profileNext.email, 'testtest@testtest.com')

    def testHasNoItemInResponse(self):
        resCount = {
            'Count': 3
        }

        resZero = {
            'Count': 0
        }

        resultExsist = hasNoItemInResponse(resCount)
        resultNoExsist = hasNoItemInResponse(resZero)

        self.assertFalse(resultExsist)
        self.assertTrue(resultNoExsist)
