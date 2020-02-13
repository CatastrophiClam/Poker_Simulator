import unittest

from src.common.enums.card import Card as C
from src.common.game_utils.ranker import *

class TestRankerBasicScoring(unittest.TestCase):

    def test_intra_high_card(self):
        s1 = get_score([C.C2, C.C4, C.C5, C.S8, C.SA])
        s2 = get_score([C.C2, C.C4, C.C5, C.S8, C.SK])
        s3 = get_score([C.C3, C.C4, C.C5, C.S8, C.SA])

        s5 = get_score([C.C2, C.C3, C.C4, C.S5, C.SA])
        s6 = get_score([C.C8, C.C10, C.CJ, C.SQ, C.SK])

        s7 = get_score([C.C7, C.C8, C.C9, C.SK, C.SA])
        s8 = get_score([C.C2, C.C3, C.C10, C.SK, C.SA])

        self.assertGreater(s1, s2, "Higher high card")
        self.assertGreater(s3, s1, "Higher kicker")
        self.assertGreater(s5, s6, "Higher high card, lowest lower cards")
        self.assertGreater(s8, s7, "Higher mid card")

    def test_intra_pairs(self):
        s1 = get_score([C.CA, C.DA, C.C5, C.S8, C.SJ])
        s2 = get_score([C.CK, C.DK, C.C5, C.S8, C.SJ])
        self.assertGreater(s1, s2, "Higher pair")

        s3 = get_score([C.C3, C.S3, C.C4, C.S5, C.S6])
        s4 = get_score([C.C2, C.S2, C.CQ, C.SK, C.SA])
        self.assertGreater(s3, s4, "Higher pair lowest kickers")

        s5 = get_score([C.C10, C.S10, C.DA, C.H5, C.S6])
        s6 = get_score([C.C10, C.S10, C.DK, C.H5, C.S6])
        self.assertGreater(s5, s6, "Same pair higher kicker")

    def test_intra_2_pair(self):
        s1 = get_score([C.C3, C.S3, C.D4, C.H4, C.S6])
        s2 = get_score([C.C2, C.S2, C.D3, C.H4, C.S6])
        self.assertGreater(s1, s2, "Higher 2 pair")

        s3 = get_score([C.CA, C.SA, C.D2, C.H2, C.S6])
        s4 = get_score([C.CK, C.SK, C.DQ, C.HQ, C.S6])
        self.assertGreater(s3, s4, "Higher pair, lowest other pair")

        s5 = get_score([C.C3, C.S3, C.D2, C.H2, C.SA])
        s6 = get_score([C.C3, C.S3, C.D2, C.H2, C.S4])
        self.assertGreater(s5, s6, "Same 2 pair higher kicker")

        s7 = get_score([C.C3, C.S3, C.S4, C.H4, C.HK, C.S9, C.H2])
        s8 = get_score([C.C3, C.S3, C.S4, C.H4, C.HK, C.HA, C.S7])
        self.assertGreater(s8, s7)

        s7 = get_score([C.C3, C.S3, C.S4, C.H4, C.H5, C.S9, C.D5])
        s8 = get_score([C.C3, C.S3, C.S4, C.H4, C.H5, C.HA, C.S5])
        self.assertGreater(s8, s7)

    def test_intra_trips(self):
        s1 = get_score([C.C10, C.S10, C.D10, C.H5, C.S6])
        s2 = get_score([C.C9, C.S9, C.D9, C.H5, C.S6])
        self.assertGreater(s1, s2, "Higher trips")

        s3 = get_score([C.C3, C.S3, C.D3, C.H4, C.S5])
        s4 = get_score([C.C2, C.S2, C.D2, C.HK, C.SA])
        self.assertGreater(s3, s4, "Higher trips lowest kickers")

        s5 = get_score([C.C10, C.S10, C.D10, C.H2, C.S4])
        s6 = get_score([C.C10, C.S10, C.D10, C.H2, C.S3])
        self.assertGreater(s5, s6, "Same trips higher kicker")

    def test_intra_straights(self):
        c1 = [C.C3, C.C4, C.S5, C.H6, C.H7]
        c2 = [C.C4, C.C5, C.C6, C.C7, C.H8]
        self.assertGreater(get_score(c2), get_score(c1))

    def test_ace_straight_smaller_than_all_straights(self):
        s1 = get_score([C.CA, C.S2, C.H3, C.D4, C.C5])
        s2 = get_score([C.C2, C.S3, C.H4, C.D5, C.C6])
        s3 = get_score([C.C10, C.CJ, C.HQ, C.SK, C.DA])
        self.assertGreater(s2, s1)
        self.assertGreater(s3, s1)

    def test_intra_flushes(self):
        s1 = get_score([C.CA, C.C10, C.C9, C.C8, C.C7])
        s2 = get_score([C.CK, C.C10, C.C9, C.C8, C.C7])
        self.assertGreater(s1, s2, "Higher flush")

        s3 = get_score([C.CA, C.C6, C.C4, C.C3, C.C2])
        s4 = get_score([C.CK, C.CQ, C.CJ, C.C10, C.C8])
        self.assertGreater(s3, s4, "Higher flush lowest low cards")

    def test_intra_quads(self):
        s1 = get_score([C.CA, C.DA, C.HA, C.SA, C.C7])
        s2 = get_score([C.CK, C.DK, C.HK, C.SK, C.C7])
        self.assertGreater(s1, s2, "Higher quads")

        s3 = get_score([C.C3, C.D3, C.H3, C.S3, C.C2])
        s4 = get_score([C.C2, C.D2, C.H2, C.S2, C.CA])
        self.assertGreater(s3, s4, "Higher quads lowest kicker")

        s5 = get_score([C.C2, C.D2, C.H2, C.S2, C.C3])
        s6 = get_score([C.C2, C.D2, C.H2, C.S2, C.C4])
        self.assertGreater(s6, s5, "Equal quads higher kicker")

    def test_intra_full_house(self):
        s1 = get_score([C.CA, C.SA, C.DA, C.H2, C.S2])
        s2 = get_score([C.CK, C.SK, C.DK, C.H2, C.S2])
        self.assertGreater(s1, s2, "Higher triple")

        s1 = get_score([C.CA, C.SA, C.DA, C.H3, C.S3])
        s2 = get_score([C.CA, C.SA, C.DA, C.H2, C.S2])
        self.assertGreater(s1, s2, "Higher pair")

        s1 = get_score([C.CA, C.SA, C.D2, C.H2, C.S2])
        s2 = get_score([C.C4, C.S4, C.D3, C.H3, C.S3])
        self.assertGreater(s2, s1, "Lowest higher triple biggest higher pair")

    def test_intra_straight_flush(self):
        s1 = get_score([C.CA, C.C2, C.C3, C.C4, C.C5])
        s2 = get_score([C.C2, C.C3, C.C4, C.C5, C.C6])
        self.assertGreater(s2, s1, "Ace low straight flush")

        s1 = get_score([C.C3, C.C4, C.C5, C.C6, C.C7])
        s2 = get_score([C.C2, C.C3, C.C4, C.C5, C.C6])
        self.assertGreater(s1, s2, "Lowest straight flushes")

        s1 = get_score([C.CA, C.CK, C.CQ, C.CJ, C.C10])
        s2 = get_score([C.CK, C.CQ, C.CJ, C.C10, C.C9])
        self.assertGreater(s1, s2, "Highest straight flushes")

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestRankerBasicScoring)
    unittest.TextTestRunner().run(suite)
