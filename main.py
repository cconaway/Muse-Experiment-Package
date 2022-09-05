import sys
import threading
import time
import concurrent.futures
import logging
import csv

from pythonosc import osc_server
from pythonosc.dispatcher import Dispatcher


from datalogger import DataLogger


def main():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.getLogger().setLevel(logging.DEBUG)

    server_ip = '192.168.0.35'
    server_port = 8000
    dispatch = Dispatcher()

    def reciever(address: str, fixed_args, *args):
        
        if fixed_args[1].is_set():
            """Set time here somehow"""

            rec_time = time.perf_counter() - fixed_args[0].start_time

            fixed_args[0].set_message(rec_time, args[0], args[1], args[2], args[3], args[4]) #datalogger, event
        
    def recorder(datalogger):
        return datalogger.record_message()
        

    datalog = DataLogger()
    event = threading.Event()
    dispatch.map("/muse/eeg", reciever, datalog, event)
    server = osc_server.BlockingOSCUDPServer((server_ip, server_port), dispatcher=dispatch)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    
    with open('test.csv', 'w') as file:
        writer = csv.writer(file)
        input("Press anything and enter to proceed")
        
        start_time = time.perf_counter()
        datalog.set_start_time(start_time)
        event.set()

        while True: #This will need to change into some time based event thing.
            
            val = recorder(datalogger=datalog)
            
            if val:
                logging.debug("Output value is {}".format(val))
                writer.writerow(val)


            


        

def shutdown():
    pass

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        shutdown()
