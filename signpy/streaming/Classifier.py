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

    def _predict(self, X):
        """
        :param X: input data, should be shaped as batchsize by 200 by 186
        :return: predicted character

        Internal function
        """
        result = (self.model.predict(X).flatten())
        indx = np.argsort(result).flatten()[::-1]
        char = [indxToChar[i] for i in indx.tolist()[:5]]
        return list(zip(char, result[indx][:5]))


    def predict(self, X, windows_size=200, batchsize=32):
        """
        :param X: input data
        :return: sequence of prediction

        This function slides window on the input, calls __predict__,
        returns the prediction
        """

        # TODO: More robust error checking
        if X is None or X.shape[0] == 0:
            return 'no hands detected'
        # TODO: More robust interpolation
        if X.shape[0] < 200:
            remaining = 200 - X.shape[0]
            L = X[-1, :]
            X = np.append(X, np.matlib.repmat(L, remaining, 1), axis=0)

        return self._predict(X[np.newaxis, :, :])
