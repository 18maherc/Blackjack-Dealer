import numpy as np
import cv2
import random
import time
import string
import statistics

from blackjack import Card


class Detector:
    def __init__(self):

        self.valueImageArray = []
        self.suitImageArray = []
        self.valueArray = ['ace', '2', '3', '4', '5', '6',
                           '7', '8', '9', '10', 'jack', 'queen', 'king']
        self.suitArray = ['Spades', 'Clubs', 'Hearts', 'Diamonds']

    def findFaceCardTest(self, img, contours):

        testFilter = []
        testFilter2 = []
        testFilterValue = []
        testFilterValue2 = []

        warped = img[200:350, 350:550]

        thresh = self.editCard(warped)
        contours2, _ = cv2.findContours(
            thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cv2.imwrite("CroppedImage.png", warped)
        print("These are from the suit")
        for c in contours2:
            if cv2.contourArea(c) > 3000 or cv2.contourArea(c) < 1200 or cv2.arcLength(c, True) > 350:
                continue
            area = cv2.contourArea(c)
            p = cv2.arcLength(c, True)
            # print(area,p)
            testFilter.append(c)

        for c in contours2:
            if (cv2.contourArea(c) > 1350 and cv2.contourArea(c) < 1450 and cv2.arcLength(c, True) > 145 and cv2.arcLength(c, True) < 185) or (cv2.contourArea(c) > 1725 and cv2.contourArea(c) < 1835 and cv2.arcLength(c, True) > 170 and cv2.arcLength(c, True) < 205) or (cv2.contourArea(c) > 1615 and cv2.contourArea(c) < 1710 and cv2.arcLength(c, True) > 215 and cv2.arcLength(c, True) < 255) or (cv2.contourArea(c) > 1750 and cv2.contourArea(c) < 1860 and cv2.arcLength(c, True) > 250 and cv2.arcLength(c, True) < 290):
                area = cv2.contourArea(c)
                p = cv2.arcLength(c, True)
                print(area, p)
                testFilter2.append(c)

        objectsTest = np.zeros([warped.shape[0], warped.shape[1], 3], 'uint8')

        for c in testFilter2:
            col = (random.randint(0, 255), random.randint(
                0, 255), random.randint(0, 255))
            cv2.drawContours(objectsTest, [c], -1, col, -1)
            area = cv2.contourArea(c)
            p = cv2.arcLength(c, True)
            # print(area,p)

        print("THESE NEXT ONES ARE THE VALUE")

        for c in contours2:
            if cv2.contourArea(c) > 700 or cv2.contourArea(c) < 225 or cv2.arcLength(c, True) > 250 or cv2.arcLength(c, True) < 90 or (cv2.arcLength(c, True) > 200 and cv2.contourArea(c) > 500):
                continue
            area = cv2.contourArea(c)
            p = cv2.arcLength(c, True)
  #          print(area,p)
            testFilterValue.append(c)

        for c in contours2:
            if (cv2.contourArea(c) > 180 and cv2.contourArea(c) < 320 and cv2.arcLength(c, True) > 120 and cv2.arcLength(c, True) < 150) or (cv2.contourArea(c) > 375 and cv2.contourArea(c) < 475 and cv2.arcLength(c, True) > 188 and cv2.arcLength(c, True) < 215) or (cv2.contourArea(c) > 560 and cv2.contourArea(c) < 650 and cv2.arcLength(c, True) > 95 and cv2.arcLength(c, True) < 130):
                area = cv2.contourArea(c)
                p = cv2.arcLength(c, True)
                print(area, p)
                testFilterValue2.append(c)

        objectsTestValue = np.zeros(
            [warped.shape[0], warped.shape[1], 3], 'uint8')

        for c in testFilterValue2:
            col = (random.randint(0, 255), random.randint(
                0, 255), random.randint(0, 255))
            cv2.drawContours(objectsTestValue, [c], -1, col, -1)
            area = cv2.contourArea(c)
            p = cv2.arcLength(c, True)
            # print(area,p)

        # cv2.imshow("Contours", objectsTest)
        cv2.imwrite("ContoursTest.png", objectsTest)

        # cv2.imshow("Contours", objectsTestValue)
        cv2.imwrite("ContoursTestValue.png", objectsTestValue)

        faceArray = ['Jack', 'Queen', 'King']
        suitArray = ['Spades', 'Clubs', 'Hearts', 'Diamonds']

        suitAreaArray = [1653, 1810, 1782, 1392]
        suitPArray = [234, 270, 188, 165]

        valueAArray = [267, 605, 425]
        valuePArray = [134, 111, 202]

        sortedSuit = sorted(testFilter2, key=cv2.contourArea, reverse=True)
        if len(testFilter2) > 0:
            x1 = sortedSuit[0]
            medCP = cv2.arcLength(x1, True)
        else:
            medCP = 160

        sortedValue = sorted(
            testFilterValue2, key=cv2.contourArea, reverse=True)
        if len(testFilterValue2) > 0:
            x2 = sortedValue[0]
            faceP = cv2.arcLength(x2, True)
        else:
            faceP = 134

        suitIndex = 3
        faceIndex = 2
        minDiff = 100000
        minDiff2 = 100000
        for i in range(4):
            q = abs((medCP - suitPArray[i])/suitPArray[i])
            if q < minDiff:
                suitIndex = i
                minDiff = q

        for i in range(3):
            q = abs((faceP - valuePArray[i])/valuePArray[i])
            if q < minDiff2:
                faceIndex = i
                minDiff2 = q

        cardString = faceArray[faceIndex] + " of " + suitArray[suitIndex]

        foundCard = Card(suitArray[suitIndex], faceArray[faceIndex])
        return foundCard

    def editCard(self, img):

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)

        thresh = cv2.adaptiveThreshold(
            blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 205, 1)
        # cv2.imshow("Binary", thresh)

        return thresh

    def getContours(self, thresh, img):

        contours, _ = cv2.findContours(
            thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        print(len(contours))

        # Create an array to filter out the contours that are too small - which means they are not what is desired
        # FilteredValues should have 1 or 2 items, depending on the value (Q has 2, 10 might, 6 or 8 might)
        # FilteredSuit should have 1 item
        initFiltered = []
        secondFiltered = []
        filtered = []

        filteredContours = []
        filteredFace = []
        filteredAreas = []
        filteredSpecFace = []

        arrayAceOfSpades = []

        for c in contours:
            if (cv2.contourArea(c) > 2100 and cv2.contourArea(c) < 2475 and cv2.arcLength(c, True) > 253 and cv2.arcLength(c, True) < 280) or (cv2.contourArea(c) > 2250 and cv2.contourArea(c) < 2575 and cv2.arcLength(c, True) > 200 and cv2.arcLength(c, True) < 230) or (cv2.contourArea(c) > 1610 and cv2.contourArea(c) < 1800 and cv2.arcLength(c, True) > 170 and cv2.arcLength(c, True) < 195) or (cv2.contourArea(c) > 2325 and cv2.contourArea(c) < 2625 and cv2.arcLength(c, True) > 290 and cv2.arcLength(c, True) < 320):
                area = cv2.contourArea(c)
                p = cv2.arcLength(c, True)
                print(area, p)
                initFiltered.append(c)
                filteredContours.append(cv2.arcLength(c, True))
                filteredAreas.append(cv2.contourArea(c))
        for c in contours:
            if (cv2.contourArea(c) > 9000 and cv2.contourArea(c) < 11000 and cv2.arcLength(c, True) > 450 and cv2.arcLength(c, True) < 550):
                # continue
                arrayAceOfSpades.append(c)
                print(cv2.contourArea(c))
                print(cv2.arcLength(c, True))

#         objectsTest = np.zeros([img.shape[0],img.shape[1],3], 'uint8')
#         for c in initFiltered:
#             col = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
#             cv2.drawContours(objectsTest,[c], -1, col, -1)
#             area = cv2.contourArea(c)
#             p = cv2.arcLength(c,True)
#             print(area,p)

      # cv2.imwrite("ContourTest.png",objectsTest)
        for c in contours:
            #              print("arc length is: ",cv2.arcLength(c,True))
            if cv2.arcLength(c, True) < 900 or cv2.arcLength(c, True) > 2000 or cv2.contourArea(c) < 40000 or cv2.contourArea(c) > 80000:
                continue
            print("arc length is: ", cv2.arcLength(c, True))
            filteredFace.append(c)

        # for c in contours:
        #    if cv2.contourArea(c) < 100: continue
        #    filteredSpecFace.append(c)

        print("Size of face checking array:")
        print(len(filteredFace))
        medianContourPerimeter = 0
        medianContourArea = 0
        if len(filteredFace) == 0 and len(filteredContours) > 0:
            medianContourPerimeter = statistics.median(filteredContours)
            print(medianContourPerimeter)
            medianContourArea = statistics.median(filteredAreas)

            for q in initFiltered:
                if abs(cv2.arcLength(q, True)-medianContourPerimeter) < 60:
                    print("here")
                    secondFiltered.append(q)

            for q in secondFiltered:
                if abs(cv2.contourArea(q)-medianContourArea) < 300:
                    filtered.append(q)

                # Get the largest contour, which should be the whole card

        print("Quantity of contours found total")
        print(len(filtered))

        # Will create arrays of the same size of the images
        # These are to store the contour images
        objects = np.zeros([img.shape[0], img.shape[1], 3], 'uint8')

        for c in filtered:
            col = (random.randint(0, 255), random.randint(
                0, 255), random.randint(0, 255))
            cv2.drawContours(objects, [c], -1, col, -1)
            area = cv2.contourArea(c)
            p = cv2.arcLength(c, True)
            print(area, p)
        print("full list")

        # cv2.imshow("Contours", objects)
        cv2.imwrite("Contours.png", objects)

        # cv2.imwrite("queen.png",objectsValue)
        # cv2.imwrite("Hearts.png",objectsSuit)

        contourCut = (filtered, filteredFace, filteredSpecFace, arrayAceOfSpades,
                      medianContourArea, medianContourPerimeter, contours)
        return contourCut

    def loadCards(self):

        for i in range(13):
            filename = self.valueArray[i] + '.png'
            self.valueImageArray.append(cv2.imread(filename, 1))

        for j in range(4):
            filename = self.suitArray[j] + '.png'
            self.suitImageArray.append(cv2.imread(filename, 1))

    def checkCard(self, filtered, medCA, medCP):

        valueArray = ['Ace', 'Two', 'Three', 'Four',
                      'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten']

        suitArray = ['Spades', 'Clubs', 'Hearts', 'Diamonds']
        storedAreaArray = [2950, 3100, 3100, 2200]
        storedPArray = [300, 350, 250, 200]
        storedPArray2 = [250, 300, 210, 180]

        storedFaceSuitAArray = [0, 0, 0, 400]
        minDiff = 1000000
        valueIndex = 100
        faceIndex = 2
        suitIndex = 3

        for i in range(4):
            q = abs((medCP - storedPArray2[i])/storedPArray2[i])
            if q < minDiff:
                suitIndex = i
                minDiff = q
        print("Length of Contours ", len(filtered))
        print("Check for Value")
        if (len(filtered) > 10):
            valueIndex = 9
        elif (len(filtered) > 0):
            valueIndex = len(filtered)-1
        else:
            valueIndex = 0

        predictedValue = valueArray[valueIndex]
        print("The identified Value is: ", format(predictedValue))

        cardString = predictedValue + 'of' + self.suitArray[suitIndex]

        foundCard = Card(suitArray[suitIndex], valueArray[valueIndex])
        return foundCard

        # cv2.destroyAllWindows()
        # return cardString
