import json
import inspect
import os
import sys
curr_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
root_dir = os.path.abspath(os.path.join(curr_dir, '../'))
sys.path.insert(0, root_dir + '/lib')
import Leap
from RawDataListener import RawDataListener


class DataRecorder(object):
    """
    Read config format from json file and output recorded data to json files
    """

    def __init__(self):
        self.label = None
        self.file_template = root_dir + '/../samples/' + 'sample_{}_{}.json'

    def _record(self):
        controller = Leap.Controller()

        r = raw_input('Enter label: ')
        # TODO: Generalize labels to more than just letters
        if len(r) != 1 or not r.isalpha():
            print('Invalid label')
            return None
        self.label = r
        listener = RawDataListener(self.label)

        controller.add_listener(listener)
        try:
            sys.stdin.readline()
        except KeyboardInterrupt:
            pass
        finally:
            controller.remove_listener(listener)

        # Create appropriate file
        i = 0
        while os.path.exists(self.file_template.format(self.label, i)):
            i += 1
        filename = self.file_template.format(self.label, i)

        print('Writing to file')
        with open(filename, 'w') as fp:
            json.dump(listener.get_data(), fp, indent=4, sort_keys=True)
        print('Write finished')

    def begin_recording(self):
        prompt = 'Press ENTER to begin recording or CTRL+C to exit'
        while True:
            try:
                sel = raw_input(prompt)
            except KeyboardInterrupt:
                print('\nExiting')
                break
            self._record()
