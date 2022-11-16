from ctypes import sizeof
import random
import math

# TODO: clear all TODOss

# Let's give the info of the card's suits, ranks and values
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
values = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
          'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
points = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}
card_stack = []


# Game Objects:
class Card():
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.points = points[value]
        self.coords = [250, 80]
        # ^ TODO find out coordinate stuff here ^

    def to_string(self) -> str:
        return f"{self.value} of {self.suit}  ({self.points})"


class Hand():
    def __init__(self):
        self.size = 0
        self.cards = []  # list of  cards
        self.score = 0
        self.done_flag = False
        self.wager = 1
        self.surrender_flag = False
        self.base_coords = [250, 80]
        # ^ TODO find out coordinate stuff here ^

    def add_card(self, card: Card):
        card.coords[0] = self.base_coords[0] - 25*(self.size)
        # ^ TODO find out coordinate stuff here ^
        card.coords[1] = self.base_coords[1]
        # ^ TODO find out coordinate stuff here ^
        self.size += 1
        self.cards.append(card)
        self.score += card.points
        if self.score > 21:
            ace_reduced = True  # Flag for when no aces exist with value 11
            for c in self.cards:
                if c.value == 'Ace' and c.points == 11:
                    self.score -= 10
                    c.points = 1
                    ace_reduced = False
                    break
            if ace_reduced:
                self.done_flag = True  # No aces to left to reduce so flag their bust as done
        elif self.score == 21:
            self.done_flag = True  # auto-stand when player hits 21
        # Add the card to the card_stack
        card_stack.insert(0, card.coords)

    def contains(self, card: Card) -> bool:
        for c in self.cards:
            if card.value == c.value:
                return True
        return False


class DealerHand():
    def __init__(self):
        self.size = 0
        self.cards = []  # list of  cards
        self.score = 0
        self.done_flag = False
        self.base_coords = [0, 165]
        # ^ TODO find out coordinate stuff here ^

    def add_card(self, card: Card):
        card.coords[0] = self.base_coords[0]
        # ^ TODO find out coordinate stuff here ^
        card.coords[1] = self.base_coords[1] + 25*(self.size)
        # ^ TODO find out coordinate stuff here ^
        self.size += 1
        self.cards.append(card)
        self.score += card.points
        if self.score > 21:
            ace_reduced = True  # Flag for when no aces exist with value 11
            for c in self.cards:
                if c.value == 'Ace' and c.points == 11:
                    self.score -= 10
                    c.points = 1
                    ace_reduced = False
                    break
            if ace_reduced:
                self.done_flag = True  # No aces to left to reduce so flag their bust as done
        elif self.score == 21:
            self.done_flag = True  # auto-stand when player hits 21
        # Add the card to the card_stack
        card_stack.insert(0, card.coords)

    def contains(self, card: Card) -> bool:
        for c in self.cards:
            if card.value == c.value:
                return True
        return False


class Player():
    def __init__(self):
        self.hands = []
        self.wallet = 0
        self.split_flag = False
        self.insurance_flag = False
        self.base_coords = [250, 80]

    def add_hand(self, hand: Hand):
        # Set the base coordinates of the new hand
        hand.base_coords[0] = self.base_coords[0]
        hand.base_coords[1] = self.base_coords[1] + 25*len(self.hands)
        # ^ TODO find out coordinate stuff here ^
        # Add the new hand to the player
        self.hands.append(hand)

    def delete_hand(self, hand: Hand):
        for card in hand.cards:
            card_stack.remove(card.coords)
        self.hands.remove(hand)

    def split_hand(self):
        # You can only split if you have one hand
        if len(self.hands) == 1:
            # You can only split a 2 card hand
            if len(self.hands[0].cards) == 2:
                first_card = self.hands[0].cards[0]
                second_card = self.hands[0].cards[1]
                hand_wager = self.hands[0].wager
                # You can only split if the cards are equal in points (faces and 10 are equal)
                if first_card.points == second_card.points:
                    # Get rid of the hand
                    self.delete_hand(self.hands[0])
                    # Add the money back
                    self.add_credits(hand_wager)

                    # Create a new hand
                    new_hand1 = Hand()
                    # Add one of the cards to it
                    new_hand1.add_card(first_card)
                    # Set the wager for it
                    new_hand1.wager = hand_wager
                    # Add the hand to the player
                    self.add_hand(new_hand1)
                    # Take money for hand's wager
                    self.remove_credits(hand_wager)

                    # Repeat for the other card
                    new_hand2 = Hand()
                    new_hand2.add_card(second_card)
                    new_hand2.wager = hand_wager
                    self.add_hand(new_hand2)
                    self.remove_credits(hand_wager)

                    # Turn on the flag for this player
                    self.split_flag = True
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
        self.wallet -= math.ceil(credits)

    def clear(self):
        self.hands.clear()
        self.add_hand(Hand())
        self.split_flag = False
        self.insurance_flag = False


class Dealer():
    def __init__(self, hand: DealerHand):
        hand.base_coords = [0, 165]
        # ^ TODO find out coordinate stuff here ^
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
        self.dealer = Dealer(DealerHand())

        # Add x number of players to the game
        for i in range(player_count):
            new_player = Player()
            new_player.base_coords[0] = 250
            # ^ TODO find out coordinate stuff here ^
            new_player.base_coords[1] = 80 + 110*i
            # ^ TODO find out coordinate stuff here ^
            new_player.add_hand(Hand())
            self.players.append(new_player)

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
