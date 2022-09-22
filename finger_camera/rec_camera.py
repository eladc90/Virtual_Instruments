from cvzone.HandTrackingModule import HandDetector
import cv2
import mediapipe as mp
import numpy as np
import urllib.request
import face_recognition
import math


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
        self.image = None
            

    def Record_data(self):
        if self.source == 0:
            self.image = self._get_image()
        elif self.source == 1:
            self.image = self._get_image_phone()
    
    
    def Get_hands_status(self):
        """
        
        this function get the get Image from source,
        process the Image to find hands and fingers and return the 
        1. Hands -> data list of the hands location (see Hands utils)
        2. fingers -> list of fingers up or down. for example: [0, 1, 0, 0, 0] -> means that just the second fingers is up.
        3. the image from source.
        
        """        
        q = cv2.waitKey(1)
        hands, image = self.detector.findHands(self.image, flipType=False)
        
        if hands:
            right_hand = hands[0]
            fingers = self.detector.fingersUp(right_hand)
            return hands, fingers, image
        return None, None, image

    
    def Get_is_mouth_open(self):
        if self.image is None:
            return None
        try:
            face_landmarks_list = face_recognition.face_landmarks(self.image, model='large')
            return self._is_mouth_open(face_landmarks_list[0])
        except Exception as ex:
            print(ex)
            return False


#==============================================#
#                PRIVATE FUNCTION              #
#==============================================#
    
    
    def _get_image(self):
        ret, frame = self.vid.read()
        image = cv2.flip(frame, 1)
        return image
        
    
    def _get_image_phone(self):
        img_arr = np.array(bytearray(urllib.request.urlopen(self.URL).read()),dtype=np.uint8)
        image = cv2.imdecode(img_arr,-1)
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        return image



#==============================================#
#              MOUTH FUNCTIONS                 #
#==============================================#


    def _get_lip_height(self, lip):
        sum=0
        for i in [2,3,4]:
            # distance between two near points up and down
            distance = math.sqrt( (lip[i][0] - lip[12-i][0])**2 +
                                  (lip[i][1] - lip[12-i][1])**2   )
            sum += distance
        return sum / 3


    def _get_mouth_height(self, top_lip, bottom_lip):
        sum = 0 
        for i in [8,9,10]:
            # distance between two near points up and down
            distance = math.sqrt( (top_lip[i][0] - bottom_lip[18-i][0])**2 + 
                                  (top_lip[i][1] - bottom_lip[18-i][1])**2   )
            sum += distance
        return sum / 3
    
    
    def _is_mouth_open(self, face_landmarks):
        top_lip = face_landmarks['top_lip']
        bottom_lip = face_landmarks['bottom_lip']
        top_lip_height =    self._get_lip_height(top_lip)
        bottom_lip_height = self._get_lip_height(bottom_lip)
        mouth_height =      self._get_mouth_height(top_lip, bottom_lip)

        # if mouth is open more than lip height * ratio, return true.
        ratio = 0.5
        if mouth_height > min(top_lip_height, bottom_lip_height) * ratio:
            return True
        else:
            return False