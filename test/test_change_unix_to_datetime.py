import unittest
from app.data.event import Event
from app.util.change_unix_to_datetime \
    import changeStartInEvent, getStrFromStartAndEndInEvent


class TestChangeStartInEvent(unittest.TestCase):
    def setUp(self):
        self.mEvent = Event(start=1554044400, end=1554080400)

    def testChangeStartInEvent(self):
        expected = '4/1(月)'
        strDate = changeStartInEvent(self.mEvent)

        self.assertEqual(strDate, expected)

    def testGetStrFromStartAndEndInEvent(self):
        expected = '0:00〜10:00'
        timeStr = getStrFromStartAndEndInEvent(self.mEvent)

        self.assertEqual(timeStr, expected)
