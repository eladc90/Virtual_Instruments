import pygame.midi
import time
from ctypes import cast, POINTER
import time
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
 
 
class Saxophone_Player:

    def __init__(self) -> None:
        instrument = 57
        device = 0
        self.note_C = 48   
        self.note_D = 50
        self.note_E = 52
        self.note_F = 53
        pygame.init()
        pygame.midi.init()
        port = pygame.midi.get_default_output_id()
        print(port)
        self.player = pygame.midi.Output(port, 0)
        self.player.set_instrument(instrument)
        self.volume = 127
        devices = AudioUtilities.GetSpeakers()
# print(devices)
        interface = devices.Activate(
           IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume_set = cast(interface, POINTER(IAudioEndpointVolume))
    
    
    def change_volume(self, vol):
        if vol != 0:
            vol = vol * -1 
            print(vol)
            dev = 380 - 245 
            vol = vol + 245
            print(vol)
            vol = (vol/dev)
            print(f'the final vol {vol}')
            # self.volume = int(vol)
            # self.player.change_vol(self.note_C, int(vol))
            self.volume_set.SetMasterVolumeLevel(vol, None) #max
            try:
                # print(pygame.midi.get_device_info(0))
                pass
            except Exception as ex:
                # print(ex)
                pass
                
            # print(type(self.channel1))
            # pygame.mixer.music.set_volume(0.8)
        
    
    def play_C(self):
        self.player.note_on(self.note_C, self.volume)
        
        
    def play_D(self):
        self.player.note_on(self.note_D, self.volume)
        

    def play_E(self):
        self.player.note_on(self.note_E, self.volume)
        
        
    def play_F(self):
        self.player.note_on(self.note_F, self.volume)
        
        
    def stop_C(self):
        self.player.note_off(self.note_C, self.volume)
        
        
    def stop_D(self):
        self.player.note_off(self.note_D, self.volume)
        
        
    def stop_E(self):
        self.player.note_off(self.note_E, self.volume)
        
        
    def stop_F(self):
        self.player.note_off(self.note_F, self.volume)
        
        
        
        
        