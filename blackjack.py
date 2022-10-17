from game_objects import *


# Game Functions:
# function prompting the Player to Hit or Stand
def action(deck: Deck, hand: Hand, player=None):
    while True:
        x = input("Would you like to Hit or Stand? Enter 'h' or 's' ")

        if x[0].lower() == 'h':
            hit(deck, hand)
        elif x[0].lower() == 's':
            stand(hand)
        elif x[0].lower() == 'p' and player is not None:
            split(player)
        else:
            print("Sorry, please try again.")
            continue
        break


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
    hit(deck, hand)
    hand.done_flag = True


# functions to display cards
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
    # Show Dealer's cards
    show_dealer(dealer_hand)
    if player_hand.score <= 21:
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

    while True:
        try:
            num_of_players = int(input('How many players?? '))
            break
        except ValueError:
            print("you must enter an integer")
            continue

    the_table = Table(num_of_players)

    the_dealer = the_table.players[0]
    the_players = the_table.players[1:]

    dealer_hand = the_dealer.hand

    # Deal first card to every player and the dealer
    for playernum in range(len(the_players)):
        the_players[playernum].hands[0].add_card(the_table.deck.deal())
    the_dealer.hand.add_card(the_table.deck.deal())
    # Deal second card to every player and the dealer
    for playernum in range(len(the_players)):
        the_players[playernum].hands[0].add_card(the_table.deck.deal())
    the_dealer.hand.add_card(the_table.deck.deal())

    # Show cards (but keep one dealer card hidden)
    for playernum in range(len(the_players)):
        player = the_players[playernum]
        for handnum in range(len(player.hands)):
            show_player(playernum, player.hands[handnum])
    show_dealer_hidden(dealer_hand)

    for playernum in range(len(the_players)):
        player = the_players[playernum]
        for handnum in range(len(player.hands)):
            hand = player.hands[handnum]
            while hand.done_flag is not True:
                # Prompt for Player to Hit or Stand
                action(the_table.deck, hand)
                # Show resulting hand
                show_player(playernum, hand)

    # Have Dealer play out its hand until reaching soft or hard 17
    while dealer_hand.score < 17:
        hit(the_table.deck, dealer_hand)

    for playernum in range(len(the_players)):
        for handnum in range(len(the_players[playernum].hands)):
            calculate_winner(
                dealer_hand, the_players[playernum].hands[handnum])

    # Ask to play again
    new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")

    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print("Thanks for playing!")
        break
