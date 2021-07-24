# Train neural networks

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import utils.aiUtils as aiUtils
from analysis.MachineLearning import MLModel

from IPython.display import display

# Load data
#df = pd.read_csv("./data/dataframes/425987_97a5f5a925c86b5b442f874d0760f6cb.csv")
df = pd.read_csv("./data/paper/dataframes/622592_ee382cc56a3fb03a01b19cbdd49d456f.csv")

# Adjust columns
df.rename(columns = {'Unnamed: 0':'time'}, inplace = True)
df['time'] = pd.DatetimeIndex(df['time'])
df.set_index('time', inplace=True)
df.drop(['orientation', 'string_id','minuteOfDay'], axis=1, inplace=True)

# Draw a sample from complete data
df_sample_true = df[df['defect'] == True].sample(5000).copy()
df_sample_false = df[df['defect'] == False].sample(5000).copy()
df_sample = pd.concat([df_sample_true, df_sample_false])

# Draw sample of data around noon time
#df_noon = df.between_time('12:00', '15:00')
#df_sample_true = df_noon[df_noon['defect'] == True].sample(5000).copy()
#df_sample_false = df_noon[df_noon['defect'] == False].sample(5000).copy()
#df_sample_noon = pd.concat([df_sample_true, df_sample_false])

# df_all = df.copy()
# df_noon = df.between_time('12:00', '15:00').copy()

# Configurations
configs = [
    {
        "data": df_sample,
        "layers": [8, 16, 5, 1],
        "activation": "relu",
        "optimizer": "adam",
        "output": "622592_ee382cc56a3fb03a01b19cbdd49d456f"
    },

    # {
    #     "data": df_sample,
    #     "layers": [8, 16, 5, 1],
    #     "activation": "sigmoid",
    #     "optimizer": "adam",
    #     "output": "97a5f5a925c86b5b442f874d0760f6cb_8-16-5-1_sigmoid_adam"
    # },

    # {
    #     "data": df_sample,
    #     "layers": [8, 16, 5, 1],
    #     "activation": "relu",
    #     "optimizer": "sgd",
    #     "output": "97a5f5a925c86b5b442f874d0760f6cb_8-16-5-1_relu_sgd"
    # },

    # {
    #     "data": df_sample,
    #     "layers": [16, 32, 16, 8, 4, 1],
    #     "activation": "relu",
    #     "optimizer": "adam",
    #     "output": "97a5f5a925c86b5b442f874d0760f6cb_16-32-16-8-4-1_relu_adam"
    # },

    # {
    #     "data": df_sample_noon,
    #     "layers": [8, 16, 5, 1],
    #     "activation": "relu",
    #     "optimizer": "adam",
    #     "output": "97a5f5a925c86b5b442f874d0760f6cb_8-16-5-1_relu_adam_noon"
    # },

    # {
    #     "data": df,
    #     "layers": [16, 32, 16, 8, 4, 1],
    #     "activation": "relu",
    #     "optimizer": "adam",
    #     "output": "97a5f5a925c86b5b442f874d0760f6cb_16-32-16-8-4-1_relu_adam_full"
    # },
]

predictColumns = ['defect']

for config in configs:
    #dframe.drop(['fracMinuteOfDay','fracDayOfYear'], axis=1, inplace=True)
    inputDimension = len(config["data"].columns) - len(predictColumns)

    # Create model
    model = MLModel(
        inputDim=inputDimension,
        loss="mean_squared_logarithmic_error",
        layers=config["layers"],
        activation=config["activation"],
        optimizer=config["optimizer"]
    )

    # Add data
    model.addData(config["data"], 0.3, 42)

    # Train model
    model.learn(predictColumns, epochs=100)

    # Model summary
    model.model.summary()

    # Evaluate model
    stdout = sys.stdout

    f = open("./data/paper/ml_plots/" + config["output"] + ".txt", "w")
    sys.stdout = f
    model.model.summary()
    sys.stdout = stdout

    f.write("\n")
    f.write(str(model.model.metrics_names) + "\n")
    f.write(str(model.evaluate(predictColumns)))
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

    fig.savefig("./data/paper/ml_plots/" + config["output"] + ".png")
    plt.close(fig)