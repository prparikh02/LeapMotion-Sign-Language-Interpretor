import time
import zmq
from multiprocessing import Process, Queue
from signpy.streaming.StreamDataRecorder import StreamDataRecorder


def producer():
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    zmq_socket.connect('tcp://127.0.0.1:5559')
    # Start your result manager and workers before you start your producers
    sdr = StreamDataRecorder(socket=zmq_socket)
    sdr.begin_recording()

if __name__ == '__main__':
    producer()
