from game_objects import *
import blackjack


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
blackjack.show_player(playerhand)
blackjack.calculate_winner(dealerhand, playerhand)

# Player and dealer both have blackjack
testDealer = Dealer(blackjack)
dealerhand = testDealer.hand
testplayer = Player()
testplayer.add_hand(blackjack)
playerhand = testplayer.hands[0]
blackjack.show_player(playerhand)
blackjack.calculate_winner(dealerhand, playerhand)

# Player busts - Dealer auto wins
testDealer = Dealer(nineteen)
dealerhand = testDealer.hand
testplayer = Player()
testplayer.add_hand(fourteen)
playerhand = testplayer.hands[0]
playerhand.add_card(Card('Hearts', 'Nine'))
blackjack.show_player(playerhand)
blackjack.calculate_winner(dealerhand, playerhand)

# Player stands, Dealer wins
testDealer = Dealer(nineteen)
dealerhand = testDealer.hand
testplayer = Player()
testplayer.add_hand(fourteen)
playerhand = testplayer.hands[0]
blackjack.show_player(playerhand)
blackjack.calculate_winner(dealerhand, playerhand)

# Player stands, Dealer busts
testDealer = Dealer(nineteen)
dealerhand = testDealer.hand
testplayer = Player()
testplayer.add_hand(nineteen)
playerhand = testplayer.hands[0]
dealerhand.add_card(Card('Hearts', 'Nine'))
blackjack.show_player(playerhand)
blackjack.calculate_winner(dealerhand, playerhand)
