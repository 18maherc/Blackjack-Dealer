import blackjack
from communication import Move
import mainDetector
move = Move()


# ---- Game Functions: ----

# function prompting the Player to Hit or Stand
def action(x: str, deck: blackjack.Deck, hand: blackjack.Hand, player: blackjack.Player, move: Move):
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
    except Exception as e:
        print(e)


def hit(deck: blackjack.Deck, hand: blackjack.Hand, move: Move):
    move.draw(len(blackjack.card_stack))
    hand.add_card(mainDetector.getCard())
    move.place(hand.cards[-1].coords)


def stand(hand: blackjack.Hand):
    hand.done_flag = True


def split(deck: blackjack.Deck, player: blackjack.Player, move: Move):
    player.split_hand(move)
    hit(deck, player.hands[0], move)
    hit(deck, player.hands[1], move)


def double(deck: blackjack.Deck, hand: blackjack.Hand, player: blackjack.Player, move: Move):
    if len(hand.cards) == 2:
        if player.wallet >= player.wager:
            player.remove_credits(player.wager)
            hit(deck, hand, move)
            player.wager *= 2
            hand.done_flag = True
        else:
            raise Exception("Do not have enough credits to double down")
    else:
        raise Exception("Can only double down with a 2 card hand")


def surrender(hand: blackjack.Hand):
    if len(hand.cards) == 2:
        print("Player surrenders this hand")
        hand.surrender_flag = True
        hand.done_flag = True
    else:
        raise Exception("Can only surrender on initial hand")


def insurance(player: blackjack.Player):
    the_wager = player.hands[0].wager
    if player.wallet >= 0.5*the_wager:
        player.insurance_flag = True
        player.remove_credits(0.5*the_wager)
    else:
        raise Exception("Do not have enough credits to place insurance bet")


# --- functions to display cards ---
def show_dealer(dealer_hand: blackjack.Hand):
    print(f"\nDealer's Hand: {dealer_hand.score}")
    for card in dealer_hand.cards:
        print(f"{card.to_string()}, ")


def show_dealer_hidden(dealer_hand: blackjack.Hand):
    print("\nDealer's Hand: ")
    print(f"{dealer_hand.cards[0].to_string()}, <hidden>")


def show_player(player_num: int, player_hand: blackjack.Hand):
    """Show the player's cards

    Args:
        player_num (int): A zero-indexed identifier from the list of players
        player_hand (Hand): The player's hand
    """
    print(f"\nPlayer {player_num+1}'s Hand: {player_hand.score}")
    for card in player_hand.cards:
        print(f"{card.to_string()}, ")


# --- functions to handle end of game scenarios ---
def player_busts(player: blackjack.Player) -> str:
    print("Player busts!")
    player.add_credits(0)
    return 'lose'


def player_wins(player: blackjack.Player) -> str:
    print("Player wins!")
    player.add_credits(2*player.wager)
    return 'win'


def player_blackjack(player: blackjack.Player) -> str:
    print("Player won with blackjack!")
    player.add_credits(2.5*player.wager)
    return 'win'


def dealer_busts(player: blackjack.Player) -> str:
    print("Dealer busts!")
    player.add_credits(2*player.wager)
    return 'win'


def dealer_wins(player: blackjack.Player) -> str:
    print("Dealer wins!")
    player.add_credits(0)
    return 'lose'


def push(player: blackjack.Player) -> str:
    print("Dealer and Player tie! It's a push.")
    player.add_credits(player.wager)
    return 'push'


def calculate_winner(dealer_hand: blackjack.Hand, player_hand: blackjack.Hand, player: blackjack.Player) -> str:
    # Player hit 21
    if player_hand.score == 21:
        if player_hand.size == 2:
            if dealer_hand.score == 21:
                if dealer_hand.size == 2:
                    result = push(player)
                else:
                    result = player_blackjack(player)
            else:
                result = player_blackjack(player)
        else:
            if dealer_hand.score == 21:
                if dealer_hand.size == 2:
                    result = dealer_wins(player)
                else:
                    result = push(player)
            else:
                result = player_wins(player)
    # Player stayed under 21
    elif player_hand.score < 21:
        # Dealer goes over and Player is under
        if dealer_hand.score > 21:
            result = dealer_busts(player)
        # Dealer and Player are both under but dealer is higher
        elif dealer_hand.score > player_hand.score:
            result = dealer_wins(player)
        # Dealer and Player are both under but player is higher
        elif dealer_hand.score < player_hand.score:
            result = player_wins(player)
        # Dealer and Player are tied
        else:
            result = push(player)
    # Player busted. A loss no matter Dealer's cards
    else:
        result = player_busts(player)

    return result
