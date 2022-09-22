from finger_camera.rec_camera import Rec_Camera_Hand
from virtual_instrument.fingers_processor import Instrument_hands_processor
from virtual_instrument.sax_player import Saxophone_Player


def start_playing():
    player = Instrument_hands_processor()
    # player = Instrument_hands_processor(1) # if using phone camera
    # player.rec_face()
    player.Start()
    
    
if __name__ == "__main__":
    start_playing()