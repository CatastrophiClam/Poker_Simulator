import unittest

from src.common.enums.card import Card as C
from src.common.game_utils.ranker import *

class TestRankerOrganize(unittest.TestCase):

    def test_high_card(self):
        h1 = organize([C.CA, C.C9, C.C10, C.CK, C.S2])
        self.assertEqual(h1.hand_type, HT.HIGH_CARD, "5 card type")
        self.assertEqual(h1.hand, [C.S2, C.C9, C.C10, C.CK, C.CA], "5 card hand")

        h1 = organize([C.CA, C.C9, C.C10, C.CK, C.S2, C.H8, C.DJ])
        self.assertEqual(h1.hand_type, HT.HIGH_CARD, "7 card type")
        self.assertEqual(h1.hand, [C.C9, C.C10, C.DJ, C.CK, C.CA], "7 card hand")

    def test_pair(self):
        h1 = organize([C.CA, C.DA, C.C10, C.CK, C.S2, C.H8, C.DJ])
        self.assertEqual(h1.hand_type, HT.PAIR, "7 card type")
        self.assertEqual(h1.primary, 12, "7 card primary")
        self.assertEqual(h1.kickers, [C.CK, C.DJ, C.C10, C.H8, C.S2], "7 card kickers")

    def test_two_pair(self):
        h1 = organize([C.C9, C.D9, C.H5, C.D5, C.S8, C.SA, C.D2])
        self.assertEqual(h1.hand_type, HT.TWO_PAIR)
        self.assertEqual(h1.primary, 7)
        self.assertEqual(h1.secondary, 3)
        self.assertEqual(h1.kickers, [C.SA, C.S8, C.D2])

    def test_trips(self):
        h1 = organize([C.C10, C.D10, C.S10, C.H9, C.HQ, C.D5, C.C2])
        self.assertEqual(h1.hand_type, HT.TRIPS)
        self.assertEqual(h1.primary, 8)
        self.assertEqual(h1.kickers, [C.HQ, C.H9, C.D5, C.C2])

    def test_straight(self):
        h1 = organize([C.CJ, C.S10, C.H9, C.D8, C.C7, C.D6, C.SA])
        self.assertEqual(h1.hand_type, HT.STRAIGHT)
        self.assertEqual(h1.hand, [C.C7, C.D8, C.H9, C.S10, C.CJ])

        h1 = organize([C.CJ, C.C7, C.S10, C.D8, C.H9, C.D6, C.SA])
        self.assertEqual(h1.hand_type, HT.STRAIGHT)
        self.assertEqual(h1.hand, [C.C7, C.D8, C.H9, C.S10, C.CJ])

        h1 = organize([C.CA, C.D2, C.H8, C.H2, C.D3, C.S4, C.D5])
        self.assertEqual(h1.hand_type, HT.STRAIGHT)
        self.assertEqual(h1.hand, [C.D2, C.D3, C.S4, C.D5, C.CA])

    def test_flush(self):
        h1 = organize([C.C2, C.C3, C.C8, C.C10, C.CJ, C.CA, C.D7])
        self.assertEqual(h1.hand_type, HT.FLUSH)
        self.assertEqual(h1.hand, [C.C3, C.C8, C.C10, C.CJ, C.CA])
