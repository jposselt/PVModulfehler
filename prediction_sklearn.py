import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from IPython.display import display
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.model_selection import cross_val_score
import numpy as np
import matplotlib as mpl
from sklearn.metrics import confusion_matrix, plot_roc_curve
import seaborn

plt.style.use('seaborn-notebook')

class MachineLearningModellEvaluator:
    """
    Class to evaluate a ML-model for a dataset
    Currently available models:
        - SVM
        - KNN
        - DTC
    """
    def __init__(self, path):

        # Load data
        df = pd.read_csv(path)


        # Adjust columns
        df.rename(columns = {'Unnamed: 0':'time'}, inplace = True)
        df['time'] = pd.DatetimeIndex(df['time'])
        df.set_index('time', inplace=True)
        df.drop(['orientation', 'string_id'], axis=1, inplace=True)


        self.df_this = df.sample(frac=1)
        self.y = self.df_this['defect'].astype('float32').to_numpy()
        self.X =  self.df_this.drop(["defect"], axis=1).astype('float32').to_numpy()
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.3)


    def Classifier(self,model, k_folds):
        """
        Evaluates ML-Classifier with k-fold cross-validation
        Parameters
        ----------
        model: model to train (SVM, KNN, DTC)
        k_folds: k-folds for cross-validation
        """

        if model == "SVM":
            clf = svm.SVC(kernel="rbf")
        elif model == "KNN":
            clf =KNeighborsClassifier(n_neighbors=10)
        elif model == "DTC":
            clf = tree.DecisionTreeClassifier()
        else:
            print("Invalid model")


        clf.fit(self.X_train, self.y_train)
        Y_predict = clf.predict(self.X_test)

        scores = cross_val_score(clf, self.X, self.y, cv=k_folds)

        print(scores)
        print("%0.4f accuracy with a standard deviation of %0.4f" % (scores.mean(), scores.std()))

        plt.ylabel("Accuracy")
        plt.xlabel("k fold run")
        plt.title("k-fold Cross-Validation")
        bot,top = plt.ylim()
        lf,right = plt.xlim()
        print(top)
        plt.text(lf, np.max(scores),"$\overline{Acc}$ = "+ str(round(scores.mean(),5)))
        plt.text(lf+2, np.max(scores),"$\sigma_{Acc}$ = "+ str(round(scores.std(),5)))
        plt.grid()
        plt.plot(scores)


        plt.show()


        print(confusion_matrix(self.y_test, Y_predict))

        seaborn.heatmap(confusion_matrix(self.y_test, Y_predict), cmap = 'rocket_r', annot = True, fmt = 'd', yticklabels = ['No Error', 'Error'], xticklabels = ['Pred No Error', 'Pred Error'])

        plt.show()


MLE = MachineLearningModellEvaluator("data/dataframes/425987_f0e9ebe626b540b7fe71850b2d26acb4.csv")

MLE.Classifier("SVM", 10)
