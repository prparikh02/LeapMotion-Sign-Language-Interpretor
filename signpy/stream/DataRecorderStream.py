import json
import inspect
import os
import sys
curr_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
root_dir = os.path.abspath(os.path.join(curr_dir, '../'))
sys.path.insert(0, root_dir + '/lib')
import Leap
from RawDataListenerStream import RawDataListenerStream


class DataRecorder(object):
    """
    Read config format from json file and output recorded data to json files
    """

    def __init__(self, config_fp=None, write_to_file=False):
        self.label = None
        self.file_template = root_dir + '/../samples/' + 'sample_{}_{}.json'

    def _record(self):
        controller = Leap.Controller()
        listener = RawDataListenerStream()

        controller.add_listener(listener)
        try:
            sys.stdin.readline()
        except KeyboardInterrupt:
            pass
        finally:
            # Remove the sample listener when done
            controller.remove_listener(listener)