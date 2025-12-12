import numpy as np

#MyKNN Regression class to find continuous value
class MyKNN:
  def __init__(self, k):
    self.K = k

  #Fit the data
  def fit(self, X_train, y_train):
    self.X_train = X_train
    self.y_train = y_train.to_numpy() if hasattr(y_train, 'to_numpy') else y_train

  #Find K nearest Neighbors
  def findKNgbs(self, x):
    distance = np.sum((self.X_train - x) ** 2, axis = 1)
    distance = np.sqrt(distance)
    index = np.argsort(distance)

    return index[:self.K]

  #Take average of K neighborhood
  def prediction(self, X):
    n = X.shape[0]
    pred = np.zeros(n)

    for i in range(n):
      nns = self.findKNgbs(X[i, :])
      labels = self.y_train[nns]

      pred[i] = np.mean(labels)

    return pred

  # Root Mean Squared Error, penalizes large errors more
  def EvaluateRMSE(self, real, pred):
    mse = np.mean((real - pred) ** 2)
    rmse = np.sqrt(mse)
    return rmse

  # Mean Absolute Error, penalizes all errors equally
  def EvaluateMAE(self, real, pred):
    return np.mean(np.abs(real - pred))


