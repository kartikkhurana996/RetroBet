import random

# Card values
CARD_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = list(CARD_VALUES.keys())

class Deck:
    def __init__(self):
        self.cards = [(rank, suit) for suit in SUITS for rank in RANKS]
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop() if self.cards else None


def hand_value(hand):
    value = sum(CARD_VALUES[rank] for rank, _ in hand)
    aces = sum(1 for rank, _ in hand if rank == 'A')

    # Adjust for aces
    while value > 21 and aces > 0:
        value -= 10
        aces -= 1

    return value


def is_blackjack(hand):
    return len(hand) == 2 and hand_value(hand) == 21


def play_blackjack():
    deck = Deck()
    player = [deck.deal(), deck.deal()]
    dealer = [deck.deal(), deck.deal()]

    # Player Blackjack wins immediately unless dealer also has blackjack
    if is_blackjack(player):
        if is_blackjack(dealer):
            return {'result': 'Tie (Both Blackjack)', 'player': player, 'dealer': dealer}
        return {'result': 'Player Blackjack!', 'player': player, 'dealer': dealer}

    # Player Turn (hit until 17+ for logic demo)
    while hand_value(player) < 17:
        player.append(deck.deal())

    if hand_value(player) > 21:
        return {'result': 'Player Bust', 'player': player, 'dealer': dealer}

    # Dealer Turn (dealer hits until 17+)
    while hand_value(dealer) < 17:
        dealer.append(deck.deal())

    if hand_value(dealer) > 21:
        return {'result': 'Dealer Bust (Player Wins)', 'player': player, 'dealer': dealer}

    # Compare values
    player_val = hand_value(player)
    dealer_val = hand_value(dealer)

    if player_val > dealer_val:
        result = 'Player Wins'
    elif dealer_val > player_val:
        result = 'Dealer Wins'
    else:
        result = 'Tie'

    return {
        'result': result,
        'player': player,
        'dealer': dealer
    }


# For testing only
if __name__ == '__main__':
    print(play_blackjack())
