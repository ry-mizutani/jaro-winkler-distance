__author__ = 'Jean-Bernard Ratte - jean.bernard.ratte@unary.ca'
import unittest
from jarowinkler import distance


class TestDistance(unittest.TestCase):
    def test_get_jaro_distance(self):
        self.assertEquals(float(0.93), distance.get_jaro_distance("frog", "fog"))
        self.assertEquals(float(0.0), distance.get_jaro_distance("fly", "ant"))
        self.assertEquals(float(0.44), distance.get_jaro_distance("elephant", "hippo"))
        self.assertEquals(float(0.91), distance.get_jaro_distance("ABC Corporation", "ABC Corp"))
        self.assertEquals(float(0.9), distance.get_jaro_distance("PENNSYLVANIA", "PENNCISYLVNIA"))
        self.assertEquals(float(0.93), distance.get_jaro_distance("D N H Enterprises Inc",
                                                                 "D & H Enterprises, Inc."))
        self.assertEquals(float(0.94), distance.get_jaro_distance("My Gym Children's Fitness Center",
                                                                  "My Gym. Childrens Fitness"))

    def test_get_jaro_distance_raises(self):
        with self.assertRaises(distance.JaroDistanceException) as e:
            distance.get_jaro_distance(None, None)
        self.assertTrue('NoneType, NoneType' in e.exception.message)

        with self.assertRaises(distance.JaroDistanceException) as e:
            distance.get_jaro_distance(" ", None)
        self.assertTrue('str, NoneType' in e.exception.message)

        with self.assertRaises(distance.JaroDistanceException) as e:
            distance.get_jaro_distance(None, "")
        self.assertTrue('NoneType, str' in e.exception.message)

    def test_transposition(self):
        self.assertEqual(distance._transpositions("", ""), 0)
        self.assertEqual(distance._transpositions("PENNSYLVANIA", "PENNCISYLVNIA"), 4)

    def test_get_diff_index(self):
        self.assertEquals(distance._get_diff_index(None, None), -1)
        self.assertEquals(distance._get_diff_index("", ""), -1)
        self.assertEquals(distance._get_diff_index("", "abc"), 0)
        self.assertEquals(distance._get_diff_index("abc", ""), 0)
        self.assertEquals(distance._get_diff_index("abc", "abc"), -1)
        self.assertEquals(distance._get_diff_index("ab", "abxyz"), 2)
        self.assertEquals(distance._get_diff_index("abcde", "xyz"), 0)
        self.assertEquals(distance._get_diff_index("abcde", "abxyz"), 2)

    def test_get_matching_characters(self):
        self.assertEqual(distance._get_matching_characters("hello", "halloa"), "hllo",
                         "The matching character should be hel")
        self.assertEquals(distance._get_matching_characters("ABC Corporation",
                                                            "ABC Corp"), "ABC Corp")
        self.assertEquals(distance._get_matching_characters("PENNSYLVANIA",
                                                            "PENNCISYLVNIA"), "PENNSYLVANI")
        self.assertEquals(distance._get_matching_characters("My Gym Children's Fitness Center",
                                                            "My Gym. Childrens Fitness"), "My Gym Childrens Fitness")
        self.assertEquals(distance._get_matching_characters("D N H Enterprises Inc",
                                                            "D & H Enterprises, Inc."), "D  H Enterprises Inc")

    def test_get_prefix(self):
        self.assertEquals(distance._get_prefix(None, None), "")
        self.assertEquals(distance._get_prefix("", ""), "")
        self.assertEquals(distance._get_prefix("", None), "")
        self.assertEquals(distance._get_prefix("", "abc"), "")
        self.assertEquals(distance._get_prefix("abc", ""), "")
        self.assertEquals(distance._get_prefix("abc", "abc"), "abc")
        self.assertEquals(distance._get_prefix("abc", "a"), "a")
        self.assertEquals(distance._get_prefix("ab", "abxyz"), "ab")
        self.assertEquals(distance._get_prefix("abcde", "abxyz"), "ab")
        self.assertEquals(distance._get_prefix("abcde", "xyz"), "")
        self.assertEquals(distance._get_prefix("xyz", "abcde"), "")
        self.assertEquals(distance._get_prefix("i am a machine", "i am a robot"), "i am a ")

    def test_score(self):
        self.assertEquals(distance._score("", ""), 0.0)
        self.assertEquals(distance._score("", "a"), 0.0)
        self.assertEquals(distance._score("aaapppp", ""), 0.0)
        self.assertEquals(distance._score("frog", "fog"), 0.9166666666666666)
        self.assertEquals(distance._score("fly", "ant"), 0.0)
        self.assertEquals(distance._score("elephant", "hippo"), 0.44166666666666665)
        self.assertEquals(distance._score("hippo", "elephant"), 0.44166666666666665)
        self.assertEquals(distance._score("hippo", "zzzzzzzz"), 0.0)
        self.assertEquals(distance._score("hello", "hallo"), 0.8666666666666667)
        self.assertEquals(distance._score("ABC Corporation", "ABC Corp"), 0.8444444444444444)
        self.assertEquals(distance._score("PENNSYLVANIA", "PENNCISYLVNIA"), 0.8300310800310801)
        self.assertEquals(distance._score("My Gym Children's Fitness Center",
                                          "My Gym. Childrens Fitness"), 0.9033333333333333)
        self.assertEquals(distance._score("D N H Enterprises Inc", "D & H Enterprises, Inc."), 0.9073153899240856)


if __name__ == '__main__':
    unittest.main()