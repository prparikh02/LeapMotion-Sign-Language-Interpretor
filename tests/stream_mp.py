import time
from multiprocessing import Process, Queue
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


def transformer_pipe(T, q):
    start_time = time.time()
    while True:
        A, y = T.transform(q.get())
        print('{}\n{}'.format(A, A.shape))
        print('{}\n{}'.format(y, y.shape))
    end_time = time.time()
    print('time elapsed: {}'.format(end_time - start_time))


def stream_recorder(sdr):
    sdr.begin_recording()

if __name__ == '__main__':
    q = Queue()
    parent_conn, child_conn = Pipe()
    sdr = StreamDataRecorder(child_conn)
    T = Transformer(config_file='./tests/config.json',
                    feature_map='./tests/mapping.txt')
    p = Process(target=stream_recorder, args=(sdr,))
    p.start()
    transformer_pipe(T, q)
    p.join()
