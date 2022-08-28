import pygame.midi
import time

class Saxophone_Player:

    def __init__(self) -> None:
        instrument = 57
        device = 0
        self.note_Do = 48
        self.note_Re = 50
        pygame.midi.init()
        self.player = pygame.midi.Output(device)
        self.player.set_instrument(instrument)
        self.volume = 127
    
    def play_do(self):
        self.player.note_on(self.note_Do, self.volume)
        
        
    def stop_do(self):
        self.player.note_off(self.note_Do, self.volume)
        
        
    def play_re(self):
        self.player.note_on(self.note_Re, self.volume)
        
        
    def stop_re(self):
        self.player.note_off(self.note_Re, self.volume)
        
        
        