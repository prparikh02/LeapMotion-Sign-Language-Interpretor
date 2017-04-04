import json
import numpy as np
import operator
import pdb
from .. import Constants

"""
Sample usage:

opt = DataParserOpt()
myOpt = DataParserOpt(both=True, only_right=False, only_left=False)
myDataReader = DataReader(
    './src/mapping.txt', './samples/sample_b_1.json', myOpt)
a, y = myDataReader.extract_features()

"""


class DataReader(object):
    """
    Class that parse json file to numpy array, with some options
    Arguments:
    map_file: text file that defines the dictionary structure
    data: json data file
    Assume responsibility of caller to specify options
    If no option object is specified, then extract_features returns raw matrix.
    """

    def __init__(self, map_file, data, opt=None):
        self.A = np.zeros((1, 1))  # feature matrix
        self.y = np.zeros((1, 1))  # labels column vector
        self.map_file = map_file
        self.data = data
        self.opt = opt

    def _filter(self, nnz_idx, A, y):
        """
        Internal function, not to be used externally.
        Called when self.opt is not None
        indx: index of valid frames.
        """
        if self.opt is None:
            return A, y

        if self.opt.no_empty:
            A = A[nnz_idx, :]
            y = y[nnz_idx]

        # TODO: Defer feature mutation until the end of data transformation
        # if self.opt.only_left:
        #     A = A[:, :Constants.NUM_FEATURES_PER_HAND]
        # if self.opt.only_right:
        #     A = A[:, Constants.NUM_FEATURES_PER_HAND:]
        return A, y

    def extract_features(self):
        """
        Parse the JSON file and and place all samples as rows into a np array.
        Return feature array with corresponding label array
        """
        # place features names in feature_list
        with open(self.map_file) as f:
            feature_list = f.read().splitlines()

        # open JSON data in nested dictionary, D if self.data is filepath
        #   otherwise self.data is already list of frames
        if isinstance(self.data, basestring):
            with open(self.data) as f:
                D = json.load(f)
                self.from_file = True
        else:
            D = self.data
            self.from_file = False

        # get number of frames and features
        num_frames = len(D)
        num_feats = len(feature_list)

        # numpy data array
        A = np.zeros((num_frames, num_feats))
        y = np.empty(num_frames, dtype=object)
        # keep track of non zero frames
        nnz_idx = []

        for frame_idx in xrange(num_frames):
            frame = D[frame_idx]
            if frame['num_hands'] != 0 and frame['num_fingers'] % 5 == 0:
                nnz_idx.append(frame_idx)
            for feat_idx, feat in enumerate(feature_list):
                feat_keys = feat.split('.')[1:]
                try:
                    val = reduce(operator.getitem, feat_keys, frame)
                    A[frame_idx, feat_idx] = val
                    y[frame_idx] = frame['label'] if self.from_file else None
                except KeyError, e:
                    pass

        return self._filter(nnz_idx, A, y)


class DataParserOpt(object):
    """
    option object for DataReader object
    no_empty: get rid of empty frames or frames with number of fingers not
        divisible by 5, default to True
    only_right: only get right hand data, default to True
    only_left: only get left hand data, default to False
    # only_complete: only get frames with complete 5 fingers, default to True
    both: get both hands, default to false
    TODO: MORE OPTIONS HERE
    """

    # TODO: design decision... Could've been a dictionary. Not necessary a
    # class.

    def __init__(self, no_empty=True, only_complete=True,
                 only_right=True, only_left=False, both=False):
        self.no_empty = no_empty
        self.only_right = only_right
        self.only_left = only_left
        self.only_complete = only_complete
        self.both = both
        assert not (self.only_left and self.only_right)
        assert self.both is not (self.only_left or self.only_right)
