from game_objects import *


# ---- Game Functions: ----
# function prompting the Player to Hit or Stand
def action(deck: Deck, hand: Hand, player=None):
    while True:
        x = input("Hit(h) Stand(s) Split(p) Double(d) Surrender(l)? ")
        try:
            if x[0].lower() == 'h':
                hit(deck, hand)
            elif x[0].lower() == 's':
                stand(hand)
            elif x[0].lower() == 'p' and player is not None:
                split(deck, player)
            elif x[0].lower() == 'd':
                double(deck, hand, player)
            elif x[0].lower() == 'l':
                surrender(hand)
            else:
                raise Exception("Invalid action. Please try again")
            break
        except Exception as e:
            print(e)


def hit(deck: Deck, hand: Hand):
    hand.add_card(deck.deal())


def stand(hand: Hand):
    hand.done_flag = True


def split(deck: Deck, player: Player):
    player.split_hand()
    player.hands[0].add_card(deck.deal())
    player.hands[1].add_card(deck.deal())


def double(deck: Deck, hand: Hand, player: Player):
    if len(hand.cards):
        if player.wallet >= hand.wager:
            player.remove_credits(hand.wager)
            hit(deck, hand)
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
                    # TODO: normally should compensate here for dealer 2 card 21, but that's what insurance should cover
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

    while True:
        # Take bets for all players (will allow you to bet 0 for now)
        for playernum in range(len(the_players)):
            player = the_players[playernum]
            while True:
                try:
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
                    bet_amount = int(input(
                        f"Player {playernum+1}, you have {player.wallet} credits, enter your wager: "))
                    if bet_amount > 0:
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
            the_players[playernum].hands[0].add_card(the_table.deck.deal())
        the_dealer.hand.add_card(the_table.deck.deal())
        # Deal second card to every player and the dealer
        for playernum in range(len(the_players)):
            the_players[playernum].hands[0].add_card(the_table.deck.deal())
        the_dealer.hand.add_card(the_table.deck.deal())

        show_dealer_hidden(dealer_hand)

        # Ask for each player's actions in the game
        for playernum in range(len(the_players)):
            player = the_players[playernum]
            if dealer_hand.cards[0].value == 'Ace':
                while True:
                    try:
                        # insurance?? y/n
                        break
                    except ValueError:
                        print("You must enter y/n")
            hand = player.hands[0]
            while hand.done_flag is not True and player.split_flag is not True:
                # Show current hand
                show_player(playernum, hand)
                # Prompt for Player to Hit or Stand
                action(the_table.deck, hand, player)
            # Show the final state of the hand
            show_player(playernum, hand)

            if player.split_flag:
                # Player split their hand so let's do that process again
                for handnum in range(len(player.hands)):
                    hand = player.hands[handnum]
                    hand_split = False
                    while hand.done_flag is not True and hand_split is not True:
                        # Show current hand
                        show_player(playernum, hand)
                        # Prompt for Player to Hit or Stand
                        action(the_table.deck, hand, player)
                    # Show the final state of the hand
                    show_player(playernum, hand)

        # Get rid of surrendered hands and refund partial wagers
        for playernum in range(len(the_players)):
            player = the_players[playernum]
            for hand in player.hands:
                if hand.surrender_flag == True:
                    player.delete_hand(hand)
                    player.add_credits(0.5*hand.wager)

        # Have Dealer play out its hand until reaching soft or hard 17
        while dealer_hand.score < 17 and dealer_hand.score != 21:
            hit(the_table.deck, dealer_hand)

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

        # Ask to play again
        new_game = input(
            "Would you like to play another game? Enter 'y' or 'n' ")

        if new_game[0].lower() == 'y':
            the_dealer.hand = Hand()
            dealer_hand = the_dealer.hand
            for playernum in range(len(the_players)):
                the_players[playernum].clear()
            continue
        else:
            print("Thanks for playing!")
            break

    close_game = input("Would you like to close the game? (y/n) ")
    if close_game[0].lower() == 'y':
        break
