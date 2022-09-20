
"""
Audio Player

Needs to Log to Csv
"""

import threading
import os
import random

import simpleaudio as sa
import numpy as np

import logging

class SoundPlayer(object):

    def __init__(self):
        #self.wave_obj = sa.WaveObject.from_wave_file('sound.wav')

        self.sound_set = {}
        for wave_file in os.listdir('./wavefiles'):

            logging.debug("Found file {}".format(wave_file))
            sound = sa.WaveObject.from_wave_file('./wavefiles/{}'.format(wave_file))
            self.sound_set.setdefault(wave_file, sound)

    def play_sound(self, sound_name):

        
        logging.info('Playing {}'.format(sound_name))
        play_obj = self.sound_set[sound_name].play()
        play_obj.wait_done()  # Wait until sound has finished playing
        logging.info('{} Complete'.format(sound_name))

    def play_randomsound(self):

        "Have this have a label of the sound played."

        sound = random.choice(list(self.sound_set.values()))
        logging.info('Playing Random Sound {}'.format(sound))
        play_obj = sound.play()
        play_obj.wait_done()
