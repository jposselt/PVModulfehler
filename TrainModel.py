import pandas as pd
from analysis.MachineLearning import MLModel

from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("./data/dataframes/425987_97a5f5a925c86b5b442f874d0760f6cb.csv")
#df = pd.read_csv("./data/dataframes/622592_48a28befcb11c72435d8f44f435d5ad0.csv")

df.rename(columns = {'Unnamed: 0':'time'}, inplace = True)
df['time'] = pd.DatetimeIndex(df['time'])
df.set_index('time', inplace=True)
df.drop(['orientation', 'string_id'], axis=1, inplace=True)

df_all = df.copy()
df_noon = df.between_time('10:00', '14:00').copy()

predictColumns = ['defect']
for dframe in [df_all]:
    #dframe.drop(['fracMinuteOfDay','fracDayOfYear'], axis=1, inplace=True)

    inputDimension = len(dframe.columns) - len(predictColumns)

    model = MLModel(
        inputDim=inputDimension,
        layers=[8, 12, 5, 1],
        activation='relu'
    )

    model.addData(dframe, 0.3, 42)
    model.learn(predictColumns, epochs=30)

    print(model.model.metrics_names)
    model.evaluate(predictColumns)

    fig, axes = plt.subplots(1, 3)
    sns.lineplot(data = model.history.history['mean_squared_error'], ax = axes[0])
    sns.lineplot(data = model.history.history['loss'], ax = axes[1])
    sns.lineplot(data = model.history.history['acc'], ax = axes[2])
    axes[0].set_title("MSE")
    axes[1].set_title("LOSS")
    axes[2].set_title("ACC")
    plt.suptitle("Metrics")
    plt.show()