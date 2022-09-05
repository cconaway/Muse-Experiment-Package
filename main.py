import sys
import threading
import time
import concurrent.futures
import logging

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

    def reciever(address: str, datalogger, *args):
        datalogger[0].set_message(args)
        
    def recorder(datalogger):
        datalogger.record_message()

    datalog = DataLogger()
    dispatch.map("/muse/eeg", reciever, datalog)
    server = osc_server.BlockingOSCUDPServer((server_ip, server_port), dispatcher=dispatch)

    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    
    while True: 
        recorder(datalogger=datalog)
        

def shutdown():
    pass

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        shutdown()
