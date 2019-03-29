import unittest
from app.data.event import Event


class TestEvent(unittest.TestCase):
    def testCreateStatusFromIsPrivate(self):
        mEvent = Event(isPrivate=False)
        mEvent.createStatusFromIsPrivate()

        self.assertEqual(mEvent.status, '0_false')

        mEvent.isPrivate = True
        mEvent.createStatusFromIsPrivate()

        self.assertEqual(mEvent.status, '0_true')

    def testCreateIsPrivateFromStatus(self):
        mEvent = Event(status='0_false')
        mEvent.createIsPrivateFromStatus()

        self.assertEqual(mEvent.isPrivate, False)

        mEvent.status = '0_true'
        mEvent.createIsPrivateFromStatus()

        self.assertEqual(mEvent.isPrivate, True)

    def testHasfavorite(self):
        mEvent = Event()
        hasFavorite = mEvent.hasfavorite()

        self.assertEqual(hasFavorite, False)

        mEvent.favorite = set([1, 2])
        hasFavorite = mEvent.hasfavorite()

        self.assertEqual(hasFavorite, True)
