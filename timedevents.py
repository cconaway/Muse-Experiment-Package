
"""
This needs to be something that triggers timed thread events.


"""

import threading
import time
import schedule

class Scheduler():

    def __init__(self):
        schedule.every(3).seconds.do(self.run_threaded, print('Event', time.time()))
        

    def run_threaded(self, function):
        job_thread = threading.Thread(target=function)
        job_thread.start()

    def run(self):
        schedule.run_pending()