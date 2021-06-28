from analysis.Preprocessing import Preprocessor
from IPython.display import display
import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

# Support-vector machine
# Gut-Daten 2:1 Schlecht-Daten
# verschiedene Kernel
#
# - linear
# - poly
# - rbf
# - sigmoid
#
# Daten aus Juli 2019


pre = Preprocessor("799038c4e3522036d1ab6f8c64bb79b5", "./data/reports/")

pre.loadFilesByPattern("../PVDaten/Real/LimesysDataParsedTmp/6/6_WR_1_inek_2_2019-07-01-2019-07-31_1.csv", "1")
df_geil = pre.preprocessData()

pre.loadFilesByPattern("../PVDaten/Real/LimesysDataParsedTmp/425987/425987_WR_1_Grafenstein_2_2019-07-01-2019-07-31_1.csv", "1")
df_geil_schatten = pre.preprocessData()


pre.loadFilesByPattern("../PVDaten/Real/LimesysDataParsedTmp/622592/622592_WR_01_1_2019-07-01-2019-07-31_0.csv", "1")
df_diode_error = pre.preprocessData()

## gut und schlecht markieren
df_geil['error'] = 0
df_geil_schatten['error'] = 0

df_diode_error['error'] = 1

#display(df_geil)
#display(df_diode_error)

frames = [df_geil, df_diode_error, df_geil_schatten]

df = pd.concat(frames)
df = df.dropna(subset=["Dci", "Dcu", "Year", "Month", "Day", "temperature", "humidity", "cloudCover", "uvIndex", "windGust", "error"])

from sklearn.preprocessing import MinMaxScaler


X = np.array(df.drop(
        [
            'AcPower',
            'Edaily',
            'Dcp',
            'Orientation',
            'apparentTemperature',
            'dewPoint',
            'windSpeed',
            'windBearing',
            'visibility'
        ], 1).astype(float))

# Define target vector
y = np.array(df['error'])

# Import train_test_split function
from sklearn.model_selection import train_test_split

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3) # 70% training and 30% test

from sklearn import svm

#Create a svm Classifier
clf = svm.SVC(kernel = 'poly') # linear, poly, rbf, sigmoid

#Train the model using the training sets
clf.fit(X_train, y_train)

#Predict the response for test dataset
y_pred = clf.predict(X_test)

#Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics

# Model Accuracy: how often is the classifier correct?
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))


from sklearn.metrics import accuracy_score, f1_score, classification_report
from sklearn.metrics import roc_auc_score, precision_score, recall_score
from sklearn.model_selection import cross_val_score

cr_knn = classification_report(y_test, y_pred)
print(cr_knn)

scores = cross_val_score(clf, X, y, cv=10)

print(scores)
print(scores.mean())
print(scores.std())

print('Precision Score: ', round(precision_score(y_test, y_pred), 2))
print('Recall Score: ', round(recall_score(y_test, y_pred), 2))
print('F1 Score: ', round(f1_score(y_test, y_pred), 2))
print('Accuracy Score: ', round(accuracy_score(y_test, y_pred), 2))
print('ROC AUC: ', round(roc_auc_score(y_test, y_pred), 2))

from sklearn.metrics import confusion_matrix, plot_roc_curve
import seaborn

seaborn.heatmap(confusion_matrix(y_test, y_pred), cmap = 'rocket_r', annot = True, fmt = 'd', yticklabels = ['No Error', 'Error'], xticklabels = ['Pred No Error', 'Pred Error'])

plt.show()