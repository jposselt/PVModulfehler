import pandas as pd
from analysis.MachineLearning import MLModel

from IPython.display import display
import matplotlib.pyplot as plt

df = pd.read_csv("./data/dataframes/425987_97a5f5a925c86b5b442f874d0760f6cb.csv")
df.drop(['Unnamed: 0', 'orientation', 'string_id'], axis=1, inplace=True)

display(df)
display(df.dtypes)

model = MLModel()
model.addData(df, 0.3, 42)
model.learn('defect')

print(model.metrics_names)
model.evaluate(test_X,test_Y)

plt.plot(model.history.history['mean_squared_error'])
plt.title('Mean Squared Error')
plt.show()