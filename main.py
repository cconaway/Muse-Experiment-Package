import sys
from threading
import time
import concurrent.futures

from pythonosc import osc_server
from pythonosc.dispatcher import Dispatcher


from datalogger import DataLogger


def main():
    server_ip = '127.0.0.1'
    server_port = 8000
    dispatch = Dispatcher

    raw_eeg = DataLogger
    dispatch.map("/muse/eeg",raw_eeg.set_message)
    server = osc_server.ThreadingOSCUDPServer((server_ip, server_port), dispatcher=dispatch)

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        executor.submit(server.serve_forever)
        executor.submit(raw_eeg.record_message)

def shutdown():
    pass

if __name__ == "__main__":
    try: 
        main()
    except KeyboardInterrupt:
        shutdown()
