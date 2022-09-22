from re import L
from finger_camera.rec_camera import Rec_Camera_Hand
from virtual_instrument.sax_player import Saxophone_Player
from virtual_instrument.hands_utils import *
import math
import cv2
import pandas as pd
import csv
from tensorflow import keras
import tensorflow as tf
import numpy as np
from numpy import loadtxt


class Instrument_hands_processor:
    def __init__(self, source=0, 
                left_hand_model_path=r"C:\Users\cohene9\OneDrive - Medtronic PLC\Desktop\elad\new_ver\finger_model_left",
                right_hand_model_path=r'C:\Users\cohene9\OneDrive - Medtronic PLC\Desktop\elad\new_ver\finger_model_right'):
        
        self._camera_data = Rec_Camera_Hand(source)             # use camera to get hands and fingers status
        self._saxophone_player = Saxophone_Player()             # instrument player (for now just saxophone)
        self.fingers_points = FINGERS_POINTS()                  # fingers points and indexes 
        self.notes_dict = Saxophone_fingering.FINGERING_LIST    # get Note name by the list of on fingers
        self.Notes_number = Saxophone_fingering.NOTES_NUMBER    # get the midi Note number by the name of Note (example: 'c' = 48)
        self._current_fingers = []
        self._prev_fingers = []
        self._last_note = ''
        self._current_note = ''
        self._is_note_on = False
        self._air_on = False
        self._current_fingers_note = None
        self.volume = 400
        self.rectangle_size = 17
        self.image = None
        self.thickness = 3
        self.left_hand_model  = keras.models.load_model(left_hand_model_path)
        self.right_hand_model = keras.models.load_model(right_hand_model_path)
        
        
    def Start(self):
        """
        Get the hands and fingers positions from camera and process the fingers and hands to 
        play or stop note and change volume.
        """
        while True:
            self._camera_data.Record_data()
            hands, self._current_fingers, image = self._camera_data.Get_hands_status()
            # self._air_on = self._camera_data.Get_is_mouth_open()
            # print(self._air_on)
            self._air_on = True
            self.image = image
            cv2.imshow("image", self.image)
            if hands:
                if len(hands) >= 2:
                    right_hand = self._get_hand_from_type(hands, 'Right')
                    left_hand = self._get_hand_from_type(hands, 'Left')
                    if right_hand is None or left_hand is None:
                        continue
                    flat_right_hand = [item for sublist in right_hand['lmList'] for item in sublist]
                    flat_left_hand = [item for sublist in left_hand['lmList'] for item in sublist]                        
                    right_hand_sts_list = self._process_right_hand(flat_right_hand)
                    left_hand_sts_list = self._process_left_hand(flat_left_hand)
                    both_list = [left_hand_sts_list, right_hand_sts_list]
                    both_list = [item for sublist in both_list for item in sublist]
                    note = self._get_note(both_list)
                    print(note)
                    self._process_fingers_note(note)


    def rec_face(self):
        while True:
            self._camera_data.Record_data()
            self._camera_data.Get_is_mouth_open()
            
    
    
    def change_volume(self, loc):
        print(loc)
        self.volume = loc
        self._saxophone_player.change_volume(self.volume)     

    
###########################################################################################
#                                                                                         #
#                                 PRIVATE FUNCTIONS                                       #
#                                                                                         #
###########################################################################################


#==============================================#
#              HANDS FUNCTIONS                 #
#==============================================#


    def _get_hand_from_type(self, hands:list , type_of_hand: str) -> list:
        for hand in hands:
            if hand['type'] == type_of_hand:
                return hand


    def _hand_status(self, hands: list) -> list or None:
        if len(hands) > 1:
            hand1 = hands[0]
            hand2 = hands[1]
            hand_status = []
            hand_status = self._Get_hand_status(hand2, hand_status, self.fingers_points.get_left_finger_list())
            hand_status = self._Get_hand_status(hand1, hand_status, self.fingers_points.get_right_finger_list())
            return hand_status


    def _Get_hand_status(self, hand: list, hand_status: list, fingers_list):
        for finger in fingers_list:
            middle_x, middle_y = self._Get_finger_point_location(finger, hand["lmList"], self.fingers_points.FINGER_BASE_MIDDLE)
            self._draw_hands_rectangle(middle_x, middle_y)
            tip_x, tip_y = self._Get_finger_point_location(finger, hand["lmList"], self.fingers_points.FINGER_TIP)
            if tip_x is None or tip_y is None or middle_x is None or middle_y is None:
                hand_status.append(0)
                continue
            
            is_point_in = self._is_point_inside_rectangle(middle_x - self.rectangle_size, middle_y + self.rectangle_size, 
                                                    middle_x + self.rectangle_size, middle_y - self.rectangle_size, tip_x, tip_y)
            if is_point_in is True:
                hand_status.append(1)
            elif is_point_in is False:
                hand_status.append(0)
        return hand_status


