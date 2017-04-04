import inspect
import numpy as np
import os
import sys
import time
from signpy.core.Transformer import Transformer

start_time = time.time()
T = Transformer(config_file='./tests/config.json',
                feature_map='./tests/mapping.txt')
A, y = T.transform('./samples/sample_a_1.json')
end_time = time.time()
print('time elapsed: {}'.format(end_time - start_time))

print('{}\n{}'.format(A, A.shape))
print('{}\n{}'.format(y, y.shape))
