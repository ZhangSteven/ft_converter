"""
Test the open_jpm.py
"""

import unittest2
from ft_converter.match import match, match_repeat, MatchedItemNotFound



class TestMatch(unittest2.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestMatch, self).__init__(*args, **kwargs)



    def test_match(self):
        list_a, list_b = create_list1()
        matched_list = match(list_a, list_b, is_matched)
        self.assertEqual(len(matched_list), 3)
        self.assertEqual(matched_list[0], (1, -1))
        self.assertEqual(matched_list[1], (2, -2))
        self.assertEqual(matched_list[2], (3, -3))



    def test_match2(self):
        list_a, list_b = create_list2()
        matched_list = match(list_a, list_b, is_matched)
        self.assertEqual(len(matched_list), 3)
        self.assertEqual(matched_list[0], (1, -1))
        self.assertEqual(matched_list[1], (4.0625, -4))
        self.assertEqual(matched_list[2], (3, -3))



    def test_match3(self):
        list_a, list_b = create_list3()
        with self.assertRaises(MatchedItemNotFound):
            matched_list = match(list_a, list_b, is_matched)



    def test_match4(self):
        list_a, list_b = create_list4()
        with self.assertRaises(MatchedItemNotFound):
            matched_list = match(list_a, list_b, is_matched)



    def test_match_repeat(self):
        list_a, list_b = create_list1()
        matched_list, unmatched_items = match_repeat(list_a, list_b, is_matched)
        self.assertEqual(len(matched_list), 3)
        self.assertEqual(len(unmatched_items), 0)
        self.assertEqual(matched_list[0], (1, -1))
        self.assertEqual(matched_list[1], (2, -2))
        self.assertEqual(matched_list[2], (3, -3))



    def test_match_repeat2(self):
        list_a, list_b = create_list2()
        matched_list, unmatched_items = match_repeat(list_a, list_b, is_matched)
        self.assertEqual(len(matched_list), 3)
        self.assertEqual(len(unmatched_items), 0)
        self.assertEqual(matched_list[0], (1, -1))
        self.assertEqual(matched_list[1], (4.0625, -4))
        self.assertEqual(matched_list[2], (3, -3))



    def test_match_repeat3(self):
        list_a, list_b = create_list3()
        matched_list, unmatched_items = match_repeat(list_a, list_b, is_matched)
        self.assertEqual(len(matched_list), 3)
        self.assertEqual(len(unmatched_items), 0)
        self.assertEqual(matched_list[0], (1, -1))
        self.assertEqual(matched_list[1], (3, -3))
        self.assertEqual(matched_list[2], (1, -1))



    def test_match_repeat4(self):
        list_a, list_b = create_list4()
        matched_list, unmatched_items = match_repeat(list_a, list_b, is_matched)
        self.assertEqual(len(matched_list), 3)
        self.assertEqual(len(unmatched_items), 2)
        self.assertEqual(matched_list[0], (1, -1))
        self.assertEqual(matched_list[1], (3, -3))
        self.assertEqual(matched_list[2], (2.0625, -2))
        self.assertEqual(unmatched_items[0], 4)
        self.assertEqual(unmatched_items[1], 8)



def create_list1():
    list_a = [1, 2, 3]
    list_b = [-1, -2, -3, -4]
    return list_a, list_b



def create_list2():
    list_a = [1, 4.0625, 3]
    list_b = [-1, -2, -3, -4]
    return list_a, list_b



def create_list3():
    list_a = [1, 3, 1]
    list_b = [-1, -2, -3, -4]
    return list_a, list_b



def create_list4():
    list_a = [1, 4, 3, 2.0625, 8]
    list_b = [-1, 5, -2, -3]
    return list_a, list_b



def is_matched(item_a, item_b):
    """
    To test the match() and match_repeat() functions
    """
    if abs(item_a + item_b) < 0.1:
        return True

    return False

