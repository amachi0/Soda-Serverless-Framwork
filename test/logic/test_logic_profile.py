import unittest
from app.data.profile import Profile


class TestProfile(unittest.TestCase):
    def setUp(self):
        self.mProfile = Profile(email='test@test.com')

    def testHasName(self):
        hasName = self.mProfile.hasName()
        self.assertEqual(hasName, False)

        self.mProfile.name = "テスト"
        hasName = self.mProfile.hasName()
        self.assertEqual(hasName, True)

    def testHasUrlData(self):
        hasUrl = self.mProfile.hasUrlData()
        self.assertEqual(hasUrl, False)

        self.mProfile.urlData = 'test'
        hasUrl = self.mProfile.hasUrlData()
        self.assertEqual(hasUrl, True)

    def testCreateNameFromEmail(self):
        self.mProfile.createNameFromEmail()

        self.assertEqual(self.mProfile.name, 'test')
