import Constants
import json
import numpy as np
import os.path
from DataReader import DataReader, DataParserOpt
from DataSampler import DataSampler
from Normalizer import Normalizer


class Transformer(object):
    '''
    Transforms raw JSON data to numpy array with transformations (e.g. filter,
        sample, normalize, etc.) specified by config file or wizard.
    '''

    def __init__(self, config_file=None, feature_map=None):
        if config_file:
            if not os.path.exists(config_file):
                raise IOError('Could not find file {}'.format(config_file))
            self.method = self._read_config_file
            self.config_file = config_file
            self._read_config_file()
        else:
            self.method = self._manual_wizard()
        self.map_file = \
            feature_map if feature_map else Constants.DEFAULT_MAPPING_FILE

    def _read_config_file(self):
        '''
        Load transformations from config file
        '''
        try:
            with open(self.config_file) as cfg_f:
                cfg = json.load(cfg_f)
        except IOError as e:
            print('I/O error({}): {}'.format(e.errno, e.strerror))
        self.config = cfg

    def _manual_wizard(self):
        '''
        TODO:
        Walk user through transformation options
        '''
        print('Manual config wizard is not yet implemented')
        return

    def _apply(self):
        '''
        Apply transformations set ...
        '''
        if 'filter' not in self.config:
            raise ValueError('Config map should include "filter."')
        opt = DataParserOpt(**self.config['filter'])
        dr = DataReader(self.map_file,
                        self.data_file,
                        opt=opt)
        A, y = dr.extract_features()
        if 'sample' in self.config:
            try:
                method = self.config['sample']['method']
                method_args = self.config['sample']['method_args']
                ds = DataSampler(A, y, method, method_args)
            except:
                ds = DataSampler(A, y)
                print('Sample structure has or method_args')
            A, y = ds.sample()
        if 'normalize' in self.config:
            nml = Normalizer()
            for method_str in self.config['normalize']['methods']:
                method = getattr(nml, method_str)
                A = method(A, map_file=self.map_file)
        return A, y

    def transform(self, raw_data_file):
        '''
        Take in raw data file as input and apply transformations
        '''
        if not os.path.exists(raw_data_file):
            raise IOError('Could not find file {}'.format(raw_data_file))
        self.data_file = raw_data_file
        return self._apply()
