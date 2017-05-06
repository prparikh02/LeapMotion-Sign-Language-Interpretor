# LeapMotion-Sign-Language-Interpretor
Rutgers ECE Capstone Project - Spring 2017
## Abstract
American Sign Language is one of the most popular non-English languages used today in America. A valuable device would be able to translate sign language into spoken words to ease the communication barrier between people who only know sign language and people who only know English. Microsoft has demonstrated a sign language interpreter using its Kinect product, though the device had trouble identifying all the fingers so we intend to improve upon their results by using the Leap Motion device to make a sign language interpreter. We find Leap to be more desirable as it focuses on only finger/hand movements and is smaller and more portable. Furthermore, it is cheaper and operates easily on the three major operating systems. We use a recurrent neural network to train and analyze sign language data input from the Leap. We observe 372 features from the hand including the three dimensional coordinates of all the joints in the hand and the center of the palm. We have achieved 95\% accuracy over 26 classes, namely the letters of the alphabet.

The repository contains the following modules:
  * Data recording: records and formats raw input from the leap motion to json file.
  * Transformer: vectorizes json files to numpy array for training
  * Recurrent neural network: further processing data as well as the network architecture.
  * Real time module: code that facilitates the real time working of the system, including streaming, classifying, and user interface.

## Data recording
To start recording, navigate to root folder `LeapMotion-Sign-Language-Interpretor`, start an ipython shell, then

```python
from signpy.core.DataRecorder import DataRecorder

myrecorder = DataRecorder()

myrecorder.begin_recording()
```

Then *Enter* to begin. You would have to input a letter label, then it will start recording. The output json file is stored in the *samples* folder.

## Transformer
TODO: fill something here

## RNN
The formated data (in .npy format) used in the training can be found in the link below:
data: https://drive.google.com/open?id=0BwXFTV4JYj9rYXFYSW44aDNLcW8
label: https://drive.google.com/open?id=0BwXFTV4JYj9rQWE1dHB5ZjRuVTA

If you are interested in the conversion from json to these npy please take a look at *signpy/core/data_partition.ipynb*.

The training happens in *signpy/core/RNN.py*, where it performs 5 fold cross validation on the whole dataset and outputs a model file. This model file can be loaded later for real-time classification. It also outputs a history file that records the accuracy in each fold.

## Real time module

The data recording module combines a basic user interface with our extended Leap API through the Flask framework. To run a real time streaming module on a trained classifier, use the following script: `stream_serial_webapp.py` found in `LeapMotion-Sign-Language-Interpretor/tests/`. This file serves as a main method which stitches a streaming object (from `signpy.streaming.StreamDataRecorder/StreamDataRecorder` with a Flask server through the Multiprocessing python module.

Point your browser to the localhost to view an automatically updated probability distribution of the predictions. The default time window is 3.5 seconds to make a prediction. This parameter can be modified in the _record() method within `StreamDataRecorder`. `stream_serial_webapp.py` should be modified to take in a default interval parameter, which gets passed to `StreamDataRecorder.begin_recording()`.
