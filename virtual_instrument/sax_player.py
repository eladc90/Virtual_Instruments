import pygame.midi
import time
from ctypes import cast, POINTER
import time
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
 
 
class Saxophone_Player:
    def __init__(self) -> None:
        instrument = 57
        pygame.init()
        pygame.midi.init()
        port = pygame.midi.get_default_output_id()
        print(port)
        self.player = pygame.midi.Output(port, 0)
        self.player.set_instrument(instrument)
        self.volume = 127
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
           IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume_set = cast(interface, POINTER(IAudioEndpointVolume))
    
    
    def change_volume(self, vol):
        if vol != 0:
            vol = vol * -1 
            dev = 380 - 245 
            vol = vol + 245
            vol = (vol/dev)
            self.volume_set.SetMasterVolumeLevel(vol, None)
            try:
                pass
            except Exception as ex:
                pass


    def play_note(self, note):
        self.player.note_on(note, self.volume)
        
        
    def stop_note(self, note):
        self.player.note_off(note, self.volume)
        
        
        
        
        