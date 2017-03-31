import numpy as np
from DataReader import DataReader, DataParserOpt

# myOpt = DataParserOpt(only_right=True)
myOpt = None
dr = DataReader('mapping.txt', 'sample_b_0.json', opt=myOpt)
A, y = dr.extract_features()
print(A.shape)
unique, counts = np.unique(y, return_counts=True)
print(dict(zip(unique, counts)))


from Normalizer_v2 import Normalizer

N = Normalizer()
A_norm = N.affine_translation(A, 'mapping.txt')

print(A[23, :][186:])
print(A_norm[23, :][186:])
print(A[23, [366, 367, 368]])
print(A_norm[23, [366, 367, 368]])