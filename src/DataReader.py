import json
import numpy as np
import operator
import pdb


class DataReader(object):
    """
    Class that parse json file to numpy array, with some options
    Arguments:
    map_file: text file that defines the dictionary structure
    data_file: json data file
    Assume responsibility of caller to specify options
    """

    def __init__(self, map_file, data_file, opt=None):
        self.A = np.zeros((1, 1))  # feature matrix
        self.y = np.zeros((1, 1))  # labels column vector
        self.map_file = map_file
        self.data_file = data_file
        if opt is None:
            self.opt = DataParserOpt()
        # if self.opt.only_left is True:
        #     assert self.opt.only_right is False
        # if self.opt.only_right:
        #     assert self.opt.only_left is False
        # assert type(opt) is DataParserOpt

    def extract_features(self):
        """
        Parse the JSON file and and place all samples as rows into a Numpy array
        Return feature array with corresponding label array
        """

        # place features names in F
        with open(self.map_file) as f:
            # if self.opt.only_left:
            feature_list = f.read().splitlines()

        # open JSON data in nested dictionary, D
        with open(self.data_file) as f:
            D = json.load(f)

        # get number of frames and features
        num_frames = len(D)
        num_feats = len(feature_list)
        print num_frames
        # print feature_list[0].split('.')
        # numpy data array
        A = np.zeros((num_frames, num_feats))
        # keep track of non zero frames
        nnz_idx = []
        # y = np.zeros((num_frames,))
        y = ['' for i in xrange(num_frames)]
        # A = np.zeros([1, num_feats])
        # y = []
        for frame_idx in xrange(num_frames):
            # y[frame_idx] = D[frame_idx]['timestamp']
            # y[frame_idx] = D[frame_idx]['label']
            if D[frame_idx]['num_hands'] != 0 and D[frame_idx]['num_fingers'] % 5 == 0:
                nnz_idx.append(frame_idx)
            for feat_idx, feat in enumerate(feature_list):
                feat_keys = feat.split('.')[1:]
                # if self.opt.no_empty and D[frame_idx]['num_hands'] == 0:
                #     continue
                # if there is atleast 1 hand -> non empty frame, add to list

                # y.append(D[frame_idx]['label'])
                try:
                    val = reduce(operator.getitem, feat_keys, D[frame_idx])
                    # A = np.vstack((A, val))
                    A[frame_idx, feat_idx] = val
                    y[frame_idx] = D[frame_idx]['label']
                    # pdb.set_trace()
                    # y.append(D[frame_idx]['label'])
                except KeyError, e:
                    # print('KeyError: {} in frame {}'.format(e, frame))
                    pass
        if self.opt.no_empty:
            # pass
            print len(nnz_idx)
            A = A[nnz_idx, :]
            y = [y[i] for i in nnz_idx]
        if self.opt.only_left:
            A = A[:, :186]
        if self.opt.only_right:
            A = A[:, 186:]
        # if self.opt.r
        return A, y


class DataParserOpt(object):
    """
    option object for DataReader object
    no_empty: get rid of empty frames or frames with number of fingers not divisible by 5
        , default to True
    only_right: only get right hand data, default to True
    only_left: only get left hand data, default to False
    # only_complete: only get frames with complete 5 fingers, default to True
    both: get both hands, default to false
    TODO: MORE OPTIONS HERE
    """

    def __init__(self, no_empty=True, only_right=True, only_left=False, both=False):
        self.no_empty = no_empty
        self.only_right = only_right
        self.only_left = only_left
        # self.only_complete = only_complete
        self.both = both
        assert self.only_left is not self.only_right
        assert self.both is not (self.only_left or self.only_right)
