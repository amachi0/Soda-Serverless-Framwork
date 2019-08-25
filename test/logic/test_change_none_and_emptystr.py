import unittest
from app.util.change_none_and_emptystr \
    import emptystrToNoneInDict, NoneToEmptystrInDict


class TestChangeNoneAndEmptystr(unittest.TestCase):
    def testEmptystrToNoneInDict(self):
        item = {
            'test': 1,
            'テスト': '',
            'テステス': 'hello'
        }

        emptystrToNoneInDict(item)

        expected = {
            'test': 1,
            'テスト': None,
            'テステス': 'hello'
        }

        self.assertEqual(item, expected)

    def testNoneToEmptystrInDict(self):
        item = {
            'test': 1,
            'テスト': None,
            'テステス': 'hello'
        }

        NoneToEmptystrInDict(item)

        expected = {
            'test': 1,
            'テスト': '',
            'テステス': 'hello'
        }

        self.assertEqual(item, expected)
