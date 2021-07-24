from keras.models import load_model
from keras.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split
import utils.aiUtils as aiUtils
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

basePath = "./data/paper/"
modelID = "finished_622592_ee382cc56a3fb03a01b19cbdd49d456f"
dataID = "1081347_f55054c9be71ab6580aa39aea9b81e69"

# Load data
df = pd.read_csv(basePath + "dataframes/" + dataID + ".csv")

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
lstmX_train, lstmX_test, lstmY_train, lstmY_test = train_test_split(lstmX, lstmY, test_size=0.3)

# Load model
predictionModel = load_model(basePath + "lstm/" + modelID + '.h5',custom_objects={'root_mean_squared_error': aiUtils.root_mean_squared_error})

# Summarize model.
predictionModel.summary()

# Metrics
print('predicting')
predictedY = predictionModel.predict(lstmX_test)

print(str(predictionModel.model.metrics_names) + "\n")
print(str(predictionModel.evaluate(lstmX_test,lstmY_test)) + "\n\n")

np.set_printoptions(formatter={'float': lambda x: "{0:0.6f}".format(x)})
print(aiUtils.fullMetrics(lstmY_test,predictedY))

# Retrain model
basePath="./data/paper/lstm/"
callbacks = [ModelCheckpoint(filepath=basePath +'retrain_checkpoint_{epoch:02d}-{val_loss:.10f}.h5', monitor='val_loss',period=5, save_best_only=False)]
history = predictionModel.fit(lstmX_train, lstmY_train, epochs=5, validation_split=0.2,batch_size=32, verbose=1,callbacks=callbacks)

# Save model
predictionModel.save(basePath + 'retrained_model.h5')

# Metrics after retraining
print('predicting')
predictedY = predictionModel.predict(lstmX_test)

print(str(predictionModel.model.metrics_names) + "\n")
print(str(predictionModel.evaluate(lstmX_test,lstmY_test)) + "\n\n")

np.set_printoptions(formatter={'float': lambda x: "{0:0.6f}".format(x)})
print(aiUtils.fullMetrics(lstmY_test,predictedY))

# Plot training history
sns.set_theme(style="darkgrid")
fsize = 16

fig, axes = plt.subplots(1, 2, figsize=(16, 8))
mse = sns.lineplot(data = predictionModel.history.history['mean_squared_error'], ax = axes[0])
acc = sns.lineplot(data = predictionModel.history.history['acc'], ax = axes[1])

mse.set_xlabel('Epoch', fontsize=fsize)
mse.set_ylabel('Mean Squared Error', fontsize=fsize)
mse.tick_params(axis='both', labelsize=fsize)

acc.set_xlabel('Epoch', fontsize=fsize)
acc.set_ylabel('Accuracy', fontsize=fsize)
acc.tick_params(axis='both', labelsize=fsize)

plt.show()