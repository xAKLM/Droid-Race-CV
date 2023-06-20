
from cv2 import resize
import numpy as np
import cv2
import colorThresholds
import math

LEFT = 0
RIGHT = 1
X = 0
Y = 1
#cap = cv2.VideoCapture(0) #0 means its continuous
cap = cv2.VideoCapture("../resource/video1.mov")
MIDDLE_SCREEN = 700

def resize_ratio(image, ratio):
    width = image.shape[1]
    height = image.shape[0]
    resize_dims = [int(width * ratio), int (height * ratio)]

    return cv2.resize(image, resize_dims)

while (cap.isOpened()):

        #cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        ret,frame1 = cap.read()

        #print(frame1.shape)
        initial = frame1
        #initial = resize_ratio(frame1, 0.5)
        HEIGHT,WIDTH,CHANNELS = initial.shape
        HEIGHT = HEIGHT / 2
        frame1 = cv2.resize(frame1, (0,0), fx=2, fy=2)
        #frame1 = cv2.bilateralFilter(frame1, 4, 3, 3)
        #frame1 = resize_ratio(frame1, 0.5)
        frame1 = cv2.GaussianBlur(frame1, (3,3), 0)
        frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
        
        #### MASK CREATION ####
        lBlue,hBlue = colorThresholds.blue_limits_HSV()
        blue_mask = cv2.inRange(frame1, lBlue, hBlue)

        lYellow, hYellow = colorThresholds.yellow_limits_HSV()
        yellow_mask = cv2.inRange(frame1, lYellow, hYellow)

        lPurple, hPurple = colorThresholds.purple_limits_HSV()
        purple_mask = cv2.inRange(frame1, lPurple, hPurple)

        lane_mask = cv2.bitwise_or(blue_mask, yellow_mask)
        #lane_mask = cv2.bitwise_or(lane_mask, purple_mask)

        all = cv2.bitwise_and(frame1, frame1, mask=lane_mask)
        all = cv2.cvtColor(all, cv2.COLOR_HSV2BGR)
        
        contourList = []
        lowestPoints = []
        halfwayPoints = []

        #split contours for yellow and blue lane
        yellowContours,hierarchy = cv2.findContours(yellow_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        blueContours,hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        #sort by size
        blueContours = sorted(blueContours, key=cv2.contourArea)
        yellowContours = sorted(yellowContours, key=cv2.contourArea)


        #Add contours to the list if they are big enough, since its sorted by size, only need to check first index
        if (len(blueContours) != 0):
            if (cv2.contourArea(blueContours[-1]) >= 250):
                contourList.append(blueContours[-1])
        if (len(yellowContours) != 0):
            if (cv2.contourArea(yellowContours[-1]) >= 250):
                contourList.append(yellowContours[-1])
        p1 = (0,0)
        p2 = (0,0)
        

        #Can see two different Lanes
        if len(contourList) == 2:

            #Store halfway points and find the lowest points on the contour
            halfwayPoints.append(int(len(contourList[LEFT]) / 2))
            halfwayPoints.append(int(len(contourList[RIGHT]) / 2))

            lowestPoints.append(contourList[LEFT][halfwayPoints[LEFT]].ravel())
            lowestPoints.append(contourList[RIGHT][halfwayPoints[RIGHT]].ravel())

            if (lowestPoints[LEFT][Y] <= lowestPoints[RIGHT][Y]):
                lower = RIGHT
                upper = LEFT
                
            else:
                lower = LEFT
                upper = RIGHT

            found = False
            
            #iterate over the lowest lane until it is horizontal to a point on the higher lane
            for point1 in contourList[lower][halfwayPoints[lower] :]:

                if (math.fabs(point1.ravel()[Y] - lowestPoints[upper].ravel()[Y]) < 20 ):
                    cv2.line(all, tuple(point1.ravel()), tuple(lowestPoints[upper].ravel()), (0,255,0), thickness=3)
                    #cv2.circle(all, (point1.ravel()[0] + abs(point1.ravel()[0] - lowestPoints[upper].ravel()[0]), point1.ravel()[Y]), radius=2, color=(0,0,255), thickness=5)
                    cv2.circle(all, (MIDDLE_SCREEN, point1.ravel()[Y]), radius=2, color=(255,0,0), thickness=5)
                    p1 = tuple(point1.ravel())
                    p2 = tuple(lowestPoints[upper].ravel())
                    xList = [p1[X],p2[X]]
                    xList.sort(reverse=False)
                    #print(xList)
                    xMid = xList[0] + int(abs(xList[1] - xList[0]) / 2)
                    desiredP = (xMid, p1[Y])
                    cv2.circle(all, desiredP, radius=2, color=(0,0,255), thickness=10)
                    
                    Found = True
                    break

            # if found is False:
            #     cv2.line(all, lowestPoints[lower], (700, 400), (0,255,0), thickness=3)


            
        #Can only see 1 Lane
        if len(contourList) == 1:
            half1 = int(len(contourList[0]) / 2)
            lowestPoints.append(contourList[0][half1].ravel())
            cv2.line(all, lowestPoints[0], (MIDDLE_SCREEN, lowestPoints[0][Y]), (0,255,0), thickness=3)
            cv2.circle(all, (MIDDLE_SCREEN, lowestPoints[0][Y]), radius=2, color=(255,0,0), thickness=2)
            p1 = lowestPoints[0]
            p2 = (MIDDLE_SCREEN,lowestPoints[0][Y])
            desiredP = (MIDDLE_SCREEN, lowestPoints[0][Y])
        
        if abs(p1[X]-p2[X]) == 0:
            print('basically in middle aye')

        else:
            diff = (desiredP[X] - MIDDLE_SCREEN) / (abs(p1[X]-p2[X]))
            print(diff) 
        
        
        
        

        #IMAGE SHOW
        #cv2.resize(yellow_mask, (0,0), fx=0.5, fy=0.5)
        cv2.imshow("normal", initial)
        cv2.imshow("lanes", yellow_mask)
        #all = cv2.resize(all, (0,0), fx=0.5, fy=0.5)
        cv2.imshow("all", all)
        #BREAK
        ch = cv2.waitKey(1) #run every 1 milisecond 
        if ch == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()


