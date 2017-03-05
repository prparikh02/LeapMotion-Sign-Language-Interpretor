from __future__ import division
from DataReader import DataReader, DataParserOpt
import numpy as np


def test():
    opt = DataParserOpt()
    # print type(opt)
    myOpt = DataParserOpt(only_left=True, only_right=False)
    myDataReader = DataReader(
        './src/mapping.txt', './samples/sample_b_1.json', myOpt)
    a, y = myDataReader.extract_features()
    np.savetxt('testdata.csv', a, delimiter=',')
    np.save('testdata', a)
    print a.shape, len(y)
if __name__ == '__main__':
    test()
