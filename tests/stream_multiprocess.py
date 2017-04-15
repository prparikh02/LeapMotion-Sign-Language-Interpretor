import sys
import time
from multiprocessing import Process, Pipe
from Classifier import Classifier
from signpy.core.Transformer import Transformer
from signpy.streaming.StreamDataRecorder import StreamDataRecorder

'''
== DO NOT USE ==
There is an issue with this procedure in that when the Leap Listener
    is spawned in a new process by the multiprocessing module, the leap
    device never calls the 'on_connect()' callback function. This could be an
    issue with hardware connectivity after spawning a new process. To be
    determined.
'''


def transformer_pipe(T, comm, classifier):
    while True:
        data = comm.recv()
        sys.stdout.flush()
        start_time = time.time()
        A, y = T.transform(data)
        # TODO: Remove left hand features in transformer
        A = A[:, 186:]
        res = classifier.predict(A)
        print('Shape of data: {}'.format(A.shape))
        print('Prediction: {}'.format(res))
        print('time elapsed: {}'.format(time.time() - start_time))


def stream_recorder(sdr):
    sdr.begin_recording()

if __name__ == '__main__':
    consumer, producer = Pipe()
    sdr = StreamDataRecorder(consumer)
    T = Transformer(config_file='./tests/config.json',
                    feature_map='./tests/mapping.txt')
    model = './tests/my_model_convlstm.h5'
    classifier = Classifier(model)
    p = Process(target=transformer_pipe, args=(T, producer, classifier))
    # p = Process(target=stream_recorder, args=(sdr,))
    p.start()
    stream_recorder(sdr)
    # transformer_pipe(T, producer, classifier)
    p.join()
