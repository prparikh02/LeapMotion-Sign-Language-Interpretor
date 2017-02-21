import json
import inspect
import os
import sys
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
root_dir = os.path.abspath(os.path.join(src_dir, '../'))
sys.path.insert(0, root_dir + '/lib')
import Leap
from RawDataListener import RawDataListener


class DataRecorder(object):
    """
    Read config format from json file and output recorded data to json files
    """

    def __init__(self, config_fp=None, write_to_file=False):
        self.data = None
        self.label = None
        self.file_template = root_dir + '/samples/' + 'sample_{}_{}.json'

    def _record_(self):
        controller = Leap.Controller()
        listener = RawDataListener()

        r = raw_input('Enter label: ')
        # TODO: Generalize labels to more than just letters
        if len(r) != 1 or not r.isalpha():
            print('Invalid label')
            return
        self.label = r

        # Create appropriate file
        i = 0
        while os.path.exists(self.file_template.format(self.label, i)):
            i += 1
        filename = self.file_template.format(self.label, i)

        controller.add_listener(listener)
        try:
            sys.stdin.readline()
        except KeyboardInterrupt:
            pass
        finally:
            # Remove the sample listener when done
            controller.remove_listener(listener)

        with open(filename, 'w') as fp:
            json.dump(listener.get_data(), fp, indent=4, sort_keys=True)

        # TODO insert code to either file generator or to classifier

    def begin_recording(self):
        while True:
            try:
                prompt = 'Press ENTER to begin recording or CTRL+C to exit'
                sel = raw_input(prompt)
            except KeyboardInterrupt:
                print('\nExiting')
                break
            self._record_()
