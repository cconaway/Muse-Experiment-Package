import queue
import logging
import threading


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

            




