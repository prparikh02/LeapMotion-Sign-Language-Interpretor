from signpy.streaming.StreamDataRecorder import StreamDataRecorder
from multiprocessing import Process, Pipe
from flask import Flask, render_template, jsonify


app = Flask(__name__)
prod = None


@app.route('/poll')
def poll():
    p = prod.recv()
    if isinstance(p, str):
        p = {'message': p}
    else:
        p = {k: str(v) for k, v in p}
    print p
    return jsonify(p)

@app.route('/')
def hello():
    return render_template('index.html')

def web_app(dummy):
    app.run()

if __name__ == '__main__':
    consumer, producer = Pipe()
    prod = producer
    sdr = StreamDataRecorder(consumer)
    p = Process(target=web_app, args=(None,))
    p.start()
    sdr.begin_recording()
    p.join()
