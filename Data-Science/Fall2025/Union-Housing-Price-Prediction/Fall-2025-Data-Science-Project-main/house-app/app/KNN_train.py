
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle
from KNN_model import MyKNN

#Read Data
df = pd.read_csv('Model_Training (3).csv')

#Drop columns not needed
df = df.drop('Style_short', axis=1)
df = df.drop('ZipCode', axis=1)

#convert towns to KNN friendly value, TOWN IS NOT JUST A NUMBER
df = pd.get_dummies(df, columns=['Town'], drop_first=True)

#split into test and training data
x = df.drop('SalesPrice',axis = 1)
y = df['SalesPrice']
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.3)

#scale features to similar proportions and influence
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

#knn tasked with finding neighborhoods of 7
knn = MyKNN(k=7)
knn.fit(X_train_scaled, y_train)

# Predictions made from both test and train sets
train_pred = knn.prediction(X_train_scaled)
test_pred = knn.prediction(X_test_scaled)

#Errors printed out
#MAE Mean Absolute Error
#RMSE Root Mean Squared Error
print(f"Train RMSE: ${knn.EvaluateRMSE(y_train, train_pred):,.2f}")
print(f"Train MAE: ${knn.EvaluateMAE(y_train, train_pred):,.2f}")
print(f"Test RMSE: ${knn.EvaluateRMSE(y_test, test_pred):,.2f}")
print(f"Test MAE: ${knn.EvaluateMAE(y_test, test_pred):,.2f}")

#Used to find best K value, was 7
"""
for k in range(1,26,2):
  knn = MyKNN(k)
  knn.fit(X_train_scaled, y_train)

  train_pred = knn.prediction(X_train_scaled)
  test_pred = knn.prediction(X_test_scaled)

  print(f"at K={k}")
  print(f"Train RMSE: ${knn.EvaluateRMSE(y_train, train_pred):,.2f}")
  print(f"Train MAE: ${knn.EvaluateMAE(y_train, train_pred):,.2f}")
  print(f"Test RMSE: ${knn.EvaluateRMSE(y_test, test_pred):,.2f}")
  print(f"Test MAE: ${knn.EvaluateMAE(y_test, test_pred):,.2f}")
  
  #BEST FIT IS AFTER EXTENSIVE TESTING K=7
"""

# --- 4. SAVE ---
print("saving model...")

with open('house_price_model.pkl', 'wb') as file:
    pickle.dump([knn,scaler,X_train.columns], file, pickle.HIGHEST_PROTOCOL)

print("KNN Model Saved Successfully!")