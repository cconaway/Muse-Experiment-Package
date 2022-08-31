import sys

from pythonosc import osc_server
from pythonosc.dispatcher import Dispatcher

from processor import Processor

def main():
    server_ip = '127.0.0.1'
    server_port = 8000

    dispatch = Dispatcher

    raw_eeg = Processor()
    dispatch.map("/muse/eeg",raw_eeg.run)

    server = osc_server.ThreadingOSCUDPServer((server_ip, server_port), dispatcher=dispatch)
    server.serve_forever()

def shutdown():
    pass

if __name__ == "__main__":
    try: 
        main()
    except KeyboardInterrupt:
        shutdown()