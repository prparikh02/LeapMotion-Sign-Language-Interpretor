import json
import numpy as np
import operator


class DataReader(object):

    def __init__(self, map_file, data_file):
        self.A = np.zeros((1, 1))  # feature matrix
        self.y = np.zeros((1, 1))  # labels column vector
        self.map_file = map_file
        self.data_file = data_file

    def extract_features(self):
        """
        Parse the JSON file and and place all samples as rows into a Numpy array
        Return feature array with corresponding label array
        """

        # place features names in F
        with open(self.map_file) as f:
            feature_list = f.read().splitlines()

        # open JSON data in nested dictionary, D
        with open(self.data_file) as f:
            D = json.load(f)

        # get number of frames and features
        num_frames = len(D)
        num_feats = len(feature_list)

        # numpy data array
        A = np.zeros((num_frames, num_feats))
        y = ['' for i in xrange(num_frames)]

        for frame_idx in xrange(num_frames):
            y[frame_idx] = D[frame_idx]['timestamp']
            for feat_idx, feat in enumerate(feature_list):
                feat_keys = feat.split('.')[1:]
                try:
                    val = reduce(operator.getitem, feat_keys, D[frame_idx])
                    A[frame_idx, feat_idx] = val
                except KeyError, e:
                    # print('KeyError: {} in frame {}'.format(e, frame))
                    pass

        return A, y
