from enum import IntEnum


class Card(IntEnum):
    S2 = 0
    S3 = 1
    S4 = 2
    S5 = 3
    S6 = 4
    S7 = 5
    S8 = 6
    S9 = 7
    S10 = 8
    SJ = 9
    SQ = 10
    SK = 11
    SA = 12
    C2 = 13
    C3 = 14
    C4 = 15
    C5 = 16
    C6 = 17
    C7 = 18
    C8 = 19
    C9 = 20
    C10 = 21
    CJ = 22
    CQ = 23
    CK = 24
    CA = 25
    D2 = 26
    D3 = 27
    D4 = 28
    D5 = 29
    D6 = 30
    D7 = 31
    D8 = 32
    D9 = 33
    D10 = 34
    DJ = 35
    DQ = 36
    DK = 37
    DA = 38
    H2 = 39
    H3 = 40
    H4 = 41
    H5 = 42
    H6 = 43
    H7 = 44
    H8 = 45
    H9 = 46
    H10 = 47
    HJ = 48
    HQ = 49
    HK = 50
    HA = 51

    def __str__(self):
        ans = "{0}{1}"
        symbols = [u'\u2660', u'\u2663', u'\u2666', u'\u2665']
        numbers = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        return ans.format(numbers[self.value % 13], symbols[self.value//13])

    def __repr__(self):
        return self.__str__()
