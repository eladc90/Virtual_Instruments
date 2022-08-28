from finger_camera.rec_camera import Rec_Camera_Hand
from sax_player import Saxophone_Player



class Instrument_hands_processor:
    def __init__(self):
        self._camera_data = Rec_Camera_Hand()
        self._saxophone_player = Saxophone_Player()
        self._current_fingers = []
        self._prev_fingers = []
        self._current_note = 0
        self._fingering_list = {1:self._saxophone_player.play_do,
                                2:self._saxophone_player.play_re,}  
        
        self._stop_fingering_list = {1:self._saxophone_player.stop_do,
                                2:self._saxophone_player.stop_re,}  
        
    def Start(self):
        while True:
            hands, self._current_fingers = self._camera_data.Get_hands_status()
            if self._current_fingers == [0, 1, 0, 0, 0]:
                self._current_fingers = 1
            elif self._current_fingers == [0, 1, 1, 0, 0]:
                self._current_fingers = 2
            else:
                self._current_fingers = 0
                
            self._process_fingers()
            self._prev_fingers = self._current_fingers
        

    def _process_fingers(self):
        print(self._current_fingers, self._prev_fingers)
        if self._current_fingers != 0 and self._prev_fingers != self._current_fingers:
            try:
                self._fingering_list[self._current_fingers]()
                self._current_note = self._current_fingers
            except:
                pass
        elif self._current_fingers != self._prev_fingers:
            try:
                self._stop_fingering_list[self._current_note]()
            except:
                pass
    


