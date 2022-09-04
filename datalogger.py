import queue

class DataLogger(queue.Queue):
    
    def __init__(self):
        super().__init__(maxsize=10)
    
    def set_message(self, address: str, *args): #sets into queue
        self.put(args)

    def record_message(self):
        return self.get()

    
"""Think through how to access the datalog and plana thread option"""