from turtle import width
import cv2
import mediapipe as mp
import urllib.request
import numpy as np
import time
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(detectionCon=0.8, maxHands=1)

URL = "http://192.168.1.7:8080/shot.jpg"

while True:
    img_arr = np.array(bytearray(urllib.request.urlopen(URL).read()),dtype=np.uint8)
    image = cv2.imdecode(img_arr,-1)
    image = cv2.flip(image, 0)
    image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    q = cv2.waitKey(1)
    if q == ord("q"):
        break;
    
    hands, image = detector.findHands(image, flipType=False)
    cv2.imshow("image", image)
    
    # if hands:
    #     hand = hands[0]
    #     fingers = detector.fingersUp(hand)
    #     # print(hand)
    #     print(fingers)
    #     if fingers == [0, 1, 0, 0, 0]:
    #         print("playing!")
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # cv2.waitKey(1)
    # success, image = cap.read()
    # RGB_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # results = hands.process(RGB_image)
    # print(results)
    # multiLandMarks = results.multi_hand_landmarks
    # if multiLandMarks:
    #     handList = []
    #     for handLms in multiLandMarks:
    #         mpDraw.draw_landmarks(image, handLms, mp_Hands.HAND_CONNECTIONS)
    #         for idx, lm in enumerate(handLms.landmark):
    #             # print("here")
    #             h, w, c = image.shape
    #             cx, cy = int(lm.x * w), int(lm.y * h)
    #             handList.append((cx, cy))
    #     for point in handList:
    #         # print(point)
    #         cv2.circle(image, point, 10, (255, 255, 0), cv2.FILLED)
                
    #     upCount = 0
    #     for coordinate in finger_Coord:
    #         if handList[coordinate[0]][1] < handList[coordinate[1]][1]:
    #             upCount += 1
    #     if handList[thumb_Coord[0]][0] > handList[thumb_Coord[1]][0]:
    #         upCount += 1
    #     # print(upCount)
    #     cv2.putText(image, str(upCount), (150,150), cv2.FONT_HERSHEY_PLAIN, 12, (0,255,0), 12)

    #     cv2.imshow("Counting number of fingers", image)
    #     cv2.waitKey(1)