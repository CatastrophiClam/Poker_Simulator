from typing import List

from src.common.enums.hand_types import HandType as HT
from src.common.models.game import OrganizedHand
from src.common.enums.card import Card

"""
Organize cards into best hand
Assume 5 - 7 card hands
"""
def organize(cards: List[Card]) -> OrganizedHand:
    organized_hand = OrganizedHand()
    organized_hand.cards = cards

    counts = [0]*13
    flushes = [0]*4
    for i in range(len(cards)):
        counts[cards[i].value % 13] += 1
        flushes[cards[i].value//13] += 1

    # NOTE cards is sorted BIGGEST CARD FIRST
    cards.sort(key=lambda x: x.value % 13, reverse=True)

    ### Assemble top pair, 2 pair, trips, quads, and full house ###
    ind = 0
    while ind < len(cards):
        card = cards[ind]
        card_val = card.value % 13
        # Found quads
        if counts[card_val] == 4:
            organized_hand.primary = card_val
            organized_hand.hand_type = HT.QUADS
            ind += 3
        # Found a pair
        if counts[card_val] == 2:
            if organized_hand.hand_type.value < HT.PAIR.value:
                organized_hand.primary = card_val
                organized_hand.hand_type = HT.PAIR
            elif organized_hand.hand_type == HT.PAIR:
                organized_hand.secondary = card_val
                organized_hand.hand_type = HT.TWO_PAIR
            elif organized_hand.hand_type == HT.TRIPS:
                organized_hand.secondary = card_val
                organized_hand.hand_type = HT.FULL_HOUSE
            else:
                organized_hand.kickers += cards[ind:ind+2]
            ind += 1
        # Found trips
        elif counts[card_val] == 3:
            if organized_hand.hand_type.value < HT.PAIR.value:
                organized_hand.primary = card_val
                organized_hand.hand_type = HT.TRIPS
            elif organized_hand.hand_type.value < HT.TRIPS.value:
                organized_hand.secondary = organized_hand.primary
                organized_hand.primary = card_val
                organized_hand.hand_type = HT.FULL_HOUSE
            elif organized_hand.hand_type == HT.TRIPS.value:
                organized_hand.secondary = card_val
                organized_hand.hand_type = HT.FULL_HOUSE
            else:
                organized_hand.kickers += cards[ind:ind+3]
            ind += 2
        else:
            organized_hand.kickers.append(card)
            if organized_hand.hand_type == HT.NONE:
                organized_hand.hand_type = HT.HIGH_CARD
        ind += 1
    if organized_hand.hand_type == HT.HIGH_CARD:
        organized_hand.hand = organized_hand.kickers[:min(5, len(organized_hand.kickers))]
    elif organized_hand.hand_type == HT.PAIR:
        organized_hand.hand = [i for i in cards if i.value % 13 == organized_hand.primary] + organized_hand.kickers[:3]
    # tbh I should put hands for 2 pair, trips and quads for consistency but hands for those types aren't used
    # and I'm too lazy

    ### Assemble straight, flush, straight flush (includes royal flush) ###

    # Deal with flushes
    all_flush_cards = None
    flush_suit = None
    for suit in range(len(flushes)):
        if flushes[suit] >= 5:
            flush_suit = suit
            all_flush_cards = []
            break
    # There's a flush
    if all_flush_cards is not None:
        for card in cards:
            if card.value // 13 == flush_suit:
                all_flush_cards.append(card)
        # Take biggest flush for flush
        if organized_hand.hand_type.value < HT.FLUSH:
            organized_hand.hand_type = HT.FLUSH
            organized_hand.hand = all_flush_cards[:5].copy()

    # Deal with straights
    cards_to_straight = 1
    # All cards that can be part of a straight - note this can include multiple
    # suits of the same card
    all_straight_cards: List[Card] = [cards[0]]

    for i in range(1, len(cards)):
        if cards[i].value % 13 == cards[i-1].value % 13 - 1:
            cards_to_straight += 1
            all_straight_cards.append(cards[i])
        elif cards[i].value % 13 == cards[i-1].value % 13:
            all_straight_cards.append(cards[i])
        else:
            if cards_to_straight >= 5:
                break
            else:
                cards_to_straight = 1
                all_straight_cards.clear()
                all_straight_cards.append(cards[i])

    # Check case of A low straight
    if cards_to_straight >= 4 and all_straight_cards[-1].value % 13 == 0:
        for card in cards:
            if card.value % 13 == 12:
                if all_straight_cards[-1].value % 13 != 12:
                    cards_to_straight += 1
                all_straight_cards.append(card)

    # At this point all_straight_cards is sorted highest to lowest, where lowest could be an A
    # Note that there can be repeated cards of same value but not suit in all_straight_cards
    # Only assemble straight if there's no higher value hand already
    if cards_to_straight >= 5 and organized_hand.hand_type.value < HT.STRAIGHT:
        cardCount = 1
        straight = [all_straight_cards[0]]
        for i in range(1, len(all_straight_cards)):
            if all_straight_cards[i].value % 13 != straight[-1].value % 13:
                straight.append(all_straight_cards[i])
                cardCount += 1
            if cardCount == 5:
                organized_hand.hand_type = HT.STRAIGHT
                organized_hand.hand = straight
                break

    # See if there's a straight flush
    if flush_suit is not None and cards_to_straight >= 5:
        straight_flush_cards = [i for i in filter(lambda x: x.value // 13 == flush_suit, all_straight_cards)]
        straight_flush = [straight_flush_cards[0]]
        for i in range(1, len(straight_flush_cards)):
            n = straight_flush_cards[i].value % 13
            last = straight_flush[-1].value % 13
            if n == last - 1 or n == 12 and last == 0:
                straight_flush.append(straight_flush_cards[i])
            else:
                straight_flush.clear()
                straight_flush.append(straight_flush_cards[i])
            if len(straight_flush) == 5:
                organized_hand.hand_type = HT.STRAIGHT_FLUSH
                organized_hand.hand = straight_flush
                break

    if organized_hand.hand is not None:
        organized_hand.hand.sort(key=lambda x: x.value % 13)
    return organized_hand


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
    if d.hand_type == HT.STRAIGHT_FLUSH:
        if d.hand[0].value % 13 == 8:
            # Royal Flush
            return 52000000
        else:
            # Straight Flush
            score = 51000000 + get_high_card_score(d.hand)
            if d.hand[-1].value % 13 == 12 and d.hand[0].value % 13 == 0:
                score -= 12**5
            return score
    else:
        if d.hand_type == HT.QUADS:
            kicker = d.kickers[0]
            return 50000000 + (d.primary + 10)**2 + (kicker.value % 13)
        elif d.hand_type == HT.FULL_HOUSE:
            return 49000000 + (d.primary + 10)**2 + d.secondary
        elif d.hand_type == HT.FLUSH is not None:
            return 48000000 + get_high_card_score(d.hand)
        elif d.hand_type == HT.STRAIGHT:
            score = 47000000 + get_high_card_score(d.hand)
            # Ace low straight case
            if d.hand[-1].value % 13 == 12 and d.hand[0].value % 13 == 0:
                score -= 12**5
            return score
        elif d.hand_type == HT.TRIPS:
            return 31000000 + ((d.primary + 10)**5)*3 + (d.kickers[0].value % 13)**3 + d.kickers[1].value % 13
        elif d.hand_type == HT.TWO_PAIR:
            return 30000000 + (d.primary**5)*2 + (d.secondary**3)*2 + d.kickers[0].value % 13
        elif d.hand_type == HT.PAIR:
            return 300000 + get_high_card_score(d.hand) + ((d.primary + 13)**5)*3
        else:
            return get_high_card_score(d.hand)

