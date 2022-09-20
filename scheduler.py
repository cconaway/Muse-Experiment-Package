
"""
This needs to be something that triggers timed thread events.


"""

import threading
import time

from apscheduler.schedulers.background import BackgroundScheduler

from player import SoundPlayer

class Scheduler():

    def __init__(self, event_flag):
        self.scheduler = BackgroundScheduler()
        self.run_experiment = True #Maintains the threading loops
        self.event_flag = event_flag #threading event flag

        sp = SoundPlayer()

        """Where jobs get added"""
        self.scheduler.add_job(self.printer, trigger='interval', seconds=3)
        #self.scheduler.add_job(sp.play_sound, args=['Tone2.wav'], trigger='interval' ,  seconds=7)
        self.scheduler.add_job(sp.play_randomsound, trigger='interval' ,  seconds=7)
        
        self.scheduler.add_job(self.end_experiment, trigger='interval', seconds=12, id='end_experiment')
    
    def run(self):
        self.scheduler.start()

    #Current Job - Temporary
    def printer(self):
        print("Hello there")
        self._set_event_flag()

        #find a way to send writes to function.
        
    #Ends Experiment
    def end_experiment(self):
        self.run_experiment = False
        self.scheduler.remove_job('end_experiment')
    

    def _set_event_flag(self):
        self.event_flag.set()

"""Need a way to log when a timed event happens within the data

    GET DATETIME of Current Date
    Then schedule the events based on the current dates. plus ttimedeltas?
    
    """

    #its possible that the event flag cant be set inside the class
    #instead pass it as an arg to the scheduled tasks.