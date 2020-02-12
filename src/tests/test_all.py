import unittest

from src.common.game_utils.tests.test_ranker import TestRanker


class TestAll(unittest.TestCase):

    def test_ranker(self):
        print("Testing Hand Ranker")
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestRanker)
        unittest.TextTestRunner().run(suite)
