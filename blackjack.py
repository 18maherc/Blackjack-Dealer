from game_objects import *
from mainDetector import getCard
import game_functions as gf
from communication import Move
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, NumericProperty
from kivy.config import Config


move = Move()
Config.set('graphics', 'fullscreen', 1)
Builder.load_file('controller.kv')


# Declare all screens
class ScreenManager(ScreenManager):
    pass


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
    # This screen is to show Dealer output and winners/losers
    # Should also allow to play again or reset the game
    pass


class TestApp(App):
    # Bundling everything together
    playernum = NumericProperty(defaultvalue=1)

    def build(self):
        # Print an opening statement
        print("Play a game of Blackjack!!")
        # Create the screen manager
        self.sm = ScreenManager(transition=NoTransition())
        # Initialize the table
        self.the_table = None

        return self.sm

    def decrease_number(self):
        if self.playernum > 1:
            self.playernum -= 1

    def increase_number(self):
        if self.playernum < 3:
            self.playernum += 1

    def init_wagerscreen(self):
        wagerlayouts = []
        for i in range(self.playernum):
            wagerlayouts.append(PlayerWager(playernum=(i+1)))

        for layout in reversed(wagerlayouts):
            self.sm.ids.players.add_widget(layout)

    def init_table(self):
        if self.the_table is None:
            self.the_table = Table(self.playernum, self.sm)

            self.the_players = self.the_table.players
            self.the_dealer = self.the_table.dealer

        self.set_wagers()
        self.initial_deal()

    def set_wagers(self):
        # Set wagers
        for i in range(len(self.the_players)):
            set_wager = self.sm.ids.players.children[(
                len(self.the_players)-1)-i].wager
            if set_wager > self.the_players[i].wallet:
                set_wager = self.the_players[i].wallet
            self.the_players[i].wager = set_wager
            self.the_players[i].remove_credits(self.the_players[i].wager)

    def initial_deal(self):
        # Deal first card to every player and the dealer. Also set the wager
        for playernum in range(len(self.the_players)):
            # Draw a physical card
            move.draw(len(card_stack))
            the_card = getCard()
            # Represent the physical card digitally
            self.the_players[playernum].hands[0].add_card(the_card)
            # Place the card at its physical location after flipping
            move.place(the_card.coords)
        # Draw a physical card
        move.draw(len(card_stack))
        the_card = getCard()
        # Represent the physical card digitally
        self.the_dealer.hand.add_card(the_card)
        # Place the card at its physical location without flipping
        move.place(the_card.coords)

        # Deal second card to every player and the dealer
        for playernum in range(len(self.the_players)):
            move.draw(len(card_stack))
            the_card = getCard()
            self.the_players[playernum].hands[0].add_card(the_card)
            move.place(the_card.coords)
            self.show_player(playernum, self.the_players[playernum].hands[0])
        move.draw(len(card_stack))
        the_card = getCard()
        self.the_dealer.hand.add_card(the_card)
        move.place(the_card.coords)
        self.show_dealer_hidden(self.the_dealer.hand)

    def action(self, char, num):
        player = self.the_players[num-1]
        try:
            if player.split_flag is True:
                if player.hands[0].done_flag is not True:
                    gf.action(char[0], self.the_table.deck,
                              player.hands[0], player, move=move)
                    self.show_player(num-1, player.hands[0])
                    player.action_btns_state(True)
                elif player.hands[1].done_flag is not True:
                    gf.action(char[0], self.the_table.deck,
                              player.hands[1], player, move=move)
                    self.show_player(num-1, player.hands[1])
                    if player.hands[1].done_flag is True:
                        player.action_btns_state(False)
                        player.done_flag = True
                    else:
                        player.action_btns_state(True)
                        player.done_flag = False
                else:
                    print("Player has no hands to do action on")
                    # Check if we move on following possible final action
                    if player.hands[1].done_flag is True:
                        player.action_btns_state(False)
                        player.done_flag = True
                    else:
                        player.action_btns_state(True)
                        player.done_flag = False

            else:
                if player.hands[0].done_flag is not True:
                    gf.action(char[0], self.the_table.deck,
                              player.hands[0], player, move=move)
                    self.show_player(num-1, player.hands[0])
                    # Check if we move on following possible final action
                    if player.hands[0].done_flag is True:
                        player.action_btns_state(False)
                        player.done_flag = True
                    else:
                        player.action_btns_state(True)
                        player.done_flag = False

                else:
                    print("Player has no hands to do action on")
                    # Check if we move on following possible final action
                    if player.hands[0].done_flag is True:
                        player.action_btns_state(False)
                        player.done_flag = True
                    else:
                        player.action_btns_state(True)
                        player.done_flag = False

        except Exception as e:
            print(e)

    def insurance(self, player):
        gf.insurance(player)

    def show_dealer(self, hand):
        gf.show_dealer(hand)

    def show_dealer_hidden(self, hand):
        gf.show_dealer_hidden(hand)

    def show_player(self, player_num, player_hand):
        gf.show_player(player_num, player_hand)

    def next_player(self):
        current = self.sm.current
        if current[:6] == 'player':
            num = int(current[6])
            if num == len(self.the_players):
                for i in range(len(self.the_players)):
                    if self.the_players[i].done_flag is not True:
                        return
                self.calculate_winners()
                self.sm.current = 'endgamescreen'
            else:
                self.sm.current = f'player{num+1}'

    def prev_player(self):
        current = self.sm.current
        if current[:6] == 'player':
            num = int(current[6])
            if num > 1:
                self.sm.current = f'player{num-1}'

    def calculate_winners(self):
        # Complete the Dealer's hand
        while self.the_dealer.hand.score < 17 and self.the_dealer.hand.score != 21:
            # Use the hit function from game_functions
            gf.action('h', self.the_table.deck,
                      self.the_dealer.hand, player=None, move=move)

        self.show_dealer(self.the_dealer.hand)
        self.sm.ids.dealerhand.add_widget(self.the_dealer.hand)

        # Calculate the winner from all hands for all players
        playerresults = []
        for player in self.the_players:
            for handnum in range(len(player.hands)):
                result = gf.calculate_winner(self.the_dealer.hand,
                                             player.hands[handnum], player)
                print(
                    f"Player {player.player_num} you now have {player.wallet} credits.")
                # self.sm.ids.playerresults.add_widget(PlayerResult(
                #    playernum=player.player_num, result=result, credits=player.wallet), index=-len(self.sm.ids.playerresults.children))
                playerresults.append(PlayerResult(
                    playernum=player.player_num, result=result, credits=player.wallet))
        # let's do this displaying in the most inefficient way possible just to not risk breaking something
        for result in reversed(playerresults):
            self.sm.ids.playerresults.add_widget(result)

    def new_game(self):
        # -- End of game sequence --
        # Replace the dealer's hand
        self.the_dealer.hand = DealerHand()
        self.dealer_hand = self.the_dealer.hand
        # Reset the players
        for playernum in range(len(self.the_players)):
            self.the_players[playernum].clear()
        # Physically collect all cards
        move.discard(card_stack)
        # Reset the card stack
        card_stack.clear()
        # Clear the Dealer's hand widget
        self.sm.ids.dealerhand.clear_widgets(self.sm.ids.dealerhand.children)
        # Add the default label back into the Dealer's hand widget
        self.sm.ids.dealerhand.add_widget(
            Label(text='Dealer Hand:', size_hint_x=0.2))
        # Clear the Player results widget(s)
        self.sm.ids.playerresults.clear_widgets(
            self.sm.ids.playerresults.children)
        # Reenable some disabled buttons
        self.sm.ids.go_button.disabled = False
        self.sm.ids.new_game_button.disabled = False


if __name__ == '__main__':
    TestApp().run()
