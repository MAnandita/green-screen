import cv2
import numpy as np
import time

raw_video = cv2.VideoCapture(0)

time.sleep(1)

count = 0

background = 0

for i in range(60):
    return_val, background = raw_video.read()
    if return_val == False:
        continue

background = np.flip(background, axis = 1)

while(raw_video.isOpened()):
    return_val, image = raw_video.read()
    if return_val == False:
        break
    count += 1
    img = np.flip(image, axis = 1)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #lower mask (lighter green)
    lower_green = np.array([40, 100, 40]) 
    upper_green = np.array([40,255,255])

    mask1 = cv2.inRange(hsv,lower_green,upper_green)

    #upper mask (darker green)
    lower_green = np.array([40,155,40])
    upper_green = np.array([255,180,255])

    #creating the mask and applying 
    mask2 = cv2.inRange(hsv,lower_green,upper_green)

    mask1 = mask1 + mask2 #(adding the masks to apply both of them) now, mask1 is all green
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3), np.uint8), iterations = 2)
    
    mask2 = cv2.bitwise_not(mask1)

    #masking
    res1 = cv2.bitwise_and(background, background, mask = mask1)
    res2 = cv2.bitwise_and(img, img, mask = mask2)
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

    cv2.imshow("INVISIBLE MAN", final_output)
    k = cv2.waitKey(10)
    if k == 27:  #when you click on escape key, the program will stop working
        break