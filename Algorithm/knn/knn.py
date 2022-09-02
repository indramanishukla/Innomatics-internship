from math import dist
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import cdist

def euclidean(point, data):
    # Euclidean distance between points a & data
    return cdist(point, data)
    # return np.linalg.norm(point[:,np.newaxis]-data, axis=2)
class KNeighbors:
    def __init__(self, k=5, dist_metric=euclidean):
        self.k = k
        self.dist_metric = dist_metric
    def fit(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train
    def predict(self, X_test):
        self.X_test = X_test
        
        # calculating the distance using dist_metric variable associated with euclidean function
        distances = self.dist_metric(self.X_test, self.X_train)
           
        # y_sorted = [y for _, y in sorted(zip(distances, self.y_train))] # another way of getting the actual target variable from the sorted distance and the y_train value associated with it
        
        # sorted k indices of distances 
        dis_idx = np.argsort(distances)[:,:self.k]
        
        # k nearest neighbors matrix 
        neighbors = self.y_train[dis_idx]

        # now we just need the mean        
        return np.mean(neighbors, axis=1)

    def mape(self,y_true, y_pred):
        
        self.y_pred = y_pred
        self.y_true = y_true

        return np.mean((np.abs(self.y_true-self.y_pred)/self.y_true))*100


if __name__ == '__main__':


    import numpy as np
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    from sklearn import datasets
    from sklearn.model_selection import train_test_split
    import os

    # basedir = os.path.abspath(os.path.dirname(__file__))
    # filename = os.path.join(basedir, 'diamonds.csv')

    # df = pd.read_csv(filename)

    dia = datasets.load_diabetes()
    X, y = dia.data, dia.target

    X_train, X_test, train_labels, test_labels = train_test_split(X, y, train_size=.7, random_state=42)



    from knn import KNN

    reg = KNN(5)
    reg.fit(X_train, train_labels)

    y_pred = reg.predict(X_test)


    # print(reg.rmse( reg.predict(X_test), test_labels))
    # print(reg.rmse(y_pred, test_labels))
    print(y_pred)
    # dist = euclidean_distance(X_train, X_test)
    print(len(y_pred))
    print(len(y_pred[0]))
    print(len(y_pred[0][0]))



    from sklearn.neighbors import KNeighborsRegressor
    from sklearn.metrics import mean_squared_error

    # knn_reg = KNeighborsRegressor(5)
    # knn_reg.fit(X_train, train_labels)
    # y_pred_sk = knn_reg.predict(X_test)
    # print(reg.rmse(y_pred_sk, test_labels))
    # print(mean_squared_error(test_labels, y_pred_sk, squared=False))
    # print(mean_squared_error(test_labels, y_pred, squared=False))

