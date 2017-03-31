import numpy as np
from DataSampler import DataSampler

N = 10
A = np.random.randint(N, size=(10, 6))
y = np.array([1 if np.random.random() < 0.50 else 0 for i in xrange(N)])
print(A, y)

method = 'prob'
DS = DataSampler(A, y, method, p=0.4)

A_sampled, y = DS.sample()
print(A_sampled, y)
