from multiprocessing import Process, Queue
from signpy.core.stream.RawDataListenerStream import RawDataListenerStream
from signpy.core.stream.DataRecorderStream import DataRecorderStream
import sys
import time 


def record(interval, queue):
    recorder = DataRecorderStream()
    recorder._record()
    time.sleep(interval)
    queue.put(recorder.get_data())


def keyboard_listener(interval, queue):
    try:
        queue.put(raw_input('Enter from the Keyboard: '))
    except EOFError:
        queue.put("No Keyboard Input Detected during Interval!")

def catcher(n, interval, queue):
    print 'Time Elapsed: %f: Output: %s' % (n*interval, queue.get())

def main(interval = 1):
    
    if __name__ == '__main__':
    
        print 'Starting Record Phase'
        queue = Queue()

        n = 1
        while True:
            try:
                record_process = Process(target = record, args = (interval,queue,))
                record_process.start()

                catcher_process = Process(target = catcher, args = (n, interval, queue,))
                time.sleep(interval)

                catcher_process.start()
                keyboard_process.join()
                catcher_process.join()
                n += 1
            except KeyboardInterrupt:
                print '\nKeyboard Interrupt; Session Ended!'
                break

main(5)
    
