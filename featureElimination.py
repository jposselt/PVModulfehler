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
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

class FeatureExtractor:
    """
    Class to select most important features from dataset based on various evaluation methods.
    Currently available:
        - chi2
        - RFE
    """
    def __init__(self, path):

        # Load data
        df = pd.read_csv(path)
        #df = pd.read_csv("./data/dataframes/622592_48a28befcb11c72435d8f44f435d5ad0.csv")

        # Adjust columns
        df.rename(columns = {'Unnamed: 0':'time'}, inplace = True)
        df['time'] = pd.DatetimeIndex(df['time'])
        df.set_index('time', inplace=True)
        df.drop(['orientation', 'string_id'], axis=1, inplace=True)


        self.df_this = df.sample(frac=1)
        self.y = self.df_this['defect'].astype('float32').to_numpy()
        self.X =  self.df_this.drop(["defect"], axis=1).astype('float32').to_numpy()



    def SelectBestFeatures(self, method, rank):
        """
        Featrue selection function
        Parameters
        ----------
        method: ranking method (chi2, RFE)
        rank: number of top features
        """
        if method == "chi2":
            # Feature extraction
            test = SelectKBest(score_func=chi2, k='all')
            fit = test.fit(self.X, self.y )


            display("Equivalent Features:", list(self.df_this.columns))

            # Summarize scores
            np.set_printoptions(precision=rank)
            print("Feature Ranking: %s" % fit.scores_)

        elif method == "RFE":

            model = LogisticRegression()
            rfe = RFE(model, rank)
            fit = rfe.fit(self.X, self.y)


            print("Num Features: %s" % (fit.n_features_))
            display("Equivalent Features:", list(self.df_this.columns))
            print("Selected Features: %s" % (fit.support_))
            print("Feature Ranking: %s" % (fit.ranking_))

        else:
            print(ValueError("Invalid method"))



