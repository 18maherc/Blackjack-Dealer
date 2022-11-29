import numpy as np
import cv2
import random
import time
import string
import statistics

from game_objects import Card 


class Detector:
    def __init__(self):
        
        self.valueImageArray = []
        self.suitImageArray = []
        self.valueArray = ['ace', '2','3','4','5','6','7','8','9','10','jack','queen','king']
        self.suitArray = ['Spades','Clubs','Hearts','Diamonds']
        
    def findFaceCardTest(self,img,contours):
        
        testFilter = []
        testFilter2 = []
        testFilterValue = []
        testFilterValue2 = []
        
        warped = img[200:350,350:550]
        
        thresh = self.editCard(warped)
        contours2, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        
        cv2.imwrite("CroppedImage.png",warped)
        print("These are from the suit")
        for c in contours2:
           if cv2.contourArea(c) > 3000 or cv2.contourArea(c)<1200 or cv2.arcLength(c,True)>350:continue
           area = cv2.contourArea(c)
           p = cv2.arcLength(c,True)
           # print(area,p)
           testFilter.append(c)
        
        for c in contours2:
           if (cv2.contourArea(c) > 1350 and cv2.contourArea(c)<1450 and cv2.arcLength(c,True)>145 and cv2.arcLength(c,True) <185) or (cv2.contourArea(c) > 1725 and cv2.contourArea(c)<1835 and cv2.arcLength(c,True)>170 and cv2.arcLength(c,True) <205) or (cv2.contourArea(c) > 1615 and cv2.contourArea(c)<1710 and cv2.arcLength(c,True)>215 and cv2.arcLength(c,True) <255) or (cv2.contourArea(c) > 1750 and cv2.contourArea(c)<1860 and cv2.arcLength(c,True)>250 and cv2.arcLength(c,True) <290):
               area = cv2.contourArea(c)
               p = cv2.arcLength(c,True)
               print(area,p)
               testFilter2.append(c)
           
           
        objectsTest = np.zeros([warped.shape[0],warped.shape[1],3], 'uint8')
        
        for c in testFilter2:
            col = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
            cv2.drawContours(objectsTest,[c], -1, col, -1)
            area = cv2.contourArea(c)
            p = cv2.arcLength(c,True)
            # print(area,p)
            
            
        print("THESE NEXT ONES ARE THE VALUE")
        
        for c in contours2:
           if cv2.contourArea(c) > 700 or cv2.contourArea(c)<225 or cv2.arcLength(c,True)>250 or cv2.arcLength(c,True)<90 or (cv2.arcLength(c,True)>200 and cv2.contourArea(c)>500):continue
           area = cv2.contourArea(c)
           p = cv2.arcLength(c,True)
 #          print(area,p)
           testFilterValue.append(c)
           
        for c in contours2:
           if (cv2.contourArea(c) > 180 and cv2.contourArea(c)<320 and cv2.arcLength(c,True)>105 and cv2.arcLength(c,True) <165) or (cv2.contourArea(c) > 375 and cv2.contourArea(c)<475 and cv2.arcLength(c,True)>180 and cv2.arcLength(c,True) <230) or (cv2.contourArea(c) > 560 and cv2.contourArea(c)< 650 and cv2.arcLength(c,True)>95 and cv2.arcLength(c,True) <130):
               area = cv2.contourArea(c)
               p = cv2.arcLength(c,True)
               print(area,p)
               testFilterValue2.append(c)    
           
        objectsTestValue = np.zeros([warped.shape[0],warped.shape[1],3], 'uint8')
        
        for c in testFilterValue2:
            col = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
            cv2.drawContours(objectsTestValue,[c], -1, col, -1)
            area = cv2.contourArea(c)
            p = cv2.arcLength(c,True)
            # print(area,p)
        
 

        cv2.imshow("Contours",objectsTest)
        cv2.imwrite("ContoursTest.png",objectsTest)
        
        cv2.imshow("Contours",objectsTestValue)
        cv2.imwrite("ContoursTestValue.png",objectsTestValue)
        
        faceArray = ['Jack','Queen','King']
        suitArray = ['Spades','Clubs','Hearts','Diamonds']
        
        suitAreaArray = [1653,1810,1782,1392]
        suitPArray = [234,270,188,165]
        
        valueAArray = [267,605,425]
        valuePArray = [134,111,202]
        
        sortedSuit = sorted(testFilter2, key=cv2.contourArea, reverse=False)
        if len(testFilter2)>0:
            x1 = sortedSuit[0]
            medCP = cv2.arcLength(x1,True)
        else:
            medCP = 160
        
        
        sortedValue = sorted(testFilterValue2, key=cv2.contourArea, reverse=True)
        if len(testFilterValue2)>0:
            x2 = sortedValue[0]
            faceP = cv2.arcLength(x2,True)
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

        foundCard = Card(suitArray[suitIndex],faceArray[faceIndex])      
        return foundCard

    def findFaceCard(self,img,filteredFace,filteredSpecFace):
        
        filteredValues = []
        filteredSuit = []
                     
        sortedContours = sorted(filteredFace, key=cv2.contourArea, reverse=True)
        wholeCard = sortedContours[0]

        epsilon = 0.01*cv2.arcLength(wholeCard,True)
        approx = cv2.approxPolyDP(wholeCard,epsilon,True)
        
        

        # Cast the approximate points received to float32
        # Now have th corner points to the outline of the card
        # Will use these to shrink the card to a uniform size
        cornerPoints = np.float32(approx)

        x,y,w,h = cv2.boundingRect(wholeCard)
        
        print("x: ", x)
        print("y: ",y)
        print("w: ",w)
        print("H: ",h)

        # (x,y) is the coordinate of the top left corner of the card
        #  w is the width of the card, h is the height

        rect = np.zeros((4,2), dtype = "float32")
        # points stored top left, top right, bottom right, bottom left
        s = cornerPoints.sum(axis = 2)
        rect[0] = cornerPoints[np.argmin(s)]
        rect[2] = cornerPoints[np.argmax(s)]

        diff = np.diff(cornerPoints, axis = -1)
        rect[1] = cornerPoints[np.argmin(diff)]
        rect[3] = cornerPoints[np.argmax(diff)]

        TopLeft = rect[0]
        TopRight = rect[1]
        BottomRight = rect[2]
        BottomLeft = rect[3]

        maxWidth = 300
        maxHeight = 400
        dst = np.array([
           [0, 0],
           [maxWidth - 1, 0],
           [maxWidth - 1, maxHeight - 1],
           [0, maxHeight - 1]], dtype = "float32")
        # compute the perspective transform matrix and then apply it
        M = cv2.getPerspectiveTransform(rect, dst)
        warped2 = cv2.warpPerspective(img, M, (maxWidth, maxHeight))

        cv2.imshow("Warped", warped2)
        cv2.imwrite("warped.png",warped2)

        # Now I should have a 300x400 image of the desired card
        # Going to crop out the value and the suit
        warped = warped2[0:75,0:50]
        valueCrop = warped2[0:60,0:50]

        cv2.imshow("Get Value", valueCrop)

        suitCrop = warped2[60:106,0:50]

        cv2.imshow("Get Suit", suitCrop)

        # Repeat graying and blurring for the cropped out value/suit
        grayValue = cv2.cvtColor(valueCrop,cv2.COLOR_BGR2GRAY)
        blurValue = cv2.GaussianBlur(grayValue, (3,3),0)

        threshValue = cv2.adaptiveThreshold(blurValue, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 205, 1)
        cv2.imshow("BinaryCornerValue",threshValue)
        
        grayW = cv2.cvtColor(warped,cv2.COLOR_BGR2GRAY)
        blurW = cv2.GaussianBlur(grayW, (3,3),0)

        threshW = cv2.adaptiveThreshold(blurW, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 205, 1)
        #cv2.imshow("BinaryCornerValue",threshValue)

        graySuit = cv2.cvtColor(suitCrop,cv2.COLOR_BGR2GRAY)
        blurSuit = cv2.GaussianBlur(graySuit, (3,3),0)

        threshSuit = cv2.adaptiveThreshold(blurSuit, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 205, 1)
        cv2.imshow("BinaryCornerSuit",threshSuit)

        contoursValue, _ = cv2.findContours(threshValue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        print(len(contoursValue))
        print("cropped image contour count:")
        contoursW, _ = cv2.findContours(threshW, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        print(len(contoursW))

        contoursSuit, _ = cv2.findContours(threshSuit, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        print(len(contoursSuit))
        
        for cc in contoursValue:
            if cv2.contourArea(cc) < 300:continue
            filteredValues.append(cc)
        
        
        for cc in contoursW:
            if cv2.arcLength(cc,True)<100 or cv2.arcLength(cc,True)>250:continue
            filteredSpecFace.append(cc)


        for cc in contoursSuit:
           if cv2.contourArea(cc) < 200:continue
           filteredSuit.append(cc)
           
        print("Quantity of contours found in the value crop")
        print(len(filteredValues))
        print("Quantity of contours found in the suit crop")
        print(len(filteredSuit))
        objects2 = np.zeros([img.shape[0],img.shape[1],3], 'uint8')
        objects3 = np.zeros([warped2.shape[0],warped2.shape[1],3], 'uint8')
        objectsValue = np.zeros([valueCrop.shape[0],valueCrop.shape[1],3], 'uint8')
        objectsSuit = np.zeros([suitCrop.shape[0],suitCrop.shape[1],3], 'uint8')
        for c in filteredFace:
            col = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
            cv2.drawContours(objects2,[c], -1, col, -1)
            area = cv2.contourArea(c)
            p = cv2.arcLength(c,True)
            print(area,p)
        
        # Draw contours for the value and suit
        print("Value Contours")
        for cc in filteredValues:
            col = (255, 255, 255)
            cv2.drawContours(objectsValue,[cc], -1, col, -1)
            area = cv2.contourArea(cc)
            p = cv2.arcLength(cc,True)

            print(area,p)

        print("Suit Contours")
        for cc in filteredSuit:
            col = (255, 255, 255)
            cv2.drawContours(objectsSuit,[cc], -1, col, -1)
            area = cv2.contourArea(cc)
            p = cv2.arcLength(cc,True)
 
            print(area,p)
            
        print("testing")
        for c in filteredSpecFace:
            col = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
            cv2.drawContours(objects3,[c], -1, col, -1)
            area = cv2.contourArea(c)
            p = cv2.arcLength(c,True)
            print(area,p)
        
        cv2.imwrite("Contours2.png",objects2)
        
        cv2.imwrite("Contours3.png",objects3)
        
        storedFaceAArray = [382,820,555]
        storedFacePArray = [155,120,225]
        minDiff = 1000000
        faceIndex = 2
        suitIndex = 3
        faceArray = ['jack','queen','king']
        suitArray = ['Spades','Clubs','Hearts','Diamonds']
        
        sortedContours = sorted(filteredSpecFace, key=cv2.contourArea, reverse=True)
        check = sortedContours[0]
        areaC = cv2.contourArea(check) 
        for i in range(3):
            q = abs((areaC - storedFaceAArray[i])/storedFaceAArray[i])
            if q < minDiff:
                faceIndex = i
                minDiff = q
                
        predictedValue = faceArray[faceIndex]
        print("The identified Value is: ", format(predictedValue))
        
        cardString = predictedValue + 'of' + self.suitArray[suitIndex]
        
        return cardString
        
    def editCard(self,img):

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3,3),0)

        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 205, 1)
        cv2.imshow("Binary",thresh)

        return thresh

    def getContours(self,thresh,img):
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
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
           if cv2.contourArea(c) > 3000 or cv2.contourArea(c)<1650 or cv2.arcLength(c,True)>410:continue
           area = cv2.contourArea(c)
           p = cv2.arcLength(c,True)
           print(area,p)
           initFiltered.append(c)
           filteredContours.append(cv2.arcLength(c,True))
           filteredAreas.append(cv2.contourArea(c))
        for c in contours:
            if cv2.contourArea(c) < 400 or cv2.contourArea(c)<10000 or cv2.arcLength(c,True)>1000 or cv2.arcLength(c,True)>625: continue
            arrayAceOfSpades.append(c)
        
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
            if cv2.arcLength(c,True)<900 or cv2.arcLength(c,True)>2000 or cv2.contourArea(c)<40000 or cv2.contourArea(c)>80000: continue
            print("arc length is: ",cv2.arcLength(c,True))
            filteredFace.append(c)
        
        #for c in contours:
        #    if cv2.contourArea(c) < 100: continue
        #    filteredSpecFace.append(c)

        print("Size of face checking array:")
        print(len(filteredFace))
        medianContourPerimeter = 0
        medianContourArea = 0
        if len(filteredFace) == 0 and len(filteredContours)>0:
            medianContourPerimeter = statistics.median(filteredContours)
            print(medianContourPerimeter)
            medianContourArea = statistics.median(filteredAreas)

            for q in initFiltered:
                if abs(cv2.arcLength(q,True)-medianContourPerimeter) < 60:
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
        objects = np.zeros([img.shape[0],img.shape[1],3], 'uint8')
        
        for c in filtered:
            col = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
            cv2.drawContours(objects,[c], -1, col, -1)
            area = cv2.contourArea(c)
            p = cv2.arcLength(c,True)
            print(area,p)
        print("full list")
 

        cv2.imshow("Contours",objects)
        cv2.imwrite("Contours.png",objects)
        
        # cv2.imwrite("queen.png",objectsValue)
        #cv2.imwrite("Hearts.png",objectsSuit)
      
        contourCut = (filtered,filteredFace,filteredSpecFace,arrayAceOfSpades,medianContourArea,medianContourPerimeter,contours)
        return contourCut
    def loadCards(self):




        for i in range(13):
            filename = self.valueArray[i] + '.png'
            self.valueImageArray.append(cv2.imread(filename,1))

        for j in range(4):
            filename = self.suitArray[j] + '.png'
            self.suitImageArray.append(cv2.imread(filename,1))

    def checkCard(self,filtered,medCA,medCP):

        valueArray = ['Ace', 'Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten']
        
        suitArray = ['Spades','Clubs','Hearts','Diamonds']
        storedAreaArray = [2950,3100,3100,2200]
        storedPArray = [300,350,250,200]
        storedPArray2 = [250,300,210,180]
        
        storedFaceSuitAArray = [0,0,0,400]
        minDiff = 1000000
        valueIndex = 100
        faceIndex = 2
        suitIndex = 3
        
    
        for i in range(4):
            q = abs((medCP - storedPArray2[i])/storedPArray2[i])
            if q < minDiff:
                suitIndex = i
                minDiff = q

        print("Check for Value")
        if(len(filtered)>0):
            valueIndex = len(filtered)-1
        else:
            valueIndex = 0
            
        predictedValue = valueArray[valueIndex]
        print("The identified Value is: ", format(predictedValue))

        
        cardString = predictedValue + 'of' + self.suitArray[suitIndex]

        foundCard = Card(suitArray[suitIndex],valueArray[valueIndex])      
        return foundCard

        #cv2.destroyAllWindows()
        #return cardString
