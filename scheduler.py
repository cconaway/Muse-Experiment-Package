import threading
import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED

from player import SoundPlayer

class Scheduler():

    def __init__(self, event_flag, data_filename):
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_listener(self._listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        self.run_experiment = True #Maintains the threading loops
        self.event_flag = event_flag #threading event flag

        self.current_event = ''
        self.sp = SoundPlayer(data_filename)

        """Where jobs get added"""
        self.scheduler.add_job(self.printer, args=self.event_flag ,trigger='interval', seconds=3)
        
        self.scheduler.add_job(self.sp.play_sound, args=['Tone2.wav', self.event_flag], trigger='interval' ,  seconds=7)
        self.scheduler.add_job(self.sp.play_randomsound, args=self.event_flag, trigger='interval' ,  seconds=7)
        
        self.scheduler.add_job(self.end_experiment, trigger='interval', seconds=12, id='end_experiment')

    def get_current_event(self):
        return self.current_event
        
    def _listener(self, event):
        if not event.exception:
            job = self.scheduler.get_job(event.job_id)
            self.current_event = job.name

            print('logging current event', self.current_event)

    def run(self):
        self.scheduler.start()




    #Current Job - Temporary
    def printer(self, *args):
        print("Hello there")
        args[0].set() 


    #Ends Experiment
    def end_experiment(self):
        self.run_experiment = False
        self.scheduler.remove_job('end_experiment')
        self.sp.write_log_to_csv()
    

