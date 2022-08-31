
import collections
import csv


class DataLogger(object):
    
    def __init__(self, filename=None):
        self.path = './'
        self.filename = filename

        self.batch = collections.deque()
        self.batchsize = 256 * 5 #every 5 seconds

    def write_to_file(self, *args):
        with open('{}{}.csv'.format(self.path, self.filename), 'w', newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['address', 'args']) #or something like this

    def batch_data(self, *args):
        self.batch.append(args)
        if len(self.batch) == self.batchsize:
            yield self.batch

