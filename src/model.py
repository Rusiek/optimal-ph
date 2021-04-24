from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler

import numpy as np
import pickle

import get_kmers



class BaselineModel:
    def __init__(self, model_file_path):
        self.model_file_path = model_file_path

    def vectorize_sequences(self, sequence_array):
        vectorize_on_length = np.vectorize(len)
        return np.reshape(vectorize_on_length(sequence_array), (-1, 1))

    def train(self, df_train):
        X = self.vectorize_sequences(df_train['sequence'].to_numpy())
        y = df_train['mean_growth_PH'].to_numpy()

        model = tree.DecisionTreeRegressor()
        model.fit(X, y)

        with open(self.model_file_path, 'wb') as model_file:
            pickle.dump(model, model_file)

    def predict(self, df_test):
        with open(self.model_file_path, 'rb') as model_file:
            model: tree.DecisionTreeRegressor = pickle.load(model_file)

        X = df_test['sequence'].to_numpy()
        X_vectorized = self.vectorize_sequences(X)
        return model.predict(X_vectorized)


class SVRModel:
    def __init__(self, model_file_path):
        self.model_file_path = model_file_path


    def train(self, df_train):
        limited_train = df_train[df_train.representative & ~df_train.is7]
        frequencies = get_kmers.get_features(limited_train.sequence, kmerlen=1)
        X = frequencies.to_numpy()
        y = limited_train.mean_growth_PH.to_numpy() 

        model = SVR(C=10.0, epsilon=0.1)
        model.fit(X, y)

        with open(self.model_file_path, 'wb') as model_file:
            pickle.dump(model, model_file)


    def predict(self, df_test):
        with open(self.model_file_path, 'rb') as model_file:
            model: SVR = pickle.load(model_file)

        X = get_kmers.get_features(df_test.sequence, kmerlen=1).to_numpy()
        return model.predict(X)

class SVRModelScaled:
    def __init__(self, model_file_path, scaler_file_path):
        self.model_file_path = model_file_path
        self.scaler_file_path = scaler_file_path


    def train(self, df_train):
        limited_train = df_train[df_train.representative & ~df_train.is7]
        frequencies = get_kmers.get_features(limited_train.sequence, kmerlen=1)
        X = frequencies.to_numpy()
        y = limited_train.mean_growth_PH.to_numpy() 

        scaler = StandardScaler().fit(X)
        X = scaler.transform(X)

        model = SVR(C=10.0, epsilon=0.1)
        model.fit(X, y)

        with open(self.model_file_path, 'wb') as model_file:
            pickle.dump(model, model_file)
        with open(self.scaler_file_path, 'wb') as scaler_file:
            pickle.dump(scaler, scaler_file)


    def predict(self, df_test):
        with open(self.model_file_path, 'rb') as model_file:
            model: SVR = pickle.load(model_file)

        with open(self.scaler_file_path, 'rb') as scaler_file:
            scaler: SVR = pickle.load(scaler_file)

        X = get_kmers.get_features(df_test.sequence, kmerlen=1).to_numpy()
        X = scaler.transform(X)
        return model.predict(X)