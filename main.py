from cmath import e
import random
from tkinter import E

# Let's give the info of the card's suits, ranks and values
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
values = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
          'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
points = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}
playing = True


# Game Objects:
class Card():
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.points = points[value]

    def to_string(self):
        return f"{self.value} of {self.suit}  ({self.points})"


class Hand():
    def __init__(self):
        self.size = 0
        self.cards = []  # list of  cards
        self.score = 0
        self.done_flag = False

    def add_card(self, card):
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

        #Player1Hand = Hand()
        #Player1Hand.add_Card(Card('Ace', 'Heart'))

    def contains(self, card):
        for c in self.cards:
            if card.value == c.value:
                return True
        return False


class Player():
    def __init__(self):
        self.hands = []

    def add_hand(self, hand):
        self.hands.append(hand)

    def delete_hand(self, hand):
        self.hands.remove(hand)

    def split_hand(self):
        if len(self.hands) == 1:
            if len(self.hands[0].cards) == 2:
                first_card = self.hands[0].cards[0]
                second_card = self.hands[0].cards[1]
                if first_card.points == second_card.points:
                    self.delete_hand(self.hands[0])
                    new_hand1 = Hand()
                    new_hand1.add_card(first_card)
                    self.add_hand(new_hand1)
                    new_hand2 = Hand()
                    new_hand2.add_card(second_card)
                    self.add_hand(new_hand2)
                else:
                    raise Exception(
                        "Can only split when 2 cards are even in points")
            else:
                raise Exception("Can only split when you have 2 cards")
        else:
            raise Exception("Can only split when you have a single hand")


class Dealer():
    def __init__(self, hand):
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

    def to_string(self):
        deck_comp = ''  # start with an empty string
        for card in self.deck:
            deck_comp += '\n '+card.__str__()  # add each Card object's print string
        return 'The deck has:' + deck_comp

    def shuffle(self):          # shuffle function will shuffle 52 card deck
        random.shuffle(self.deck)

    def deal(self):             # deal function will take one card from the deck
        single_card = self.deck.pop()
        return single_card


# Game Functions:
# function prompting the Player to Hit or Stand
def action(deck, hand):
    while True:
        x = input("Would you like to Hit or Stand? Enter 'h' or 's' ")

        if x[0].lower() == 'h':
            hit(deck, hand)
        elif x[0].lower() == 's':
            stand(hand)
        elif x[0].lower() == 'p':
            split(hand)
        else:
            print("Sorry, please try again.")
            continue
        break


def hit(deck, hand):
    hand.add_card(deck.deal())


def stand(hand):
    hand.done_flag = True


def split(player):
    try:
        player.split_hand()
    except Exception as e:
        print(e)


def double(deck, hand):
    hit(deck, hand)
    hand.done_flag = True


# functions to display cards
def show_dealer(dealer_hand):
    print(f"\nDealer's Hand: {dealer_hand.score}")
    for card in dealer_hand.cards:
        print(f"{card.to_string()}, ")


def show_dealer_hidden(dealer_hand):
    print("\nDealer's Hand: ")
    print(f"{dealer_hand.cards[0].to_string()}, <hidden>")


def show_player(player_hand):
    print(f"\nPlayer's Hand: {player_hand.score}")
    for card in player_hand.cards:
        print(f"{card.to_string()}, ")


# functions to handle end of game scenarios
def player_busts():
    print("Player busts!")


def player_wins():
    print("Player wins!")


def dealer_busts():
    print("Dealer busts!")


def dealer_wins():
    print("Dealer wins!")


def push():
    print("Dealer and Player tie! It's a push.")


def calculate_winner(dealer_hand, player_hand):
    if player_hand.score <= 21:

        # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
        while dealer_hand.score < 17:
            hit(deck, dealer_hand)

        # Show all cards
        show_dealer(dealer_hand)

        # Run different winning scenarios
        if dealer_hand.score > 21:
            dealer_busts()

        elif dealer_hand.score > player_hand.score:
            dealer_wins()

        elif dealer_hand.score < player_hand.score:
            player_wins()

        else:
            push()
    else:
        # If player's hand exceeds 21, run player_busts() and break out of loop
        player_busts()


# Game:
while True:
    # Print an opening statement
    print('Play a game of Blackjack!!')

    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    # drawing from 3 decks shuffled together
    deck.add_deck()
    deck.add_deck()

    Player1 = Player()
    Player1.add_hand(Hand())
    Dealer1 = Dealer(Hand())

    player_hand = Player1.hands[0]
    dealer_hand = Dealer1.hand

    player_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Show cards (but keep one dealer card hidden)
    show_dealer_hidden(dealer_hand)
    show_player(player_hand)

    while player_hand.done_flag is not True:

        # Prompt for Player to Hit or Stand
        action(deck, player_hand)

        # Show resulting hand
        show_player(player_hand)

    calculate_winner(dealer_hand, player_hand)

    # Ask to play again
    new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")

    if new_game[0].lower() == 'y':
        playing = True
        continue
    elif new_game[0].lower() == 't':

        testdeck = Deck()

        blackjack = Hand()
        blackjack.add_card(Card('Hearts', 'Ace'))
        blackjack.add_card(Card('Hearts', 'King'))

        fourteen = Hand()
        fourteen.add_card(Card('Hearts', 'Eight'))
        fourteen.add_card(Card('Hearts', 'Six'))

        nineteen = Hand()
        nineteen.add_card(Card('Hearts', 'Nine'))
        nineteen.add_card(Card('Hearts', 'Ten'))

        doubleace = Hand()
        doubleace.add_card(Card('Hearts', 'Ace'))
        doubleace.add_card(Card('Hearts', 'Ace'))

        print("Test Cases:")
        # Player gets blackjack
        testDealer = Dealer(nineteen)
        dealerhand = testDealer.hand
        testplayer = Player()
        testplayer.add_hand(blackjack)
        playerhand = testplayer.hands[0]
        show_player(playerhand)
        calculate_winner(dealerhand, playerhand)

        # Player and dealer both have blackjack
        testDealer = Dealer(blackjack)
        dealerhand = testDealer.hand
        testplayer = Player()
        testplayer.add_hand(blackjack)
        playerhand = testplayer.hands[0]
        show_player(playerhand)
        calculate_winner(dealerhand, playerhand)

        # Player busts - Dealer auto wins
        testDealer = Dealer(nineteen)
        dealerhand = testDealer.hand
        testplayer = Player()
        testplayer.add_hand(fourteen)
        playerhand = testplayer.hands[0]
        playerhand.add_card(Card('Hearts', 'Nine'))
        show_player(playerhand)
        calculate_winner(dealerhand, playerhand)

        # Player stands, Dealer wins
        testDealer = Dealer(nineteen)
        dealerhand = testDealer.hand
        testplayer = Player()
        testplayer.add_hand(fourteen)
        playerhand = testplayer.hands[0]
        show_player(playerhand)
        calculate_winner(dealerhand, playerhand)

        # Player stands, Dealer busts
        testDealer = Dealer(nineteen)
        dealerhand = testDealer.hand
        testplayer = Player()
        testplayer.add_hand(nineteen)
        playerhand = testplayer.hands[0]
        dealerhand.add_card(Card('Hearts', 'Nine'))
        show_player(playerhand)
        calculate_winner(dealerhand, playerhand)

    else:
        print("Thanks for playing!")
        break
