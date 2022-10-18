from game_objects import *


# ---- Game Functions: ----
# function prompting the Player to Hit or Stand
def action(deck: Deck, hand: Hand, player=None):
    while True:
        x = input("Hit(h) Stand(s) Split(p) Double(d)? ")

        try:
            if x[0].lower() == 'h':
                hit(deck, hand)
            elif x[0].lower() == 's':
                stand(hand)
            elif x[0].lower() == 'p' and player is not None:
                split(player)
            elif x[0].lower() == 'd':
                double(deck, hand)
            break
        except Exception:
            print("Invalid action. Please try again")


def hit(deck: Deck, hand: Hand):
    hand.add_card(deck.deal())


def stand(hand: Hand):
    hand.done_flag = True


def split(player: Player):
    try:
        player.split_hand()
    except Exception as e:
        print(e)


def double(deck: Deck, hand: Hand):
    try:
        if len(hand.cards):
            hit(deck, hand)
            hand.wager *= 2
            hand.done_flag = True
        else:
            raise Exception("Can only double down with a 2 card hand")
    except Exception as e:
        print(e)


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


def player_wins(player: Player):
    print("Player wins!")
    player.add_credits(2*player.betamt)


def player_blackjack(player: Player):
    print("Player won with blackjack!")
    player.add_credits(2.5*player.betamt)


def dealer_busts(player: Player):
    print("Dealer busts!")
    player.add_credits(2*player.betamt)


def dealer_wins(player: Player):
    print("Dealer wins!")
    player.add_credits(0)


def push(player: Player):
    print("Dealer and Player tie! It's a push.")
    player.add_credits(player.betamt)


def calculate_winner(dealer_hand: Hand, player_hand: Hand, player: Player):
    # Player hit 21
    if player_hand.score == 21:
        # Dealer wins with less cards
        if player_hand.size > dealer_hand.size:
            dealer_wins(player)
        # Player wins with less cards
        elif player_hand.size < dealer_hand.size:
            if player_hand.size == 2:
                player_blackjack(player)
            else:
                player_wins(player)
        # Player and Dealer tie with equal cards
        else:
            push(player)
    # Player stayed under 21
    elif player_hand.score < 21:
        # Dealer goes over and Player is under
        if dealer_hand.score > 21:
            dealer_busts(player)
        # Dealer and Player are both under but dealer is higher
        elif dealer_hand.score > player_hand.score:
            dealer_wins(player)
        # Dealer and Player are both under but player is higher
        elif dealer_hand.score < player_hand.score:
            player_wins(player)
        # Dealer and Player are tied
        else:
            push(player)
    # Player busted. A loss no matter Dealer's cards
    else:
        player_busts(player)


# ---- Game: ----
while True:
    # Print an opening statement
    print("Play a game of Blackjack!!")

    while True:
        try:
            num_of_players = int(input("How many players?? "))
            break
        except ValueError:
            print("You must enter an integer")
            continue

    the_table = Table(num_of_players)

    the_dealer = the_table.dealer
    the_players = the_table.players

    dealer_hand = the_dealer.hand

    # Take bets for all players (will allow you to bet 0 for now)
    for playernum in range(len(the_players)):
        player = the_players[playernum]
        while True:
            try:
                bet_amount = int(
                    input(f"Player {playernum+1}, you have {player.wallet} credits, enter your wager: "))
                player.set_bet_amt(bet_amount)
                break
            except Exception as e:
                print(e)
                continue

    # Set wagers for each players' initial hand
    for playernum in range(len(the_players)):
        player = the_players[playernum]
        player.hands[0].wager = player.betamt
        player.remove_credits(player.betamt)
    # Deal first card to every player and the dealer. Also set the wager
    for playernum in range(len(the_players)):
        the_players[playernum].hands[0].add_card(the_table.deck.deal())
    the_dealer.hand.add_card(the_table.deck.deal())
    # Deal second card to every player and the dealer
    for playernum in range(len(the_players)):
        the_players[playernum].hands[0].add_card(the_table.deck.deal())
    the_dealer.hand.add_card(the_table.deck.deal())

    show_dealer_hidden(dealer_hand)

    for playernum in range(len(the_players)):
        player = the_players[playernum]
        for handnum in range(len(player.hands)):
            hand = player.hands[handnum]
            while hand.done_flag is not True:
                # Show current hand
                show_player(playernum, hand)
                # Prompt for Player to Hit or Stand
                action(the_table.deck, hand, player)
            # Show the final state of the hand
            show_player(playernum, hand)

    # Have Dealer play out its hand until reaching soft or hard 17
    while dealer_hand.score < 17:
        hit(the_table.deck, dealer_hand)

    # Show Dealer's cards
    show_dealer(dealer_hand)

    # Show cards (but keep one dealer card hidden)
    # for playernum in range(len(the_players)):
    #    player = the_players[playernum]
    #    for handnum in range(len(player.hands)):
    #        show_player(playernum, player.hands[handnum])

    for playernum in range(len(the_players)):
        player = the_players[playernum]
        for handnum in range(len(player.hands)):
            calculate_winner(dealer_hand, player.hands[handnum], player)
            print(
                f"Player {playernum+1} you now have {player.wallet} credits.")

    # Ask to play again
    new_game = input("Would you like to play another game? Enter 'y' or 'n' ")

    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print("Thanks for playing!")
        break
