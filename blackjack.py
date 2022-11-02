from game_objects import *
from game_functions import *

# ---- Game: ----
while True:
    # Print an opening statement
    print("Play a game of Blackjack!!")

    # Get the number of players for the game
    while True:
        try:
            num_of_players = int(input("How many players?? "))
            break
        except ValueError:
            print("You must enter an integer")
            continue

    # Initialize our table
    the_table = Table(num_of_players)
    the_dealer = the_table.dealer
    the_players = the_table.players
    dealer_hand = the_dealer.hand

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
            the_players[playernum].hands[0].add_card(the_table.deck.deal())
        the_dealer.hand.add_card(the_table.deck.deal())
        # Deal second card to every player and the dealer
        for playernum in range(len(the_players)):
            the_players[playernum].hands[0].add_card(the_table.deck.deal())
        the_dealer.hand.add_card(the_table.deck.deal())

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
                action(the_table.deck, hand, player)
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
