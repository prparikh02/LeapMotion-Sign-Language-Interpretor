import numpy as np
import numpy.matlib
import keras
from keras.models import load_model
import string


indxToChar = dict(zip(range(27), string.ascii_lowercase))
charToIndx = dict(zip(string.ascii_lowercase, range(27)))

class Classifier():
    """
    TODO: docstring
    """
    def __init__(self, model):
        """
        :param model: path to .h5 file
        h5 file stores the model architecture and weights
        """
        self.model = load_model(model)
        print('Ready')

    def __predict__(self, X):
        """
        :param X: input data, should be shaped as batchsize by 200 by 186
        :return: predicted character

        Internal function
        """
        result = self.model.predict(X)
        result = np.argmax(result)
        # return [indxToChar[i] for i in result]
        return [indxToChar[result]]

    def predict(self, X, windows_size=200, batchsize=32):
        """
        :param X: input data
        :return: sequence of prediction

        This function slides window on the input, calls __predict__,
        returns the prediction
        """

        if X is None or X.shape[0] == 0:
            print('no hands detected')
        if X.shape[0] < 200:
            remaining = 200 - X.shape[0]
            L = X[-1, :]
            X = np.append(X, np.matlib.repmat(L, remaining, 1), axis=0)

        return self.__predict__(X[np.newaxis, :, :])
        # result = []
        # for i in range(X.shape[0] - windows_size):
        #     temp = X.view()[i:i+windows_size][np.newaxis,:,:]
        #     result.extend(self.__predict__(temp))
        # return result

# # test code
# myClassifier = Classifier('/mnt/64efbe69-b915-4398-ae54-48f156ce7125/Documents/Rutgers/S17/capstone/common/LeapMotion-Sign-Language-Interpretor/my_model_convlstm.h5')
# opt = DataParserOpt()
# myDataReader = DataReader('./src/mapping.txt',
#                           '/mnt/64efbe69-b915-4398-ae54-48f156ce7125/Documents/Rutgers/S17/capstone/Unsorted_data/March24/normal/sample_a_1.json',
#                           opt)
# a,y = myDataReader.extract_features()
# res = myClassifier.predict(a)
# result_in_letter = [indxToChar[r] for r in res]