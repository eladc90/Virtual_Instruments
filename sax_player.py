import pygame.midi
import time

class Saxophone_Player:

    def __init__(self) -> None:
        instrument = 57
        device = 0
        self.note_C = 48   
        self.note_D = 50
        self.note_E = 52
        self.note_F = 53
        pygame.midi.init()
        self.player = pygame.midi.Output(device)
        self.player.set_instrument(instrument)
        self.volume = 127
    
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
        
        
        
        
        