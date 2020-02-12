from src.common.enums.card import Card as C

"""
range object:
   2 3 4 5 6 7 8 9 10 J K Q A
2  O O O O O O O O O  O O O O
3  S O O O O
4  S S O O O
5  S S S O O
6  x x x x x
7  ...
8
9
0
10
J
Q
K
A
to index, suited is row > col, unsuited is row <= col
"""

# Redo
class Range:

    grid = []

    def __init__(self, grid):
        self.grid = grid

    def __str__(self):
        return self.grid

    """
    Convert a range 2D array to a list of possible hands
    """
    def to_possible_hands(self):
        answer = []
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                if self.grid[r][c]:
                    # suited
                    if r > c:
                        answer += [(C(r+i*13), C(c+i*13)) for i in [0,1,2,3]]
                    # unsuited
                    else:
                        temp = []
                        for i in range(4):
                            for j in range(4):
                                if i != j:
                                    temp.append((C(r+i*13), C(c+j*13)))
                        answer += temp
        return answer

    def intersect(self, r1):
        return Range([ [r1[r][c] and self.grid[r][c] for c in range(len(r1[r]))] for r in range(len(r1)) ])

    """
    :type cards: tuple of 2 Cards
    """
    def is_in_self(self, cards):
        a = max(cards[0].value % 13, cards[1].value % 13)
        b = min(cards[0].value % 13, cards[1].value % 13)
        if cards[0].value // 13 == cards[1].value // 13:
            return self.grid[a][b]
        else:
            return self.grid[b][a]

    def clone(self):
        return Range([i.copy for i in self.grid])
