from cvzone.HandTrackingModule import HandDetector
import cv2
import mediapipe as mp
import numpy as np
import urllib.request


class Rec_Camera_Hand:
    def __init__(self, source=0, URL = "http://192.168.1.7:8080/shot.jpg"):
        self.source = source
        self.URL = "http://192.168.1.7:8080/shot.jpg"
        self.detector = HandDetector(detectionCon=0.8, maxHands=1)
        self.vid = cv2.VideoCapture(0)
        
        
    def start_rec_camera(self):
        if self.source == 0:
            self.start_source_IP()    
            
            
    def Get_hands_status(self):
        image = self._get_image()
        q = cv2.waitKey(1)
        hands, image = self.detector.findHands(image, flipType=False)
        cv2.imshow("image", image)
        if hands:
            right_hand = hands[0]
            fingers = self.detector.fingersUp(right_hand)
            return hands, fingers
        return None, None

    
    
    
    def _get_image(self):
        ret, frame = self.vid.read()
        return frame
        
        
    
    def _get_image_phone(self):
        img_arr = np.array(bytearray(urllib.request.urlopen(self.URL).read()),dtype=np.uint8)
        image = cv2.imdecode(img_arr,-1)
        image = cv2.flip(image, 0)
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        return image