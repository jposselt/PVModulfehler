import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from analysis.MachineLearning import MLModel

from IPython.display import display

# Load data
df = pd.read_csv("./data/dataframes/425987_97a5f5a925c86b5b442f874d0760f6cb.csv")
#df = pd.read_csv("./data/dataframes/622592_48a28befcb11c72435d8f44f435d5ad0.csv")

# Adjust columns
df.rename(columns = {'Unnamed: 0':'time'}, inplace = True)
df['time'] = pd.DatetimeIndex(df['time'])
df.set_index('time', inplace=True)
df.drop(['orientation', 'string_id'], axis=1, inplace=True)

# Draw a sample from complete data
df_sample_true = df[df['defect'] == True].sample(5000).copy()
df_sample_false = df[df['defect'] == False].sample(5000).copy()
df_sample = pd.concat([df_sample_true, df_sample_false])

# Draw sample of data around noon time
df_noon = df.between_time('12:00', '15:00')
df_sample_true = df_noon[df_noon['defect'] == True].sample(5000).copy()
df_sample_false = df_noon[df_noon['defect'] == False].sample(5000).copy()
df_sample_noon = pd.concat([df_sample_true, df_sample_false])

# df_all = df.copy()
# df_noon = df.between_time('12:00', '15:00').copy()

# Configurations
configs = [
    {
        "data": df_sample,
        "layers": [8, 16, 5, 1],
        "activation": "relu",
        "optimizer": "adam",
        "output": "97a5f5a925c86b5b442f874d0760f6cb_8-16-5-1_relu_adam"
    },
]

predictColumns = ['defect']

for config in configs:
    #dframe.drop(['fracMinuteOfDay','fracDayOfYear'], axis=1, inplace=True)
    inputDimension = len(config["data"].columns) - len(predictColumns)

    # Create model
    model = MLModel(
        inputDim=inputDimension,
        layers=config["layers"],
        activation=config["activation"],
        optimizer=config["optimizer"]
    )

    # Add data
    model.addData(config["data"], 0.3, 42)

    # Train model
    model.learn(predictColumns, epochs=200)

    # Evaluate model
    f = open("./data/ml_plots/" + config["output"] + ".txt", "w")
    f.write(str(model.model.metrics_names) + "\n")
    f.write(str(model.evaluate(predictColumns)))
    f.close()

    # Plot training history
    fig, axes = plt.subplots(1, 3, figsize=(16, 8))
    sns.lineplot(data = model.history.history['mean_squared_error'], ax = axes[0])
    sns.lineplot(data = model.history.history['loss'], ax = axes[1])
    sns.lineplot(data = model.history.history['acc'], ax = axes[2])
    axes[0].set_title("Mean Squared Error")
    axes[1].set_title("Loss")
    axes[2].set_title("Accuracy")
    plt.suptitle("Metrics")
    fig.savefig("./data/ml_plots/" + config["output"] + ".png")
    plt.close(fig)