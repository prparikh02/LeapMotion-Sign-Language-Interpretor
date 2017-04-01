import inspect
import numpy as np
import os
import sys
import time
test_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
root_dir = os.path.abspath(os.path.join(test_dir, '../'))
sys.path.insert(0, root_dir + '/lib')
sys.path.insert(0, root_dir + '/src')
from Transformer import Transformer

start_time = time.time()
T = Transformer(config_file='./config.json', feature_map='./src/mapping.txt')
A, y = T.transform('./samples/sample_b_0.json')
end_time = time.time()
print('time elapsed: {}'.format(end_time - start_time))

print(A, A.shape)
print(y, y.shape)
