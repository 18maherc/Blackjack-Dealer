from game_objects import *
from communication import Move
#from mainDetector import getCard


# ---- Game Functions: ----

# function prompting the Player to Hit or Stand
def action(x: str, deck: Deck, hand: Hand, player: Player, move: Move):
    while True:
        try:
            if x[0].lower() == 'h':
                hit(deck, hand, move)
            elif x[0].lower() == 's':
                stand(hand)
            elif x[0].lower() == 'p' and player is not None:
                split(deck, player, move)
            elif x[0].lower() == 'd':
                double(deck, hand, player, move)
            elif x[0].lower() == 'l':
                surrender(hand)
            else:
                raise Exception("Invalid action. Please try again")
            break
        except Exception as e:
            print(e)


def hit(deck: Deck, hand: Hand, move: Move):
    # TODO: move.draw(len(card_stack))
    # TODO: hand.add_card(getCard())
    hand.add_card(deck.deal())
    # TODO: move.place(hand.cards[-1].coords)


def stand(hand: Hand):
    hand.done_flag = True


def split(deck: Deck, player: Player, move: Move):
    player.split_hand()
    hit(deck, player.hands[0], move)
    hit(deck, player.hands[1], move)
    # player.hands[0].add_card(deck.deal())
    # player.hands[1].add_card(deck.deal())


def double(deck: Deck, hand: Hand, player: Player, move: Move):
    if len(hand.cards) == 2:
        if player.wallet >= hand.wager:
            player.remove_credits(hand.wager)
            hit(deck, hand, move)
            hand.wager *= 2
            hand.done_flag = True
        else:
            raise Exception("Do not have enough credits to double down")
    else:
        raise Exception("Can only double down with a 2 card hand")


def surrender(hand: Hand):
    if len(hand.cards) == 2:
        print("Player surrenders this hand")
        hand.surrender_flag = True
        hand.done_flag = True
    else:
        raise Exception("Can only surrender on initial hand")


def insurance(player: Player):
    the_wager = player.hands[0].wager
    if player.wallet >= 0.5*the_wager:
        player.insurance_flag = True
        player.remove_credits(0.5*the_wager)
    else:
        raise Exception("Do not have enough credits to place insurance bet")


# --- functions to display cards ---
def show_dealer(dealer_hand: Hand):
    print(f"\nDealer's Hand: {dealer_hand.score}")
    for card in dealer_hand.cards:
        print(f"{card.to_string()}, ")


def show_dealer_hidden(dealer_hand: Hand):
    print("\nDealer's Hand: ")
    print(f"{dealer_hand.cards[0].to_string()}, <hidden>")


def show_player(player_num: int, player_hand: Hand):
    """Show the player's cards

    Args:
        player_num (int): A zero-indexed identifier from the list of players
        player_hand (Hand): The player's hand
    """
    print(f"\nPlayer {player_num+1}'s Hand: {player_hand.score}")
    for card in player_hand.cards:
        print(f"{card.to_string()}, ")


# --- functions to handle end of game scenarios ---
def player_busts(player: Player):
    print("Player busts!")
    player.add_credits(0)


def player_wins(player: Player, hand: Hand):
    print("Player wins!")
    player.add_credits(2*hand.wager)


def player_blackjack(player: Player, hand: Hand):
    print("Player won with blackjack!")
    player.add_credits(2.5*hand.wager)


def dealer_busts(player: Player, hand: Hand):
    print("Dealer busts!")
    player.add_credits(2*hand.wager)


def dealer_wins(player: Player):
    print("Dealer wins!")
    player.add_credits(0)


def push(player: Player, hand: Hand):
    print("Dealer and Player tie! It's a push.")
    player.add_credits(hand.wager)


def calculate_winner(dealer_hand: Hand, player_hand: Hand, player: Player):
    # Player hit 21
    if player_hand.score == 21:
        if player_hand.size == 2:
            if dealer_hand.score == 21:
                if dealer_hand.size == 2:
                    push(player, player_hand)
                else:
                    player_blackjack(player, player_hand)
            else:
                player_blackjack(player, player_hand)
        else:
            if dealer_hand.score == 21:
                if dealer_hand.size == 2:
                    dealer_wins(player)
                else:
                    push(player, player_hand)
            else:
                player_wins(player, player_hand)
    # Player stayed under 21
    elif player_hand.score < 21:
        # Dealer goes over and Player is under
        if dealer_hand.score > 21:
            dealer_busts(player, player_hand)
        # Dealer and Player are both under but dealer is higher
        elif dealer_hand.score > player_hand.score:
            dealer_wins(player)
        # Dealer and Player are both under but player is higher
        elif dealer_hand.score < player_hand.score:
            player_wins(player, player_hand)
        # Dealer and Player are tied
        else:
            push(player, player_hand)
    # Player busted. A loss no matter Dealer's cards
    else:
        player_busts(player)
