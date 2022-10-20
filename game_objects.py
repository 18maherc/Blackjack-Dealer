import random
import math

# Let's give the info of the card's suits, ranks and values
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
values = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
          'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
points = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}


# Game Objects:
class Card():
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.points = points[value]

    def to_string(self) -> str:
        return f"{self.value} of {self.suit}  ({self.points})"


class Hand():
    def __init__(self):
        self.size = 0
        self.cards = []  # list of  cards
        self.score = 0
        self.done_flag = False
        self.wager = 1

    def add_card(self, card: Card):
        self.size += 1
        self.cards.append(card)
        self.score += card.points
        if self.score > 21:
            for c in self.cards:
                if c.value == 'Ace' and c.points == 11:
                    self.score -= 10
                    c.points = 1
                    break
            self.done_flag = True  # No aces to reduce so flag their bust as done
        elif self.score == 21:
            self.done_flag = True  # auto-stand when player hits 21

    def contains(self, card: Card) -> bool:
        for c in self.cards:
            if card.value == c.value:
                return True
        return False


class Player():
    def __init__(self, starting_hand: Hand):
        self.hands = [starting_hand]
        self.wallet = 0

    def add_hand(self, hand: Hand):
        self.hands.append(hand)

    def delete_hand(self, hand: Hand):
        self.hands.remove(hand)

    def split_hand(self):
        # You can only split if you have one hand
        if len(self.hands) == 1:
            # You can only split a 2 card hand
            if len(self.hands[0].cards) == 2:
                first_card = self.hands[0].cards[0]
                second_card = self.hands[0].cards[1]
                # You can only split if the cards are equal in points (faces and 10 are equal)
                if first_card.points == second_card.points:
                    # Get rid of the hand
                    self.delete_hand(self.hands[0])
                    # Create a new hand
                    new_hand1 = Hand()
                    # Add one of the cards to it
                    new_hand1.add_card(first_card)
                    # Add the hand to the player
                    self.add_hand(new_hand1)
                    # Repeat for the other card
                    new_hand2 = Hand()
                    new_hand2.add_card(second_card)
                    self.add_hand(new_hand2)
                else:
                    raise Exception(
                        "Can only split when two cards are equal in points")
            else:
                raise Exception("Can only split when you have two cards")
        else:
            raise Exception("Can only split when you have a single hand")

    def add_credits(self, credits: int):
        self.wallet += math.ceil(credits)

    def remove_credits(self, credits: int):
        self.wallet -= credits

    def clear(self):
        self.hands.clear()
        self.add_hand(Hand())


class Dealer():
    def __init__(self, hand: Hand):
        self.hand = hand


# Following below is the Deck Class which will create a deck from the given cards
class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for value in values:
                # build 52 Card objects and add them to the list
                self.deck.append(Card(suit, value))

    def add_deck(self):
        new_deck = Deck()
        new_deck.shuffle()
        self.deck.extend(new_deck.deck)
        self.shuffle()

    def to_string(self) -> str:
        deck_comp = ''  # start with an empty string
        for card in self.deck:
            deck_comp += '\n '+card.__str__()  # add each Card object's print string
        return 'The deck has:' + deck_comp

    def shuffle(self):          # shuffle function will shuffle 52 card deck
        random.shuffle(self.deck)

    def deal(self) -> Card:             # deal function will take one card from the deck
        single_card = self.deck.pop()
        return single_card


class Table():
    def __init__(self, player_count: int):
        # Initialize our collection of players
        self.players = []
        # Initialize our Dealer
        self.dealer = Dealer(Hand())

        # Add x number of players to the game
        for i in range(player_count):
            self.players.append(Player(Hand()))

        # Create & shuffle 3 decks together
        self.deck = Deck()
        self.deck.shuffle()
        self.deck.add_deck()
        self.deck.add_deck()

    def add_player(self, player: Player, deposit: int):
        player.wallet = deposit
        self.players.append(player)

    def remove_player(self, player: Player):
        self.players.remove(player)
