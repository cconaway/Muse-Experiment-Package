
"""
This needs to be something that triggers timed thread events.


"""

import threading
import time
from apscheduler.schedulers.background import BackgroundScheduler
from player import SoundPlayer

class Scheduler():

    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.run_experiment = True #Maintains the threading loops

        sp = SoundPlayer()

        """Where jobs get added"""
        self.scheduler.add_job(self.printer, trigger='interval', seconds=3)
        self.scheduler.add_job(sp.play_sound, args=['sound1'], trigger='interval' ,  seconds=6)
        self.scheduler.add_job(self.end_experiment, trigger='interval', seconds=12, id='end_experiment')
    
    def run(self):
        self.scheduler.start()

    #Current Job - Temporary
    def printer(self):
        print("Hello there")
        
    #Ends Experiment
    def end_experiment(self):
        self.run_experiment = False
        self.scheduler.remove_job('end_experiment')
        
"""Need a way to log when a timed event happens within the data"""