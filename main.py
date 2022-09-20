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
from datalogger import DataLogger
from scheduler import Scheduler


def main():
    """
    main loop:
        1. Establishes Log
        2. Establishes Server
        3. Create Datalog interface
        4. Create Threads - Start Server
        5. Begins Recording Thread on Input
    """

    logging_level = logging.INFO

    # Logging
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.getLogger().setLevel(logging_level)

    # Server Setup
    server_ip = '192.168.0.35'
    server_port = 8000
    dispatch = Dispatcher()

    #Datalog 
    datalog = DataLogger()
    reciever_event = threading.Event()
    scheduled_event = threading.Event()

    #Reciever - interfaces with the Muse out directly.
    def reciever(address: str, fixed_args, *args):

        #If Event is Set -> Place time and Args in Queue
        if fixed_args[1].is_set(): 
            rec_time = time.perf_counter() - fixed_args[0].start_time #gets recording time

            if fixed_args[2].is_set():
                logging.info('Scheduled Task has been added to log.')
                fixed_args[2].clear()

                scheduled_task = 'Task Completed'
            else:
                scheduled_task = None
            
            #Sets message to datalog
            fixed_args[0].set_message(rec_time, args[0], args[1], args[2], args[3], args[4], scheduled_task) #datalogger, event
        
    #Recorder pulls messages from the queue
    def recorder(datalogger):

        #Pull Message from Queue and Record
        return datalogger.record_message()

    #Server
    dispatch.map("/muse/eeg", reciever, datalog, reciever_event, scheduled_event)
    server = osc_server.BlockingOSCUDPServer((server_ip, server_port), dispatcher=dispatch)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    
    #Establish the CSV context for the recording.
    with open('data/test_3.csv', 'w') as file:
        writer = csv.writer(file)

        #Arm everything
        scheduler = Scheduler(event_flag=scheduled_event)
        
        #current sync barrier
        input("Press anything and enter to proceed") #The Current time sync is this.
        start_time = time.perf_counter()
        datalog.set_start_time(start_time)

        #Run it and set flags.
        reciever_event.set() #Triggers Receiver
        scheduler.run()

        while True: #Set to some time based event.
            val = recorder(datalogger=datalog) #Recorder to both get the datalog and the schedulers return.
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


"""Next up is setting Various wave file tests and names and recording to the log."""