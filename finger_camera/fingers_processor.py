from finger_camera.rec_camera import Rec_Camera_Hand
from sax_player import Saxophone_Player



class Instrument_hands_processor:
    
    notes_dict = {'[0, 1, 0, 0, 0]': 'C',
                  '[0, 1, 1, 0, 0]': 'D',
                  '[0, 1, 1, 1, 0]': 'E',
                  '[0, 1, 1, 1, 1]': 'F',
                                        }
                    
    def __init__(self):
        self._camera_data = Rec_Camera_Hand()
        self._saxophone_player = Saxophone_Player()
        self._current_fingers = []
        self._prev_fingers = []
        self._last_note = ''
        self._current_note = ''
        self._is_note_on = False
        self._current_fingers_note = None
        
        
        self.Notes_on_dict = {  'C': self._saxophone_player.play_C,
                                'D': self._saxophone_player.play_D,
                                'E': self._saxophone_player.play_E,
                                'F': self._saxophone_player.play_F
                        }
        
        self.Notes_off_dict = { 'C': self._saxophone_player.stop_C,
                                'D': self._saxophone_player.stop_D,
                                'E': self._saxophone_player.stop_E,
                                'F': self._saxophone_player.stop_F
                        }
        
    def Start(self):
        while True:
            hands, self._current_fingers = self._camera_data.Get_hands_status()
            self._current_note = self._get_note(self._current_fingers)
            print(self._current_note)
            self._process_fingers(self._current_note)
            self._last_note = self._current_note
        
        
    def _get_note(self, current_fingers):
        try:
            return self.notes_dict[str(current_fingers)]
        except:
            return None
    
    
    def _process_fingers(self, Note):
        if self._is_note_on is True:
            if Note != self._last_note:
                print('stopping note')
                self.Notes_off_dict[self._last_note]()
                self._is_note_on = False
            else:
                print("do nothing")
                return 
            
        elif self._is_note_on is False and self._current_note in self.Notes_on_dict:
            self.Notes_on_dict[self._current_note]()
            self._is_note_on = True
        
    


