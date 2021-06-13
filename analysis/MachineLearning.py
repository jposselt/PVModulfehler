from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import pandas as pd


class MLModel:
    def __init__(self):
        self.trainingData = None
        self.testData = None
        self.history = None

        # Hardcoded model for now
        self.model = Sequential()
        self.model.add(Dense(8, input_dim=8, activation='sigmoid'))
        self.model.add(Dense(14, activation='sigmoid'))
        self.model.add(Dense(7, activation='sigmoid'))
        self.model.add(Dense(1, activation='sigmoid'))
        
        # Compile model
        self.model.compile(loss='mean_squared_error', optimizer='sgd',metrics=['mse', 'mae', 'mape', 'cosine','acc'])

        self.scaler = MinMaxScaler()

    def addData(self, data, test_size, random_state):
        train, test = train_test_split(data, test_size=test_size, random_state=random_state)

        if self.trainingData:
            self.trainingData.append()
        else:
            self.trainingData = pd.concat([self.trainingData, train.copy()])

        if self.testData:
            self.testData = pd.concat([self.testData, test.copy()])
        else:
            self.testData = test.copy()

    def learn(self, trainClass, epochs=30, batch_size=10):
        if not (self.trainingData is None or self.trainingData.empty):
            # Split class from training data
            train_X = self.trainingData.drop(columns=[trainClass]) #Input
            train_Y = self.trainingData[trainClass]                #Class

            train_X = self.scaler.fit_transform(train_X)
        
            self.history = self.model.fit(train_X, train_Y, epochs=epochs, batch_size=batch_size)

    def evaluate(self, trainClass):
        if not (self.testData is None or self.testData.empty):
            # Split class from test data
            test_X = self.testData.drop(columns=[trainClass]) #Input
            test_Y = self.testData[trainClass]                #Class

            test_X = self.scaler.fit_transform(test_X)

            self.model.evaluate(test_X,test_Y)

    def save(self):
        pass

    def load(self):
        pass