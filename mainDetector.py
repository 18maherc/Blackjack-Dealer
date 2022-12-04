import cv2
import numpy as np
import time
import os

from dataStream import VideoStream
from CardDetector import Detector
import blackjack


def getCard():

    camStream = VideoStream((600, 700), 10).start()
    time.sleep(1)  # Give the camera time to warm up
    while True:

        stop_camera = 0
        detect = Detector()
        # detect.loadCards()

        img = camStream.read()

        cv2.imshow("Image from Camera", img)
        cv2.imwrite("ReceivedImage.png", img)

        thresh = detect.editCard(img)

        array1, array2, array3, aceArray, medCA, medCP, contours = detect.getContours(
            thresh, img)

        #cv2.imshow("Suit Pulled", suitSent)
        #cv2.imshow("Value pulled", valueSent)
        if len(aceArray) == 0 and len(array1) == 0 and len(array2) == 0:
            cardIdentity = blackjack.Card('Joker', 'Joker')
        elif len(aceArray) == 1 and len(array1) == 0:
            cardIdentity = blackjack.Card('Spades', 'Ace')
        elif len(array2) > 0:
            cardIdentity = detect.findFaceCardTest(img, contours)
            #cardIdentity = detect.findFaceCard(img,array2,array3)
        else:
            cardIdentity = detect.checkCard(array1, medCA, medCP)

        print("the card identified is: ", cardIdentity.to_string())
        cv2.destroyAllWindows()

        if cardIdentity.value == 'Joker':
            time.sleep(1)  # Give the camera time to warm up
            continue
        else:
            camStream.stop()
            return cardIdentity

    # cardIdentity = detect.checkCard(array1,array2,array3, suitSent,valueSent,medCA,medCP)

    # print("The identified Card is:", cardIdentity)

    # cv2.waitKey(0)
    # Poll the keyboard. If 'q' is pressed, exit the main loop.
    # key = cv2.waitKey(1) & 0xFF
    # if key == ord("c"):
    # stop_camera = 1

    # Close all windows and close the PiCamera video stream.
