from audioop import avg
from calendar import c
from re import L
import cv2
import numpy as np
from q2HoughFull import *

def main():
    global image
    cap = cv2.VideoCapture("../resource/video1.mov")

    while (1):
        ret,image = cap.read()
        h,w,c = image.shape
        
        image = image[int(h*0.3):,int(0.05*w):int(0.95*w)  ]
        colImage = image.copy()
        allImgeTest = image.copy()

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        gray = cv2.GaussianBlur(gray, (7,7), cv2.BORDER_DEFAULT)
        gray = cv2.GaussianBlur(gray, (5,5), cv2.BORDER_DEFAULT)

        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15,1)
        edges = cv2.erode(edges, (20,20) ,iterations=5)


        conts, __ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        conts = sorted(conts, key=cv2.contourArea, reverse=True)[:10]
        filteredLaneContours = sortCntsByLaneShape(conts)
        blueLanes, yellowLanes, allLanes = sortLanesByColour(filteredLaneContours, colImage)

        cv2.imshow("image",image)
        cv2.imshow("col_image",colImage)


        cv2.imshow('edges', edges)
        cv2.imshow("gray", gray)
  
        if cv2.waitKey(50) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

def sortCntsByLaneShape(contours):
    sortedContours = []
    for cnt in contours:
        if cv2.contourArea(cnt) > 10000:
            continue
        lengthToTest = int(len(cnt)*0.35)
        errors = int(lengthToTest * 0.2)
        errorCount = 0
        for i,points in enumerate(cnt):
            points = points[0]
            laneCheck = False
            if i == 0:
                prev_y = points[1]
                continue

            if (prev_y <= points[1]):
                prev_y = points[1]
            else:
                errorCount += 1

            if errorCount >= errors:
                break

            if i == lengthToTest:
                laneCheck = True
                break

        # cv2.drawContours(image, [cnt], 0, (0,0,255), 2)

        if laneCheck:
            # cv2.drawContours(image, [cnt], 0, (0,255,255), 2)
            sortedContours.append(cnt)

    return sortedContours

def sortLanesByColour(contours, image):
    blueLanes = []
    yellowLanes = []
    allLanes = []

    yellowLower = (20, 50, 50)
    yellowUpper = (60,255,255)

    yellowLower = np.array([23,80,80])
    yellowUpper = np.array([60, 255, 255])
    
    blueLower = np.array([30,50,80])
    blueUpper = np.array([170,190,230])
    
    blueLower = np.array([60,40,40]) #93 100 100
    blueUpper = np.array([150,255,255]) #130 255 255

    HSVFrame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    blueMask = cv2.inRange(HSVFrame, blueLower, blueUpper)
    yellowMask = cv2.inRange(HSVFrame, yellowLower, yellowUpper)

    blueMask = cv2.dilate(blueMask, (5,5), iterations=8)
    yellowMask = cv2.dilate(yellowMask, (5,5), iterations=8)

    cv2.imshow("g", blueMask)
    cv2.imshow("y", yellowMask)

    for cnt in contours:
        blueCount = 0
        yellowCount = 0
        totalCount = int(len(cnt)*0.8) # check over half the contour length (saves computations)
        for i, point in enumerate(cnt):
            point = point[0]

            if blueMask[point[1]][point[0]] > 0:
               blueCount += 1
            if yellowMask[point[1]][point[0]] > 0:
                yellowCount += 1
            if (i == totalCount):
                break

        # print("BLUE: {0} YELLOW: {1} TOTAL: {2}".format(blueCount, yellowCount, totalCount))
        if blueCount > yellowCount:
            if blueCount / totalCount > 0.1:
                cv2.drawContours(image, [cnt], 0, (0,0,255), 2)
                blueLanes.append(cnt)
                allLanes.append(cnt)

        if yellowCount > blueCount:
            if yellowCount / totalCount > 0.1:
                cv2.drawContours(image, [cnt], 0, (0,255,0), 2)
                yellowLanes.append(cnt)
                allLanes.append(cnt)

        # if len(blueLanes) != 0: np.concatenate(blueLanes)
        # if len(allLanes) != 0: np.concatenate(allLanes)
        # if len(yellowLanes) != 0: np.concatenate(yellowLanes)

    return blueLanes, yellowLanes, allLanes
    
            
        
if __name__ == "__main__":
    main()
