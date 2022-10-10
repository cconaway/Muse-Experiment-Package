import queue
import logging
import threading
import time


class DataLogger(queue.Queue):
    """
    Modified Queue Object to set messages to queue and
    retrieve from the queue.
    """
    def __init__(self):
        super().__init__(maxsize=1024)
        self.start_time = 0

    def set_message(self, *args): #sets into queue

        logging.debug("Adding {} to queue".format(args))
        self.put(args)
        logging.debug("Added {} to queue, queue length {}".format(args, self.qsize()))

    def record_message(self):
        while not self.empty():
            logging.debug("About to record from queue")
            val = self.get()
            logging.debug("Got {} from queue, queue size is {}".format(val, self.qsize()))
            return val

    def set_start_time(self, time):
        self.start_time = time

class QHandler():

    def reciever(address: str, fixed_args, *args):
    
        #If Event is Set -> Place time and Args in Queue
        if fixed_args[1].is_set(): 
            rec_time = time.perf_counter() - fixed_args[0].start_time #gets recording time

            if fixed_args[2].is_set():
                fixed_args[2].clear()
                scheduled_task = fixed_args[3].get_current_event() #event data
                logging.info('Scheduled Task {} has been added to log.'.format(scheduled_task))

            else:
                scheduled_task = None

            fixed_args[0].set_message(rec_time, args[0], args[1], args[2], args[3], args[4], scheduled_task)


    def recorder(datalogger):
        #Pull Message from Queue and Record
        return datalogger.record_message()


