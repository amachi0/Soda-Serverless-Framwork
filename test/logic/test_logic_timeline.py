import unittest
from app.data.event import Event
from app.logic.logic_timeline \
    import createResponseFromEvents, createStartNumAndSize


class TestLogicTimeline(unittest.TestCase):
    def setUp(self):
        self.mEvents = [
            Event(eventId=1, eventName='テスト１', updateTime=1553688554,
                  start=1554044400, location='BKC', urlData='test1',
                  university='立命館大学', countOfLike=1),
            Event(eventId=2, eventName='テスト２', updateTime=1553688554,
                  start=1554080400, end=1554088888, location='OIC',
                  urlData='test2', university='立命館大学', countOfLike=2),
            Event(eventId=3, eventName='テスト３', updateTime=1553688554,
                  start=1554088888, location='衣笠', urlData='test3',
                  university='立命館大学', countOfLike=5)
        ]

    def testPageZero(self):
        startNum, size = createStartNumAndSize(0)
        self.assertEqual(startNum, 0)
        self.assertEqual(size, 3)

    def testPageFive(self):
        startNum, size = createStartNumAndSize(5)
        self.assertEqual(startNum, 23)
        self.assertEqual(size, 5)

    def testCreateResponseFromEvents(self):
        favoriteEvents = [2]
        res = createResponseFromEvents(self.mEvents, 0, favoriteEvents)

        expected = {
            0: {
                'eventId': 1,
                'eventName': 'テスト１',
                'updateTime': 1553688554,
                'startTime': 1554044400,
                'endTime': None,
                'location': 'BKC',
                'urlData': 'test1',
                'university': '立命館大学',
                'countOfLike': 1,
                'isFavorite': False
            },
            1: {
                'eventId': 2,
                'eventName': 'テスト２',
                'updateTime': 1553688554,
                'startTime': 1554080400,
                'endTime': 1554088888,
                'location': 'OIC',
                'urlData': 'test2',
                'university': '立命館大学',
                'countOfLike': 2,
                'isFavorite': True
            },
            2: {
                'eventId': 3,
                'eventName': 'テスト３',
                'updateTime': 1553688554,
                'startTime': 1554088888,
                'endTime': None,
                'location': '衣笠',
                'urlData': 'test3',
                'university': '立命館大学',
                'countOfLike': 5,
                'isFavorite': False
            }
        }

        self.assertEqual(expected, res)
