import sys
import time
import zmq
import random
from Classifier import Classifier
from signpy.core.Transformer import Transformer


def transformer_pipe(T, cr):
    model = './tests/my_model_convlstm.h5'
    myClassifier = Classifier(model)
    while True:
        data = cr.recv_json()['data']
        start_time = time.time()
        A, y = T.transform(data)
        A = A[:, 186:]
        res = myClassifier.predict(A)
        # TODO: INSERT NN
        print('Shape of data: {}'.format(A.shape))
        print('Prediction: {}'.format(res))
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
