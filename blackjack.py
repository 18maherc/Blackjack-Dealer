# from game_objects import *
import game_functions as gf
from communication import Move
from mainDetector import getCard
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
import math
import random


# Let's give the info of the card's suits, ranks and values
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
values = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
          'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
points = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}
card_stack = []

# move = Move()
Builder.load_file('controller.kv')


# ---- Game: ----
while True:
    # TODO: Display a splash screen with a start button

    # TODO: Display a player number selection screen
    break

    # Play the game
    while True:

        # Take bets for all players
        for playernum in range(len(the_players)):
            player = the_players[playernum]
            while True:
                try:
                    # Prompt to deposit if insufficient funds
                    if player.wallet < 1:
                        while True:
                            try:
                                deposit = int(
                                    input(f"Player {playernum+1}, input a number of credits to deposit: "))
                                player.add_credits(deposit)
                                break
                            except ValueError:
                                print("You must enter an integer")
                                continue

                    # Prompt for wager
                    bet_amount = int(input(
                        f"Player {playernum+1}, you have {player.wallet} credits, enter your wager: "))

                    # Handle wager input
                    if bet_amount > 0:
                        # Set wager and remove credits if sufficient funds
                        if bet_amount <= player.wallet:
                            player.hands[0].wager = bet_amount
                            player.remove_credits(bet_amount)
                        else:
                            raise Exception(
                                "Cannot bet more than your current wallet")
                    else:
                        raise Exception(
                            "Must bet a minimum of 1 credits to play")
                    break

                except Exception as e:
                    print(e)
                    continue

        # Deal first card to every player and the dealer. Also set the wager
        for playernum in range(len(the_players)):
            # Draw a physical card
            move.draw(len(card_stack))
            # TODO: Read the physical card in
            the_card = getCard()
            # Represent the physical card digitally
            the_players[playernum].hands[0].add_card(the_card)
            # Place the card at its physical location after flipping
            move.place(the_card.coords)
        # Draw a physical card
        move.draw(len(card_stack))
        # TODO: Read the physical card in
        the_card = getCard()
        # Represent the physical card digitally
        the_dealer.hand.add_card(the_card)
        # Place the card at its physical location without flipping
        move.place(the_card.coords, dealer=True)

        # Deal second card to every player and the dealer
        for playernum in range(len(the_players)):
            move.draw(len(card_stack))
            the_card = getCard()
            the_players[playernum].hands[0].add_card(the_card)
            move.place(the_card.coords)
        move.draw(len(card_stack))
        the_card = getCard()
        the_dealer.hand.add_card(the_card)
        move.place(the_card.coords)

        # Show Dealer's initial hand with one card shown
        show_dealer_hidden(dealer_hand)

        # Ask for each player's actions in the game
        for playernum in range(len(the_players)):
            player = the_players[playernum]
            # Check if dealer is showing Ace
            if dealer_hand.cards[0].value == 'Ace':
                # Ask players if they want to place insurance bet
                while True:
                    try:
                        ins_choice = input(
                            "Would you like to place an insurance wager? (y/n) ")
                        if ins_choice[0].lower() == 'y':
                            insurance(player)
                        break
                    except ValueError:
                        print("You must enter y/n")
                    except Exception as e:
                        print(e)
                        break
            hand = player.hands[0]
            # Continuously ask Player for action until they are finished
            while hand.done_flag is not True and player.split_flag is not True:
                # Show current hand
                show_player(playernum, hand)
                # Prompt for Player to Hit or Stand
                action(the_table.deck, hand, player, move)
            # Show the final state of the hand
            show_player(playernum, hand)

            # Check if the Player split their initial hand
            if player.split_flag:
                # Player split their hand so let's do that process again
                for handnum in range(len(player.hands)):
                    hand = player.hands[handnum]
                    hand_split = False
                    while hand.done_flag is not True and hand_split is not True:
                        # Show current hand
                        show_player(playernum, hand)
                        # Prompt for Player to Hit or Stand
                        # TODO: pass in 'move'
                        action(the_table.deck, hand, player, move)
                    # Show the final state of the hand
                    show_player(playernum, hand)

        # Get rid of surrendered hands and refund partial wagers
        # TODO: figure out if we want to just do this at the end (and have a surrender flag check for winnings)
        surrender_coords = []
        for playernum in range(len(the_players)):
            player = the_players[playernum]
            for hand in player.hands:
                if hand.surrender_flag == True:
                    for card in hand:
                        surrender_coords.append(card.coords)
                    player.delete_hand(hand)
                    player.add_credits(0.5*hand.wager)
        move.discard(surrender_coords)

        # Have Dealer play out its hand until reaching soft or hard 17
        while dealer_hand.score < 17 and dealer_hand.score != 21:
            # Use the hit function from game_functions
            hit(the_table.deck, dealer_hand, move)
            # TODO: add motor functionality here --------------------------

        # Show Dealer's cards
        show_dealer(dealer_hand)

        # Handle insurance bets
        if dealer_hand.score == 21 and dealer_hand.size == 2:
            for player in the_players:
                if player.insurance_flag is True:
                    player.add_credits(3*0.5*player.hands[0].wager)

        # Calculate any winning hands as necessary and show final balance
        for playernum in range(len(the_players)):
            player = the_players[playernum]
            for handnum in range(len(player.hands)):
                calculate_winner(dealer_hand, player.hands[handnum], player)
                print(
                    f"Player {playernum+1} you now have {player.wallet} credits.")

        # -- End of game sequence --
        # Replace the dealer's hand
        the_dealer.hand = Hand()
        dealer_hand = the_dealer.hand
        # Reset the players
        for playernum in range(len(the_players)):
            the_players[playernum].clear()
        # Physically collect all cards
        move.discard(card_stack)
        card_stack = []

        # Ask to play again
        new_game = input(
            "Would you like to play another game? Enter 'y' or 'n' ")

        if new_game[0].lower() == 'y':
            continue
        else:
            print("Thanks for playing!")
            break

    # TODO: Handle removal/addition of players frorm the table
    # (Will require adjusting base coords)

    close_game = input(
        "Would you like to close the game (otherwise resets table)? (y/n) ")
    if close_game[0].lower() == 'y':
        break


