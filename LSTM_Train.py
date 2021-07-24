import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import utils.aiUtils as aiUtils
from sklearn.model_selection import train_test_split
from keras.layers import CuDNNLSTM
from keras.layers.core import Dense, Dropout
from keras.models import Sequential
from keras.callbacks import EarlyStopping, ModelCheckpoint

from IPython.display import display

modelDesc = "622592_ee382cc56a3fb03a01b19cbdd49d456f"

# Load data
df = pd.read_csv("./data/paper/dataframes/"+ modelDesc +".csv")

# Adjust columns
df.rename(columns = {'Unnamed: 0':'time'}, inplace = True)
df['time'] = pd.DatetimeIndex(df['time'])
df.set_index('time', inplace=True)
df.drop(['orientation', 'string_id','minuteOfDay','fracDayOfYear'], axis=1, inplace=True)

# Reshape
timesteps = 4
outputColumns = ['defect']
outputSteps = 1
inputShapeWidth = 8
inputOutputWidth = 1
lstmData = aiUtils.reshapeDataForPredictionLSTM(df, timesteps, outputColumns, outputSteps, 6)

lstmX = lstmData['x']
lstmY = lstmData['y']

# Train/Test data
lstmX_train, lstmX_test, lstmY_train, lstmY_test = train_test_split(lstmX, lstmY, test_size=0.1)

# Model
model = Sequential()
model.add(CuDNNLSTM(inputShapeWidth,return_sequences=True, input_shape=(timesteps, inputShapeWidth)))  #return_sequences=True https://github.com/keras-team/keras/issues/7403
model.add(Dropout(0.2))
model.add(CuDNNLSTM(inputShapeWidth*3,return_sequences=True))
model.add(Dropout(0.2))
model.add(CuDNNLSTM(inputShapeWidth*2,return_sequences=True))
model.add(Dropout(0.2))
model.add(CuDNNLSTM(inputShapeWidth*2,return_sequences=True))
model.add(Dropout(0.2))
model.add(CuDNNLSTM(6))
model.add(Dropout(0.2))
model.add(Dense(inputOutputWidth))

model.compile(optimizer='rmsprop', loss=aiUtils.root_mean_squared_error, metrics=['accuracy',"mse"])

# Train model
basePath="./data/paper/lstm/"
callbacks = [#EarlyStopping(monitor='val_loss', patience=4),
             ModelCheckpoint(filepath=basePath +'checkpoint_{epoch:02d}-{val_loss:.10f}.h5', monitor='val_loss',period=5, save_best_only=False)]
history = model.fit(lstmX_train, lstmY_train, epochs=50, validation_split=0.2,batch_size=32, verbose=1,callbacks=callbacks)

# Save model
model.save(basePath + 'finished_' + modelDesc + '.h5')

# Evaluate model
np.set_printoptions(formatter={'float': lambda x: "{0:0.6f}".format(x)})
predictedY = model.predict(lstmX_test)
stdout = sys.stdout

f = open("./data/paper/lstm/" + "eval_" + modelDesc + ".txt", "w")
sys.stdout = f
model.model.summary()
sys.stdout = stdout

f.write("\n")
f.write(str(model.model.metrics_names) + "\n")
f.write(str(model.evaluate(lstmX_test,lstmY_test)) + "\n\n")
f.write(str(aiUtils.fullMetrics(lstmY_test,predictedY)))
f.close()

# Plot training history
sns.set_theme(style="darkgrid")
fsize = 16

fig, axes = plt.subplots(1, 2, figsize=(16, 8))
mse = sns.lineplot(data = model.history.history['mean_squared_error'], ax = axes[0])
acc = sns.lineplot(data = model.history.history['acc'], ax = axes[1])

mse.set_xlabel('Epoch', fontsize=fsize)
mse.set_ylabel('Mean Squared Error', fontsize=fsize)
mse.tick_params(axis='both', labelsize=fsize)

acc.set_xlabel('Epoch', fontsize=fsize)
acc.set_ylabel('Accuracy', fontsize=fsize)
acc.tick_params(axis='both', labelsize=fsize)

fig.savefig(basePath + modelDesc + ".png")
plt.close(fig)