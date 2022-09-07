
"""
Half sine tone generator, half audio file player.

If the player is playing a sound, log it in the csv.
"""


import numpy as np
import threading
import pyaudio

class SoundPlayer(object):

    def __init__(self):
        self.audio_context = pyaudio.PyAudio()
        self.stream = ''

        fs = 44100       # sampling rate, Hz, must be integer
        duration = 1.0   # in seconds, may be float
        f = 440.0        # sine frequency, Hz, may be float
        self.samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

    def open_context(self):
        self.stream = self.audio_context.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                output=True)

    def write_to_stream(self):
        volume = 0.5
        self.stream.write(volume*self.samples)

        self.stream.stop_stream()
        self.stream.close()  
        self._terminate()

    def _terminate(self):
        self.audio_context.terminate()