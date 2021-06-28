from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import pandas as pd


class MLModel:
    """Model for a standard multilayer perceptron
    """
    def __init__(self, inputDim, layers, activation='sigmoid', loss='mean_squared_error', optimizer='sgd', metrics=['mse','acc']):
        """Constructor

        Args:
            inputDim (int): Size of the input vector
            layers (list[int]): List with number of perceptron for each layer.
            activation (str, optional): Used perceptron activation function. Defaults to 'sigmoid'.
            loss (str, optional): Used loss function. Defaults to 'mean_squared_error'.
            optimizer (str, optional): Used optimizer. Defaults to 'sgd'.
            metrics (list, optional): List of tracked metrics. Defaults to ['mse','acc'].
        """
        self.trainingData = None
        self.testData = None
        self.history = None

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
        """Add data to the model

        Args:
            data (dataframe): Data used for training/testing
            test_size (float): Fraction of data to use for validation
            random_state (int): Controls the shuffling applied to the data before applying the split.
                                See documentation of sklearn.model_selection.train_test_split for more information
        """
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
        """Train the model

        Args:
            trainColumns (string): Data column the model should predict.
            epochs (int, optional): Number of training epochs. Defaults to 30.
            batch_size (int, optional): Number of samples per gradient update. Defaults to 10.
        """
        if not (self.trainingData is None or self.trainingData.empty):
            # Split class from training data
            train_X = self.trainingData.drop(columns=trainColumns) #Input
            train_Y = self.trainingData[trainColumns]              #Class

            train_X = self.scaler.fit_transform(train_X)
        
            self.history = self.model.fit(train_X, train_Y, epochs=epochs, batch_size=batch_size)

    def evaluate(self, trainColumns):
        """Returns the loss value & metrics values for the model in test mode.

        Args:
            trainColumns (string): Data column to predict

        Returns:
            [?]: Scalar test loss or list of scalars
        """
        if not (self.testData is None or self.testData.empty):
            # Split class from test data
            test_X = self.testData.drop(columns=trainColumns) #Input
            test_Y = self.testData[trainColumns]              #Class

            test_X = self.scaler.fit_transform(test_X)

            return self.model.evaluate(test_X,test_Y)