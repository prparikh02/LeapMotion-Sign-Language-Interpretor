import sys
import time
import zmq
import random
from signpy.core.Transformer import Transformer


def transformer_pipe(T, cr):
    while True:
        data = cr.recv_json()['data']
        start_time = time.time()
        A, y = T.transform(data)
        # print('{}\n{}'.format(A, A.shape))
        # print('{}\n{}'.format(y, y.shape))
        print('Shape of data: {}'.format(A.shape))
        print('Labels: {}'.format(y.shape))
        end_time = time.time()
        print('Time elapsed for processing: {}'.format(end_time - start_time))


def consumer():
    context = zmq.Context()
    # recieve work
    consumer_receiver = context.socket(zmq.PULL)
    consumer_receiver.connect('tcp://127.0.0.1:5560')

    T = Transformer(config_file='./tests/config.json',
                    feature_map='./tests/mapping.txt')
    transformer_pipe(T, consumer_receiver)

if __name__ == '__main__':
    consumer()
