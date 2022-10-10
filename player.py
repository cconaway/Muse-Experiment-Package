
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
        
        #Gets sounds from wavefiles.
        self.sound_set = {}
        for wave_file in os.listdir('./wavefiles'):

            logging.debug("Found file {}".format(wave_file))
            sound = sa.WaveObject.from_wave_file('./wavefiles/{}'.format(wave_file))
            self.sound_set.setdefault(wave_file, sound)

        self.sound_log = []

    def _set_event_flag(self, event_flag):
        event_flag.set()

    def play_sound(self, *args):

        sound_name = args[0]
        logging.info('Playing {}'.format(sound_name))
        play_obj = self.sound_set[sound_name].play()
        play_obj.wait_done()  # Wait until sound has finished playing
        logging.info('{} Complete'.format(sound_name))
        self._set_event_flag(args[-1])

        self.sound_log.append(sound_name)

    def play_randomsound(self, *args):

        sound = random.choice(list(self.sound_set.values()))
        logging.info('Playing Random Sound {}'.format(sound))
        play_obj = sound.play()
        play_obj.wait_done()
        self._set_event_flag(args[-1])
        
        self.sound_log.append(sound)

