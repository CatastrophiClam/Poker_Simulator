import unittest

from src.common.game_utils.tests.test_ranker_basic_scoring import TestRankerBasicScoring
from src.common.game_utils.tests.test_ranker_organize import TestRankerOrganize


class TestAll(unittest.TestCase):

    def test_ranker(self):
        print("Testing hand ranker basic scoring")
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestRankerBasicScoring)
        unittest.TextTestRunner().run(suite)

        print("Testing hand ranker organizing")
        suite1 = unittest.defaultTestLoader.loadTestsFromTestCase(TestRankerOrganize)
        unittest.TextTestRunner().run(suite1)

