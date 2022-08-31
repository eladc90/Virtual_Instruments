from re import L
from finger_camera.rec_camera import Rec_Camera_Hand
from virtual_instrument.sax_player import Saxophone_Player
from virtual_instrument.hands_utils import *
import math
import cv2


class Instrument_hands_processor:
    def __init__(self, source=0):
        self._camera_data = Rec_Camera_Hand(source)
        self._saxophone_player = Saxophone_Player()
        self._current_fingers = []
        self._prev_fingers = []
        self._last_note = ''
        self._current_note = ''
        self._is_note_on = False
        self._current_fingers_note = None
        self.fingers_points = FINGERS_POINTS()
        self.volume = 400
        self.notes_dict = Saxophone_fingering.FINGERING_LIST
        self.Notes_number = Saxophone_fingering.NOTES_NUMBER
        self.rectangle_size = 10
        self.image = None
        self.thickness = 3
        
    def Start(self):
        while True:
            hands, self._current_fingers, image = self._camera_data.Get_hands_status()
            self.image = image
            if hands:
                self._current_fingers = self._hand_status(hands)
                print(self._current_fingers)
                cv2.imshow("image", self.image)
                self._current_note = self._get_note(self._current_fingers)
                self._process_fingers(self._current_note)
                self._last_note = self._current_note
                
                
    def _draw_hands_rectangle(self, middle_x, middle_y):
        self.image = cv2.rectangle(self.image, (middle_x - self.rectangle_size, middle_y + self.rectangle_size),
                                            (middle_x + self.rectangle_size, middle_y - self.rectangle_size),
                                            color=(0, 255, 0), thickness=self.thickness)
        
        
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
            middle_x, middle_y = self._Get_finger_point_location(finger, hand["lmList"], self.fingers_points.FINGER_TIP_MIDDLE)
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
#               FINGER GETTERS                 # 
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
    
    
    def _process_fingers(self, Note):
        if self._is_note_on is True:
            if Note != self._last_note:
                self._saxophone_player.stop_note(self.Notes_number[self._last_note])
                self._is_note_on = False
            else:
                return 
            
        elif self._is_note_on is False and self._current_note in self.Notes_number:
            self._saxophone_player.play_note(self.Notes_number[self._current_note])
            self._is_note_on = True
        
    
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
        
