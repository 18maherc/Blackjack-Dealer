import random


class Card():
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value


class Hand():
    def __init__(self, size, cards):
        self.size = size
        self.cards = []

    def add_Card(self, suit, value):
        self.size = self.size + 1
        self.cards.append(Card(suit, value))


class Player():
    def __init__(self, money, hand):
        self.money = money