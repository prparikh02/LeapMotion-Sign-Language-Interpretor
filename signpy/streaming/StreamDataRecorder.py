import inspect
import os
import sys
curr_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
root_dir = os.path.abspath(os.path.join(curr_dir, '../'))
sys.path.insert(0, root_dir + '/lib')
import Leap
from multiprocessing import Process, Queue
from StreamRawDataListener import StreamRawDataListener
import time


class StreamDataRecorder(object):
    '''
    Read frames from Leap and batch pipe to transformer without going to file
    '''

    def __init__(self, socket=None):
        self.controller = Leap.Controller()
        self.socket = socket

    def _record(self, interval=5):
        terminate = False
        listener = StreamRawDataListener()
        self.controller.add_listener(listener)
        t_end = time.time() + interval
        try:
            while time.time() < t_end:
                pass
        except KeyboardInterrupt:
            terminate = True
        self.controller.remove_listener(listener)
        return listener.get_data(), terminate

    def begin_recording(self):
        prompt = 'Press Enter to begin recording or CTRL+C to exit'
        try:
            sel = raw_input(prompt)
        except KeyboardInterrupt:
            print('\nExiting')
            return
        except EOFError as e:
            print('\n{}'.format(e))
        while True:
            try:
                data, terminate = self._record()
                print('Data collected of shape: {}'.format(len(data)))
                self.socket.send_json({
                    'data': data
                })
                if terminate:
                    break
            except KeyboardInterrupt:
                break
        print('\nExiting')