#==============================================#
#             FINGERS FUNCTIONS                # 
#==============================================#

    
    def _get_hand_middle(self, list_of_fingers_location: list) -> tuple[int, int] or tuple[None, None]:
        if list_of_fingers_location == None:
            return None, None
        return list_of_fingers_location[0][self.fingers_points.X] , list_of_fingers_location[0][self.fingers_points.Y]
        

    def _Get_finger_point_location(self, finger_to_search: list, list_of_fingers_location: list, point_in_the_finger: int) -> tuple[int, int] or tuple[None, None]:
        if list_of_fingers_location == None:
            return None, None
        points = []
        for point in finger_to_search:
            try:
                points.append(list_of_fingers_location[point])
            except:
                return None, None
        return points[point_in_the_finger][self.fingers_points.X], points[point_in_the_finger][self.fingers_points.Y] 
        
    
    def _get_note(self, current_fingers):
        try:
            return self.notes_dict[str(current_fingers)]
        except:
            return None

    
#==============================================#
#              PROCESS FUNCTIONS               #
#==============================================#


    def _process_hand(self, right_hand, indexes, model):
        res_list = []
        decision_threshold = 0.5
        fingers_indexes = indexes
        for indexes in fingers_indexes:
            finger = right_hand[indexes[0]:indexes[1]]
            data = tf.stack([finger])
            res = model(data, training=False)
            if res[0][0] > decision_threshold:
                res_list.append(1)
            else:
                res_list.append(0)
        return res_list
        
        
    def _process_right_hand(self, right_hand):
        return self._process_hand(right_hand, self.fingers_points.get_hands_fingers_indexes(), self.right_hand_model)
        
    
    def _process_left_hand(self, left_hand):
        return self._process_hand(left_hand, self.fingers_points.get_hands_fingers_indexes(), self.left_hand_model)
    
    
    def _process_fingers_note(self, Note):
        self._current_note = Note
        if self._is_note_on is True:
            if Note != self._last_note or self._air_on is False:
                self._saxophone_player.stop_note(self.Notes_number[self._last_note])
                self._is_note_on = False
            else:
                return 
            
        elif self._is_note_on is False and self._current_note in self.Notes_number and self._air_on is True:
            self._saxophone_player.play_note(self.Notes_number[self._current_note])
            self._is_note_on = True
        self._last_note = Note
        
    
#==============================================#
#                STATICS METHODS               #
#==============================================#


    @staticmethod
    def _calc_distance_between_point(point_a, point_b):
        return math.dist(point_a, point_b)


    @staticmethod
    def _is_point_inside_rectangle(top_left_x, top_left_y, right_bottom_x, right_bottom_y, x, y):
        if (x > top_left_x and x < right_bottom_x and y > right_bottom_y and y < top_left_y) :
            return True
        return False 


#==============================================#
#            RECORD HANDS FUNCTIONS            #
#==============================================#


    def record_hands(self, file_name):
        with open(file_name, 'a') as fd:
            while True:
                writer = csv.writer(fd)
                hands, self._current_fingers, image = self._camera_data.Get_hands_status()
                self.image = image
                cv2.imshow("image", self.image)
                if hands:
                    if len(hands) >= 1:
                        right_hand = self._get_hand_from_type(hands, 'Right')
                        left_hand = self._get_hand_from_type(hands, 'Left')
                        if right_hand is None or 'left_hand' is None:
                            continue
                        flat_right_hand = [item for sublist in right_hand['lmList'] for item in sublist]
                        flat_left_hand = [item for sublist in left_hand['lmList'] for item in sublist]    
                        write_row = flat_right_hand[15:27]
                        write_row.append('0')                  
                        writer.writerow(write_row) 

