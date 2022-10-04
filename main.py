import random

# Let's give the info of the card's suits, ranks and values

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
         'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}


class Card():
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.points = values[value]


class Hand():
    def __init__(self, size):
        self.size = size
        self.cards = []  # list of  cards
        self.total = 0
        self.ace_total = 10

    def add_Card(self, card):
        self.size += 1
        self.cards.append(card)
        self.total += card.points
        if card.value == 'Ace':
            self.ace_total += card.points
        #Player1Hand = Hand()
        #Player1Hand.add_Card(Card('Ace', 'Heart'))

    def contains(self, card):
        for c in self.cards:
            if card.value == c.value:
                return True
        return False


class Player():
    def __init__(self, money, hand):
        self.money = money


class Dealer():
    def __init__(self, hand):
        return
