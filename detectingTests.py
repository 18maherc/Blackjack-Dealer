from mainDetector import getCard

import time
from blackjack import Card

start_time = time.time()
receivedcard = getCard()
end_time = time.time() - start_time
print("The time for the trial is: ", end_time)
print("seconds")
