import inspect
import numpy as np
import os
import sys
import time
from signpy.core.Transformer import Transformer

start_time = time.time()
T = Transformer(config_file='./tests/config.json',
                feature_map='./tests/mapping.txt')
A, y = T.transform('./samples/sample_b_0.json')
end_time = time.time()
print('time elapsed: {}'.format(end_time - start_time))

print(A, A.shape)
print(y, y.shape)