# Declare all screens
class SplashScreen(Screen):
    # Intro screen with logo and start button
    pass


class StartGameScreen(Screen):
    # This screen should set number of players
    pass


class WagerScreen(Screen):
    # This screen should set the wagers for each player before initializing them
    pass


class EndGameScreen(Screen):
    # This screen is to
    pass


class ScreenManager(ScreenManager):
    pass


class Card():
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.points = points[value]
        self.coords = [250, 80]
        # ^ TODO find out coordinate stuff here ^
        self.filename = f"{self.value}_{self.suit}.png"

    def to_string(self) -> str:
        return f"{self.value} of {self.suit}  ({self.points})"


class Hand(BoxLayout):
    wager = NumericProperty(defaultvalue=1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.length = 0
        self.cards = []  # list of  cards
        self.score = 0
        self.done_flag = False
        self.wager = 1
        self.surrender_flag = False
        self.base_coords = [250, 80]
        # ^ TODO find out coordinate stuff here ^

    def add_card(self, card: Card):
        card.coords[0] = self.base_coords[0] - 25*(self.length)
        # ^ TODO find out coordinate stuff here ^
        card.coords[1] = self.base_coords[1]
        # ^ TODO find out coordinate stuff here ^
        self.length += 1
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
        # Show the card to the player
        self.add_widget(Image(source=f"card_images/{card.filename}"))


class DealerHand(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.length = 0
        self.cards = []  # list of  cards
        self.score = 0
        self.done_flag = False
        self.base_coords = [0, 165]
        # ^ TODO find out coordinate stuff here ^

    def add_card(self, card: Card):
        card.coords[0] = self.base_coords[0]
        # ^ TODO find out coordinate stuff here ^
        card.coords[1] = self.base_coords[1] + 25*(self.length)
        # ^ TODO find out coordinate stuff here ^
        self.length += 1
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


class Player(Screen):
    player_num = NumericProperty(defaultvalue=1)
    wallet = NumericProperty(defaultvalue=10)
    hands = ObjectProperty(defaultvalue=[])
    wager = NumericProperty(defaultvalue=1)
    # Each player will have their own instance of this

    def __init__(self, name, player_num, **kwargs):
        super().__init__(**kwargs)
        self.wallet = 10
        self.wager = 1
        self.split_flag = False
        self.insurance_flag = False
        self.name = name
        self.player_num = player_num
        self.base_coords = [250, 80+110*(self.player_num-1)]
        self.hands = []
        self.add_hand(Hand(wager=self.wager))

    def add_hand(self, hand: Hand):
        # Set the base coordinates of the new hand
        hand.base_coords[0] = self.base_coords[0]
        hand.base_coords[1] = self.base_coords[1] + 25*len(self.hands)
        # ^ TODO find out coordinate stuff here ^
        # Add the new hand to the player
        self.hands.append(hand)
        self.ids.hand_layout.add_widget(hand)

    def delete_hand(self, hand: Hand):
        for card in hand.cards:
            card_stack.remove(card.coords)
        self.remove_widget(hand)
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

    pass


class PlayerWager(BoxLayout):
    playernum = NumericProperty()
    wager = NumericProperty(defaultvalue=1)

    def decrease_wager(self):
        if self.wager > 0:
            self.wager -= 1
    pass


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
    def __init__(self, player_count: int, screen_manager: ScreenManager):
        # Initialize our collection of players
        self.players = []
        # Initialize our Dealer
        self.dealer = Dealer(DealerHand())

        # Add x number of players to the game
        for i in range(player_count):
            new_player = Player(
                name=f"player{i+1}", player_num=(i+1))
            self.players.append(new_player)
            screen_manager.add_widget(new_player)

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


class TestApp(App):
    # Bundling everything together
    playernum = NumericProperty(defaultvalue=1)

    def build(self):
        # Print an opening statement
        print("Play a game of Blackjack!!")
        # Create the screen manager
        self.sm = ScreenManager(transition=NoTransition())

        return self.sm

    def decrease_number(self):
        if self.playernum > 1:
            self.playernum -= 1

    def increase_number(self):
        if self.playernum < 3:
            self.playernum += 1

    def init_wagerscreen(self):
        for i in range(self.playernum):
            player_layout = PlayerWager(playernum=(i+1))
            self.sm.ids.players.add_widget(player_layout)

    def init_table(self):
        self.the_table = Table(self.playernum, self.sm)

        self.the_players = self.the_table.players
        self.the_dealer = self.the_table.dealer

        # Set wagers
        for i in range(len(self.the_players)):
            self.the_players[i].wager = self.sm.ids.players.children[(
                len(self.the_players)-1)-i].wager
            self.the_players[i].remove_credits(self.the_players[i].wager)

        # Deal first card to every player and the dealer. Also set the wager
        for playernum in range(len(self.the_players)):
            # Draw a physical card
            # move.draw(len(card_stack))
            # TODO: Read the physical card in
            the_card = self.the_table.deck.deal()
            # Represent the physical card digitally
            self.the_players[playernum].hands[0].add_card(the_card)
            # Place the card at its physical location after flipping
            # move.place(the_card.coords)
        # Draw a physical card
        # move.draw(len(card_stack))
        # TODO: Read the physical card in
        the_card = self.the_table.deck.deal()
        # Represent the physical card digitally
        self.the_dealer.hand.add_card(the_card)
        # Place the card at its physical location without flipping
        # move.place(the_card.coords, dealer=True)

        # Deal second card to every player and the dealer
        for playernum in range(len(self.the_players)):
            # move.draw(len(card_stack))
            the_card = self.the_table.deck.deal()
            self.the_players[playernum].hands[0].add_card(the_card)
            # move.place(the_card.coords)
            self.show_player(playernum, self.the_players[playernum].hands[0])
        # move.draw(len(card_stack))
        self.the_table.deck.deal()
        self.the_dealer.hand.add_card(the_card)
        # move.place(the_card.coords)
        self.show_dealer_hidden(self.the_dealer.hand)

    def action(self, char, num):
        player = self.the_players[num-1]
        try:
            if player.split_flag is True:
                if player.hands[0].done_flag is not True:
                    gf.action(char[0], self.the_table.deck,
                              player.hands[0], player, move=None)
                    self.show_player(num, player.hands[0])
                elif player.hands[1].done_flag is not True:
                    gf.action(char[0], self.the_table.deck,
                              player.hands[1], player, move=None)
                    self.show_player(num, player.hands[1])
                else:
                    print(f"Player {num} has no hands to do action on")
                    self.sm.current = f'player{num+1}'
            else:
                if player.hands[0].done_flag is not True:
                    gf.action(char[0], self.the_table.deck,
                              player.hands[0], player, move=None)
                    self.show_player(num, player.hands[0])
                else:
                    print(f"Player {num} has no hands to do action on")
                    self.sm.current = f'player{num+1}'
        except Exception as e:
            print(e)

    def insurance(self, player):
        gf.insurance(player)

    def show_dealer(self, hand):
        gf.show_dealer(hand)

    def show_dealer_hidden(self, hand):
        gf.show_dealer_hidden(hand)

    def show_player(self, player_num, player_hand):
        gf.show_player(player_num-1, player_hand)


if __name__ == '__main__':
    TestApp().run()
