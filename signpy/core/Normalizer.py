import numpy as np
import re
from .. import Constants


class Normalizer(object):
    """
    This class offers various methods to normalize the data()

    Sample use:
    my_norm = Normalizer()
    X = np.load('data.npy')
    X_norm = my_norm.affine(X, out_file)
    """

    def __init__(self, map_file=Constants.DEFAULT_MAPPING_FILE):
        try:
            with open(map_file, 'r') as f:
                feature_map = f.read()
                self.features = \
                    [feat.strip() for feat in feature_map.splitlines()]
        except IOError:
            print('Could not find or open map file.')
            raise


    def affine_translation(self, X):
        """
        Performs affine translation of the hand coordinates by centering the
            palm at the origin.
        Input -
            X: Numpy array
            map_file: file containing feature mapping of input array X
        Output -
            X_aff: affinely translation of the input array, X
        """

        features = self.features

        palm_template = 'frame.hands.{}.palm_pos.{}'
        hands = ['left', 'right']
        pos = ['x', 'y', 'z']

        pos_bins = {key: [] for key in pos}

        pos_pattern = re.compile("^.*(\.[x-z])$")
        for idx, feat in enumerate(features):
            # discount non-positional (x,y,z) features
            if not pos_pattern.match(feat.strip()):
                continue
            pos_bins[feat[-1]].append(idx)

        # indices of left and right palm coordinates
        left_palm_idx = {
            k: features.index(palm_template.format('left', k)) for k in pos
        }
        right_palm_idx = {
            k: features.index(palm_template.format('right', k)) for k in pos
        }

        X_aff = np.copy(X)
        # for each frame
        for x in X_aff:
            # for each position coordinate (x, y, z)
            for k, indices in pos_bins.iteritems():
                # obtain coordinate k for appropriate hand's palm position
                diff_k_left = x[left_palm_idx[k]]
                diff_k_right = x[right_palm_idx[k]]
                # for each occurrence of coordinate k
                for idx in indices:
                    if idx < Constants.NUM_FEATURES_PER_HAND:
                        x[idx] -= diff_k_left
                    else:
                        x[idx] -= diff_k_right

        return X_aff
