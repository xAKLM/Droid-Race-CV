import numpy as np
import cv2

cap = cv2.VideoCapture(0) #0 means its continuous

color = (0, 255, 0)
line_width = 3
radius = 100
point = (0,0)

while (True):

        ret,frame1 = cap.read()
        #resize video
        frame1 = cv2.resize(frame1, (0,0), fx=1, fy=1) #no absolute value, only halves
        frame1 = cv2.bilateralFilter(frame1, 9, 75, 75)

        h,w,c = frame1.shape
        gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        camera_hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
        low_red = np.array([0,100,100])
        high_red = np.array([21, 255, 255])

        red_mask = cv2.inRange(camera_hsv, low_red, high_red)
        red = cv2.bitwise_and(frame1, frame1, mask=red_mask)
        cv2.imshow("frame1", frame1)
        cv2.imshow("mask", red)

        # dark_green = np.array([109, 89, 32])
        # light_green = np.array([109, 61, 90])
        # mask_green = cv2.inRange(camera_hsv, light_green, dark_green)
        # mask_white = cv2.inRange(gray, 200, 255)
        # mask_new = cv2.bitwise_or(mask_white, mask_green)
        # filtered = cv2.bitwise_and(gray, mask_new)
        # mask_green = cv2.resize(mask_green, (w,h))
        # mask_green = np.stack((mask_green,) * 3, axis=-1)
        # yuv = cv2.cvtColor(frame1, cv2.COLOR_BGR2YUV)
        luv = cv2.cvtColor(frame1, cv2.COLOR_BGR2LUV)
        low_luv = np.array([30,100,100])
        high_luv = np.array([80, 255, 255])

        luv_mask = cv2.inRange(luv, low_luv, high_luv)
        luv_filter = cv2.bitwise_and(frame1,frame1,mask=luv_mask)
        cv2.imshow("luv", luv)
        cv2.imshow("fitlered", luv_filter)

        # HLS = cv2.cvtColor(frame1, cv2.COLOR_BGR2HLS)
        # LAB = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    
        # print(luv)
        # print(mask_green)
        
        # #YUV good for blue little bit good for purple
        # cv2.imshow("yuv", yuv)

        # #LUV good for red
        cv2.imshow("luv", luv)

        # #HLS good for yellow
        # cv2.imshow("HLS", HLS)

        # greenOr = cv2.bitwise_or(luv, mask_green)
        # cv2.imshow("OR", greenOr)

        # greenAnd = cv2.bitwise_and(luv, mask_green)
        # cv2.imshow("AND", greenAnd)

        # cv2.imshow("LAB", LAB)
        # cv2.imshow("gray", mask_white)
        # cv2.imshow("green", mask_green)
        # cv2.imshow("Frame", filtered)

        #Exit condition
        ch = cv2.waitKey(1) #run every 1 milisecond 
        if ch == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()


