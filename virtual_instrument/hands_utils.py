from dataclasses import dataclass
from virtual_instrument.sax_player import Saxophone_Player


class FINGERS_POINTS:
    X = 0
    Y = 1
    Z = 2
    FINGER_BASE = 0
    FINGER_BASE_MIDDLE = 1
    FINGER_TIP_MIDDLE = 2
    FINGER_TIP = 3
    def __init__(self) -> None:
        self.first  :list = [1, 2, 3, 4]     # thumb
        self.second :list = [5, 6, 7, 8]     # index finger
        self.third  :list = [9, 10, 11, 12]  # middle finger
        self.fourth :list = [13, 14, 15, 16] # ring finger
        self.fifth  :list = [17, 18, 19, 20] # little finger
        self.middle_hand: list = [0]
        

    def get_hands_fingers_indexes(self):
        hands_indexes = [[15, 27], [27, 39], [39, 51]]
        return hands_indexes
    
    
    def get_finger_as_list(self):
        return [self.first, self.second, self.third, self.fourth, self.fifth]
        
        
    def get_right_finger_list(self):
        return [self.second, self.third, self.fourth, self.fifth]
    
    
    def get_left_finger_list(self):
        return [self.second, self.third, self.fourth]
        
class Saxophone_fingering:
    FINGERING_LIST = { '[1, 1, 1, 1, 1, 1]': 'C',
                       '[1, 1, 1, 1, 1, 1]': 'D',
                       '[1, 1, 1, 1, 1, 0]': 'E',
                       '[1, 1, 1, 1, 0, 0]': 'F',
                       '[1, 1, 1, 0, 0, 0]': 'G',
                       '[1, 1, 0, 0, 0, 0]': 'A',
                       '[1, 0, 0, 0, 0, 0]': 'B',
                       '[0, 1, 0, 0, 0, 0]': 'C2',
                                              }    
    
    NOTES_NUMBER = {'C' :48,   
                    'D' :50,
                    'E' :52,
                    'F' :53,
                    'G' :55,
                    'A' :57,
                    'B' :59,
                    'C2':60,
                            }
     
