import unittest
from app.data.event import Event
from decimal import Decimal
from app.logic.logic_event_table \
    import getEventIdListFromTwoResponse, getListKeysForBatchGet, \
    getEventsFromBatchGetResponse, getEventsForWeekMailFromResponse, \
    getEventsFromResponse

res = {'Items': [
    {
        'eventName': 'イベント名',
        'eventId': Decimal('14'),
        'university': '立命館大学',
        'location': 'BKC アクロスウィング',
        'updateTime': Decimal('1552805737'),
        'status': '0_true',
        'countOfLike': Decimal('0'),
        'end': None,
        'urlData': 'test3.png',
        'start': Decimal('1553675195')
    },
    {
        'eventName': 'イベント名',
        'eventId': Decimal('15'),
        'university': '立命館大学',
        'location': 'BKC アクロスウィング',
        'updateTime': Decimal('1552805737'),
        'status': '0_true',
        'countOfLike': Decimal('2'),
        'end': None,
        'urlData': 'test3.png',
        'start': Decimal('1553675195')
    }]
}


class TestLogicEventTable(unittest.TestCase):
    def testGetEventIdListFromTwoResponse(self):
        itemsNotPrivate = {'Items': [
            {
                'eventName': '2',
                'eventId': Decimal('16'),
                'university': '立命館大学',
                'location': 'test',
                'updateTime': Decimal('1553483264'),
                'status': '0_false',
                'countOfLike': Decimal('1'),
                'end': None,
                'urlData': 'test1.png',
                'start': Decimal('1553482800')
            },
            {
                'eventName': '１',
                'eventId': Decimal('18'),
                'university': '立命館大学',
                'location': 'tes',
                'updateTime': Decimal('1553505729'),
                'status': '0_false',
                'countOfLike': Decimal('0'),
                'end': None,
                'urlData': 'test2.png',
                'start': Decimal('1553558400')
            }],
            'Count': 3
        }

        itemsPrivate = {'Items': [
            {
                'eventName': 'イベント名',
                'eventId': Decimal('14'),
                'university': '立命館大学',
                'location': 'BKC アクロスウィング',
                'updateTime': Decimal('1552805737'),
                'status': '0_true',
                'countOfLike': Decimal('0'),
                'end': None,
                'urlData': 'test3.png',
                'start': Decimal('1553675195')
            }],
            'Count': 1
        }

        eventIdList = getEventIdListFromTwoResponse(
            itemsNotPrivate, itemsPrivate)

        self.assertEqual(eventIdList, [
            Decimal('16'), Decimal('18'), Decimal('14')])

    def testGetListKeysForBatchGet(self):
        listEventId = [1, 2, 3]
        listKeys = getListKeysForBatchGet(listEventId)

        expected = [
            {
                "eventId": {
                    "N": str(1)
                }
            },
            {
                "eventId": {
                    "N": str(2)
                }
            },
            {
                "eventId": {
                    "N": str(3)
                }
            }
        ]

        self.assertEqual(listKeys, expected)

    def testGetListKeysForBatchGetBlank(self):
        listEventId = []
        listKeys = getListKeysForBatchGet(listEventId)

        expected = []

        self.assertEqual(listKeys, expected)

    def testGetEventsFromBatchGetResponse(self):
        response = {
            'Responses': {
                'dev-event': [
                    {
                        'eventId': {'N': '11'},
                        'eventName': {'S': 'イベント名'},
                        'location': {'S': 'BKC アクロスウィング'},
                        'university': {'S': '立命館大学'},
                        'updateTime': {'N': '1552629886'},
                        'countOfLike': {'N': '0'},
                        'end': {'NULL': True},
                        'urlData': {'S': 'https://nangngnainil34982379esssgg'},
                        'start': {'N': '1526000000'}
                    }
                ]
            }
        }

        events = getEventsFromBatchGetResponse(response, 'dev-event')

        event = events[0]
        self.assertIsInstance(event, Event)
        self.assertEqual(event.eventId, 11)
        self.assertEqual(event.eventName, 'イベント名')
        self.assertEqual(event.location, 'BKC アクロスウィング')
        self.assertEqual(event.university, '立命館大学')
        self.assertEqual(event.updateTime, 1552629886)
        self.assertEqual(event.countOfLike, 0)
        self.assertIsNone(event.end)
        self.assertEqual(
            event.urlData, 'https://nangngnainil34982379esssgg')
        self.assertEqual(event.start, 1526000000)

    def testGetEventsForWeekMailFromResponse(self):
        events = getEventsForWeekMailFromResponse(res)
        eventTop = events[0]
        eventNext = events[1]

        self.assertEqual(eventTop.eventId, 15)
        self.assertEqual(eventNext.eventId, 14)

    def testGetEventsFromResponse(self):
        events = getEventsFromResponse(res)
        eventTop = events[0]

        self.assertIsInstance(eventTop, Event)
