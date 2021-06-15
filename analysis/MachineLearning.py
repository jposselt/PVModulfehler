from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import pandas as pd


class MLModel:
    def __init__(self, inputDim, layers, activation='sigmoid', loss='mean_squared_error', optimizer='sgd', metrics=['mse', 'mae', 'mape', 'cosine','acc']):
        self.trainingData = None
        self.testData = None
        self.history = None

        # Hardcoded model for now
        self.model = Sequential()

        layerCount = 0
        for units in layers:
            if layerCount == 0:
                self.model.add(Dense(units, input_dim=inputDim, activation=activation))
                self.model.add(Dropout(0.2))
            else:
                if layerCount == (len(layers) - 1):
                    self.model.add(Dense(units, activation='sigmoid'))
                else:
                    self.model.add(Dense(units, activation=activation))
                    self.model.add(Dropout(0.2))
            layerCount += 1
        
        # Compile model
        self.model.compile(loss=loss, optimizer=optimizer, metrics=metrics)

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

    def learn(self, trainColumns, epochs=30, batch_size=10):
        if not (self.trainingData is None or self.trainingData.empty):
            # Split class from training data
            train_X = self.trainingData.drop(columns=trainColumns) #Input
            train_Y = self.trainingData[trainColumns]              #Class

            train_X = self.scaler.fit_transform(train_X)
        
            self.history = self.model.fit(train_X, train_Y, epochs=epochs, batch_size=batch_size)

    def evaluate(self, trainColumns):
        if not (self.testData is None or self.testData.empty):
            # Split class from test data
            test_X = self.testData.drop(columns=trainColumns) #Input
            test_Y = self.testData[trainColumns]              #Class

            test_X = self.scaler.fit_transform(test_X)

            self.model.evaluate(test_X,test_Y)

    def save(self):
        pass

    def load(self):
        pass