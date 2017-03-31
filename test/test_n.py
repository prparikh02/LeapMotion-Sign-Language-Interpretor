from Normalizer import Normalizer
from Transformer import Transformer

# nrm = Normalizer()
# method = getattr(nrm, 'affine_translation')
# print method
# method('hi')

T = Transformer(config_file='../config.json', feature_map='mapping.txt')
A, y = T.transform('sample_b_0.json')

print A
print y
