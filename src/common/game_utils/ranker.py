from typing import List

from src.common.models.game import OrganizedHand
from src.common.enums.card import Card

"""
Assumes max 7 cards
"""
def organize(cards: List[Card]) -> OrganizedHand:
    counts = [0]*13
    flushes = [0]*4
    for i in range(len(cards)):
        counts[cards[i].value%13] += 1
        flushes[cards[i].value//13] += 1

    cards.sort(key=lambda x: x.value % 13)
    card_ints = [i.value for i in cards]

    org_hand = OrganizedHand(cards,[],[],[],[])

    # organize cards
    for i in range(len(counts)):
        if counts[i] == 4:
            org_hand.quads.append(i)
            break
        elif counts[i] == 3:
            if len(org_hand.trips) == 1:
                org_hand.pairs.append(org_hand.trips[0])
                org_hand.trips.append(i)
            else:
                org_hand.trips.append(i)
        elif counts[i] == 2:
            org_hand.pairs.append(i)

    maxPairs = 2 if len(org_hand.trips) == 0 else 1
    while len(org_hand.pairs) > maxPairs:
        del org_hand.pairs[0]
    
    flush_ind = -1
    org_hand.has_flush = False
    for i in range(len(flushes)):
        if flushes[i] >= 5:
            flush_ind = i
            org_hand.has_flush = True
            break

    # lowest ind is the start of the straight, it is 12 for A 2 3 4 5, 8 for 10 J Q K A, etc.
    straight_start = -1
    org_hand.has_straight = False
    if counts[12] >= 1 and counts[0]>=1 and counts[1]>=1 and counts[2]>=1 and counts[3]>=1:
        straight_start = 12
        org_hand.has_straight = True

    for i in range(9):
        if counts[i]>=1 and counts[i+1]>=1 and counts[i+2]>=1 and counts[i+3]>=1 and counts[i+4]>=1:
            straight_start = 8 if i == 8 else max(i, straight_start)
            org_hand.has_straight = True

    # MAKE HAND
    # check royal flush/ straight flush after quads
    if len(org_hand.quads) == 1:
        org_hand.hand = [i for i in card_ints]
        ind = 0
        while len(org_hand.hand) > 5:
            if org_hand.hand[ind] % 13 != org_hand.quads[0]:
                del org_hand.hand[ind]
            else:
                ind += 1
        new_hand = [Card(i) for i in org_hand.hand]
        org_hand.hand = new_hand
    # full house
    elif len(org_hand.trips) == 1 and len(org_hand.pairs) == 1:
        org_hand.hand = [Card(i) for i in filter(lambda x: x % 13 == org_hand.pairs[0], card_ints)] + \
               [Card(i) for i in filter(lambda x: x % 13 == org_hand.trips[0], card_ints)]
    # flush
    elif org_hand.has_flush:
        org_hand.hand = [i for i in filter(lambda x: x // 13 == flush_ind, card_ints)]
        while len(org_hand.hand) > 5:
            del org_hand.hand[0]
        new_hand = [Card(i) for i in org_hand.hand]
        org_hand.hand = new_hand
    # straight
    elif org_hand.has_straight:
        temp_straight = []
        if straight_start == 12:
            temp_straight = [0, 1, 2, 3, 12]
        else:
            temp_straight = [i for i in range (straight_start, straight_start+5)]
        org_hand.hand = []
        for i in temp_straight:
            for j in card_ints:
                if j % 13 == i:
                    org_hand.hand.append(j)
                    break
        temp_straight = [Card(i) for i in org_hand.hand]
        org_hand.hand = temp_straight
    # trips
    elif len(org_hand.trips) == 1:
        org_hand.hand = [i for i in card_ints]
        ind = 0
        while len(org_hand.hand) > 5:
            if org_hand.hand[ind] % 13 != org_hand.trips[0]:
                del org_hand.hand[ind]
            else:
                ind += 1
        new_hand = [Card(i) for i in org_hand.hand]
        org_hand.hand = new_hand
    # 2 pair
    elif len(org_hand.pairs) >= 2:
        org_hand.hand = [i for i in card_ints]
        ind = 0
        while len(org_hand.hand) > 5:
            if org_hand.hand[ind] % 13 != org_hand.pairs[-1] and org_hand.hand[ind] % 13 != org_hand.pairs[-2]:
                del org_hand.hand[ind]
            else:
                ind += 1
        new_hand = [Card(i) for i in org_hand.hand]
        org_hand.hand = new_hand
    # pair
    elif len(org_hand.pairs) == 1:
        org_hand.hand = [i for i in card_ints]
        ind = 0
        while len(org_hand.hand) > 5:
            if org_hand.hand[ind] % 13 != org_hand.pairs[0]:
                del org_hand.hand[ind]
            else:
                ind += 1
        new_hand = [Card(i) for i in org_hand.hand]
        org_hand.hand = new_hand
    # high card
    else:
        if len(cards) > 5:
            org_hand.hand = cards[-5:]
        else:
            org_hand.hand = cards

    # check for straight flush/royal flush
    sf_ind = -1
    if org_hand.has_straight and org_hand.has_flush:
        cards_to_print = [Card(i) for i in card_ints]
        print("Hand has straight and flush: %s" % cards_to_print)
        temp_hand = [i for i in filter(lambda x: x // 13 == flush_ind, card_ints)]
        count = 1
        for i in range(1, len(temp_hand)):
            if (temp_hand[i]%13) - (temp_hand[i-1]%13) == 1:
                count += 1
                if count >= 5:
                    sf_ind = i-4
            else:
                sf_ind = i
                count = 1
        sf_ind = temp_hand[sf_ind] % 13
        
        if temp_hand[-1] % 13 == 12 and temp_hand[0] % 13 == 0 and temp_hand[1] % 13 == 1 and \
                temp_hand[2] % 13 == 2 and temp_hand[3] % 13 == 3:
            if sf_ind != 8:
                sf_ind = 12

        if sf_ind != -1:
            if sf_ind == 12:
                org_hand.hand = [Card(i+13*flush_ind) for i in [0, 1, 2, 3, 12]]
            else:
                print("Hand: %s has sf_ind of %d" % (temp_hand, sf_ind))
                org_hand.hand = [Card(i+13*flush_ind) for i in range(sf_ind, sf_ind+5)]

    org_hand.has_straight_flush = sf_ind != -1
    return org_hand
        
"""
Get high card score of a hand following scoring rule below
:type cards: Card[5], sorted ascending
"""
def get_high_card_score(cards):
    return cards[0].value % 13 + (cards[1].value % 13)**2 + (cards[2].value % 13)**3 + (cards[3].value % 13)**4 + (cards[4].value % 13)**5

"""
Assign a score to each hand
Scoring works as follows:
High card: 0 - 264562 (12^5 + 11^4 + ... + 8 for maximum)
Pair: 300000 - 29867883 (300000 + high card score + ((pair card+13)^5)*3)
2 Pair: 30000000 - 30500338 (30 000 000 + top pair card^5 * 2 + bottom pair card^3 * 2 + kicker)
Trips: 31000000 - 46462276 (31 000 000 + (trip card+10)^5 * 3 + kicker1^3 + kicker2)
Straight: 47000000 - 47264562 (47 000 000 + high card score)
Flush: 48000000 - 48264562 (48 000 000 + high card score)
Full House: 49000000 - 49000495 (49 000 000 + (trip+10)^2 + pair)   //NOTE one card from the triple and one from the pair
Quads: 50000000 - 50000495 (50 000 000 + (quad+10)^2 + kicker)
Straight Flush: 51000000 - 51264562 (51 000 000 + high card score)
Royal Flush: 52000000
"""
def get_score(cards: List[Card]):
    
    d = organize(cards)
    if d.has_straight_flush:
        if d.hand[0].value % 13 == 8:
            # Royal Flush
            return 52000000
        else:
            # Straight Flush
            return 51000000 + get_high_card_score(d.hand)
    else:
        if len(d.quads) == 1:
            kicker = [i for i in filter(lambda x: x.value % 13 != d.quads[0], d.hand)][0]
            return 50000000 + (d.quads[0]+10)**2 + (kicker.value % 13)
        elif len(d.trips) == 1 and len(d.pairs) == 1:
            return 49000000 + (d.trips[0]+10)**2 + d.pairs[0]
        elif d.has_flush:
            return 48000000 + get_high_card_score(d.hand)
        elif d.has_straight:
            score = 47000000 + get_high_card_score(d.hand)
            if Card.HA in d.hand or Card.DA in d.hand or Card.CA in d.hand or Card.SA in d.hand:
                score -= 12**5
            return score
        elif len(d.trips) == 1:
            kickers = [i for i in filter(lambda x: x.value % 13 != d.trips[0], d.hand)]
            kickers.sort(key=lambda x: x.value % 13)
            return 31000000 + ((d.trips[0]+10)**5)*3 + kickers[1].value**3 + kickers[0].value
        elif len(d.pairs) >= 2:
            kicker = [i for i in filter(
                lambda x: x.value % 13 != d.pairs[-1] and x.value % 13 != d.pairs[-2], d.hand
            )][0]
            return 30000000 + (d.pairs[1]**5)*2 + (d.pairs[0]**3)*2 + kicker.value % 13
        elif len(d.pairs) == 1:
            return 300000 + get_high_card_score(d.hand) + ((d.pairs[0] + 13)**5)*3
        else:
            return get_high_card_score(d.hand)

