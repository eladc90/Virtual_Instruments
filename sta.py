# import library ---------------------------------------------------------------
import pygame.midi
import time

# define all the constant values -----------------------------------------------
device = 0     # device number in win10 laptop
instrument = 57 # http://www.ccarh.org/courses/253/handout/gminstruments/
note_Do = 48   # http://www.electronics.dit.ie/staff/tscarff/Music_technology/midi/midi_note_numbers_for_octaves.htm
note_Re = 50
note_Me = 52
volume = 127
wait_time = 4

# initize Pygame MIDI ----------------------------------------------------------
pygame.midi.init()

# set the output device --------------------------------------------------------
player = pygame.midi.Output(device)

# set the instrument -----------------------------------------------------------
player.set_instrument(instrument)

# play the notes ---------------------------------------------------------------
player.note_on(note_Do, volume)
time.sleep(wait_time)
player.note_off(note_Do, volume)

player.note_on(note_Re, volume)
time.sleep(wait_time)
player.note_off(note_Re, volume)

player.note_on(note_Me, volume)
time.sleep(wait_time)
# player.note_off(note_Me, volume)

# close the device -------------------------------------------------------------
del player
pygame.midi.quit()