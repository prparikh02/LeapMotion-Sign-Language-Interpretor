from __future__ import division
import numpy as np
import json
import math

class DataSampler(object):
    
    def __init__(self, raw_data, method, *method_args):
        self.raw_data = raw_data # currently it works for list based data. Will have to be extended for numpy
        self.length = len(raw_data)
        self.method = method
        self.method_args = method_args


    def uniform_sampling(self, method = 'rate', value = -1):
        """
        Inputs: data - an m, n dimension matrix (m samples, n features)
                method - a string param which specifies the type of uniform sampling
                       - 'rate' => uniform sampling rate (every k frames)
                       - 'num_frames' => determine a uniform rate 'k' as length_of_data/num_frames
                value  - integer value the particular method utilizes
        
        Outputs: data matrix (m', n), where m' is the new number of data points
        """
        if value == -1:
            return None

        if value > len(self.raw_data):
            value = len(self.raw_data)
        sorted_data = sorted(self.raw_data) # When extending this, it would be best to sort by timestamp

        if method == 'rate' and value > 0 and isinstance(value, (int, long)):
            return sorted_data[0::value]
        elif method == 'num_frames' and value > 0 and isinstance(value, (int, long)):
            new_data = sorted_data[0::int(math.floor(self.length/value))]
            if len(new_data) > value:
                new_data = new_data[0:value]
            return new_data     
               

    def random_sampling(self, num_frames = -1):
        """
        Inputs: data - an m, n dimension matrix (m samples, n features)
                num_frames - if num_frames < m, num_frames randomly sampled frames are complied without replacement
        
        Outputs: data matrix (m', n), where m' is the new number of data points
        """
        if num_frames == -1 or not isinstance(num_frames, (int, long)):
            return None

        if num_frames > len(self.raw_data):
            num_frames = len(self.raw_data)
        
        return np.random.choice(self.raw_data, num_frames, replace=False)

    def begin_sampling(self):
        """
        Main method of the Data Sampler. It handles the logic of running the correct method on the data.
        """
        if self.method == 'uniform_sampling':
             return self.uniform_sampling(*(self.method_args))
        elif self.method == 'random_sampling':
            return self.random_sampling(*(self.method_args))
        else:
            return None
        
            

    
    