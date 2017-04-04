from __future__ import division
import numpy as np
from types import *
from .. import Constants


class DataSampler(object):

    def __init__(self, data, labels, method='uniform_rate', **kwargs):
        self.data = data
        self.labels = labels
        self.method, self.method_args = self._resolve_method(method, kwargs)

    def _resolve_method(self, method, method_args):
        if method == 'uniform_rate':
            if 'k' in method_args:
                return self._uniform_rate, method_args['k']
            return self._uniform_rate, None
        elif method == 'uniform_number':
            if 'N' in method_args:
                return self._uniform_number, method_args['N']
            return self._uniform_number, None
        elif method == 'simple_random':
            if 'N' in method_args:
                return self._simple_random, method_args['N']
            return self._simple_random, None
        elif method == 'prob':
            if 'p' in method_args:
                return self._prob, method_args['p']
            return self._prob, None
        print ('Using default method: {}'.format('uniform_rate'))
        return self._uniform_rate, None

    def _uniform_rate(self, k=None):
        if not k or k > self.data.shape[0]:
            return self._uniform_number()
        assert type(k) is IntType, 'k is not an integer: {}'.format(k)
        return self.data[::k], self.labels[::k]

    def _uniform_number(self, N=None):
        """
        Discouraged from because if N does not divide number of samples
            nicely, the sampling is heavily skewed
        """
        num_frames = self.data.shape[0]
        if not N:
            N = int(np.floor(
                Constants.DEFAULT_SAMPLE_PERCENTAGE * num_frames
            ))
            k = int(np.floor(num_frames / N))
            if k == 0:
                k = 1
        elif N > num_frames:
            k = 1
        else:
            assert type(N) is IntType, 'N is not an integer: {}'.format(N)
            k = int(np.floor(num_frames / N))

        # ensure that at most N samples are taken if N does not divide nicely
        return self.data[::k][:N], self.labels[::k][:N]

    def _simple_random(self, N=None):
        num_frames = self.data.shape[0]
        if not N or N > num_frames:
            N = int(np.floor(
                Constants.DEFAULT_SAMPLE_PERCENTAGE * num_frames
            ))
        assert type(N) is IntType, 'N is not an integer: {}'.format(N)

        idx = np.sort(np.random.choice(xrange(num_frames), N, replace=False))
        return self.data[idx], self.labels[idx]

    def _prob(self, p=None):
        if not p:
            p = Constants.DEFAULT_SAMPLE_PERCENTAGE
        assert 0.0 < p < 1.0, 'p must be in between [0.0, 1.0]: {}'.format(p)
        num_frames = self.data.shape[0]
        while True:
            idx = [i for i in xrange(num_frames) if np.random.uniform() < p]
            if idx:
                break
        return self.data[idx], self.labels[idx]

    def sample(self):
        return self.method(self.method_args)
