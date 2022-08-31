from cvzone.HandTrackingModule import HandDetector
import cv2
import mediapipe as mp
import numpy as np
import urllib.request


class Rec_Camera_Hand:
    """
    Rec camera Hand get camera input from camera (default camera is PC default camera
    
    and can be changed to use phone camera using IP camera app and enter the localHost IP address as URL)
    
    * source 0 = default PC camera
    * source 1 = phone camera
    
    ================================================================
    
    - To get the hands and fingers status use the Get_hands_status. this function return the hands and the 
        fingers status.
     
    """
    
    def __init__(self, source=0, URL = "http://192.168.1.7:8080/shot.jpg"):
        self.source = source
        self.URL = "http://192.168.1.7:8080/shot.jpg"
        self.detector = HandDetector(detectionCon=0.8, maxHands=2)
        self.vid = cv2.VideoCapture(0)
            
            
    def Get_hands_status(self):
        """
        
        this function get the get Image from source,
        process the Image to find hands and fingers and return the 
        1. Hands -> data list of the hands location (see Hands utils)
        2. fingers -> list of fingers up or down. for example: [0, 1, 0, 0, 0] -> means that just the second fingers is up.
        3. the image from source.
        
        """
        if self.source == 0:
            image = self._get_image()
        elif self.source == 1:
            image = self._get_image_phone()
            
        q = cv2.waitKey(1)
        hands, image = self.detector.findHands(image, flipType=False)
        
        if hands:
            right_hand = hands[0]
            fingers = self.detector.fingersUp(right_hand)
            return hands, fingers, image
        return None, None, image

    
#==============================================#
#                PRIVATE FUNCTION              #
#==============================================#
    
    
    def _get_image(self):
        ret, frame = self.vid.read()
        return frame
        
    
    def _get_image_phone(self):
        img_arr = np.array(bytearray(urllib.request.urlopen(self.URL).read()),dtype=np.uint8)
        image = cv2.imdecode(img_arr,-1)
        image = cv2.flip(image, 0)
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        return image