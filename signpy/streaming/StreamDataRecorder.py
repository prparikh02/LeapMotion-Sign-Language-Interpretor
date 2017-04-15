import inspect
import os
import sys
import time
curr_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
root_dir = os.path.abspath(os.path.join(curr_dir, '../'))
sys.path.insert(0, root_dir + '/lib')
import Leap
# from multiprocessing import Process, Pipe
from StreamRawDataListener import StreamRawDataListener
from Classifier import Classifier
from ..core.Transformer import Transformer


# to be used with stream_serial.py
def transformer_pipe(T, classifier, data):
    start_time = time.time()
    A, y = T.transform(data)
    print('time elapsed (transformation): {}'.format(time.time() - start_time))
    start_time = time.time()
    # TODO: Remove left hand features in transformer
    A = A[:, 186:]
    res = classifier.predict(A)
    print('Shape of data: {}'.format(A.shape))
    print('Prediction: {}'.format(res))
    print('time elapsed (prediction): {}'.format(time.time() - start_time))
    sys.stdout.flush()


class StreamDataRecorder(object):
    '''
    Read frames from Leap and batch pipe to transformer without going to file
    '''

    def __init__(self, comm=None):
        self.controller = Leap.Controller()
        self.comm = comm  # to be used with stream_multiprocess.py

        ''' to be used with stream_serial.py '''
        self.T = Transformer(config_file='./tests/config.json',
                             feature_map='./tests/mapping.txt')
        model = './signpy/streaming/my_model_convlstm.h5'
        self.classifier = Classifier(model)

    def _record(self, interval=3):
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
                # to be used with stream_producer.py
                # self.comm.send_json({
                #     'data': data
                # })
                # to be used with stream_multiprocess.py
                # self.comm.send(data)
                transformer_pipe(self.T, self.classifier, data)
                if terminate:
                    break
            except KeyboardInterrupt:
                break
        # self.comm.close()  # to be used with stream_multiprocess.py
        print('\nExiting')
