# Import Standard Library
import sys
import threading
import time
import concurrent.futures
import logging
import csv

# Import Third Parties
from pythonosc import osc_server
from pythonosc.dispatcher import Dispatcher

# Import Internal Libraries
from datalogger import DataLogger, QHandler
from scheduler import Scheduler


def main():

    # Set Logging Level
    logging_level = logging.INFO

    # Configure Log Messages
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.getLogger().setLevel(logging_level)

    # Configure Server IP, Port and Initialize Dispatcher
    server_ip = '192.168.0.35'
    server_port = 8000
    dispatch = Dispatcher()

    # Configure Datalog and it's reciever flag
    datalog = DataLogger() #can it be cleared before we set things up.
    reciever_event = threading.Event()
    
    #Configure Qhandler for the Datalog
    q = QHandler()

    #Configure Scheduler and scheduler flag
    scheduled_event = threading.Event() #can events carry info? No so instead we put it to some global
    scheduler = Scheduler(event_flag=scheduled_event)

    # Mapping dispatch to events and schedules, Start Server Thread
    dispatch.map("/muse/eeg", q.reciever, datalog, reciever_event, scheduled_event, scheduler)
    server = osc_server.BlockingOSCUDPServer((server_ip, server_port), dispatcher=dispatch)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    # Establish the CSV context for the recording. Perform block sync.
    with open('data/test_3.csv', 'w') as file:
        writer = csv.writer(file)

        #Current sync barrier
        input("Press anything and enter to proceed") 
        start_time = time.perf_counter()
        datalog.set_start_time(start_time)

        #Run it and set flags.
        reciever_event.set() #Triggers Receiver
        scheduler.run()

        while True: #Set to some time based event.
            val = q.recorder(datalogger=datalog) #Recorder to both get the datalog and the schedulers return.
            if val:
                logging.debug("Output value is {}".format(val))
                writer.writerow(val)

            if scheduler.run_experiment == False:
                break

def shutdown():
    print('Shutting Down Experiment')

if __name__ == "__main__":
    try:
        main()
        shutdown()
    except KeyboardInterrupt:
        shutdown()

