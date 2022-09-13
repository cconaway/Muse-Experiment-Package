
"""
Audio Player

Needs to Log to Csv
"""

import threading
import os
import random

import simpleaudio as sa
import numpy as np

class SoundPlayer(object):

    def __init__(self):
        #self.wave_obj = sa.WaveObject.from_wave_file('sound.wav')

        self.sound_set = []
        for wave_file in os.listdir('/wavefiles'):
            self.sound_set.append(sa.WaveObject.from_wave_file(wave_file))
            

    def play_sound(self, sound_name):
        print(sound_name)
        #play_obj = self.wave_obj.play()
        #play_obj.wait_done()  # Wait until sound has finished playing

    def play_randomsound(self):
        sound = random.choice(self.sound_set)
        #play_obj = sound.play()
        #play_obj.wait_done()


"""Todo:

    Create a .mp3/.wav player to play at specific times."""