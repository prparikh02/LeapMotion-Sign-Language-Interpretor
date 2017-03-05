from __future__ import division
import numpy as np
import json
import math


class DataSampler(object):

    def __init__(self, data, method, *method_args):
        self.data = data  # np matrix; m samples, n features
        self.data_length = data.shape[0]
        self.method = method
        self.method_args = method_args

        if self.method == 'uniform_sampling':
            self.__class__.__call__ = self.uniform_sampling(
                *(self.method_args))
        elif self.method == 'random_sampling':
            self.__class__.__call__ = self.random_sampling(*(self.method_args))

    def uniform_sampling(self, method='rate', value=None):
        """
        Inputs: data - an m, n dimension matrix (m samples, n features)
                method - a string param which specifies the type of uniform sampling
                       - 'rate' => uniform sampling rate (every k frames)
                       - 'num_frames' => determine a uniform rate 'k' as length_of_data/num_frames
                value  - integer value the particular method utilizes

        Outputs: data matrix (m', n), where m' is the new number of data points
        """

        if value is None or not isinstance(value, (int, long)):
            print "The rate and number of frames should be a positive integer!"
            return None

        if value > self.data_length:
            value = self.data_length

        if method == 'rate' and value > 0 and isinstance(value, (int, long)):
            return self.data[0::value]
        elif method == 'num_frames' and value > 0 and isinstance(value, (int, long)):
            new_data = self.data[0::int(math.floor(self.data_length / value))]
            if self.data_length > value:
                new_data = new_data[0:value]
            return new_data

    def random_sampling(self, num_frames=None):
        """
        Inputs: data - an m, n dimension matrix (m samples, n features)
                num_frames - if num_frames < m, num_frames randomly sampled frames are complied without replacement

        Outputs: data matrix (m', n), where m' is the new number of data points
        """

        if num_frames is None or not isinstance(num_frames, (int, long)):
            print "The number of frames should be a positive integer!"
            return None

        if num_frames > self.data_length:
            num_frames = self.data_length

        return self.data[np.random.choice(self.data_length, num_frames, replace=False), :]
