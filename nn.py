import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
import math
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras import Model
import sklearn.metrics as metrics
from tensorflow.keras import Sequential
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split
from tensorflow.keras.losses import MeanSquaredLogarithmicError
from sklearn.metrics import mean_squared_error


url = "data.csv"

data = pd.read_csv(url)

X = data.iloc[1:, 0:5]

y = data.iloc[1:,5:7]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)

standard_scaler = StandardScaler()
x_train_scaled = pd.DataFrame(
      standard_scaler.fit_transform(X_train),
      columns=X_train.columns
)
x_test_scaled = pd.DataFrame(
      standard_scaler.transform(X_test),
      columns = X_test.columns
)

hidden_units1 = 3000
hidden_units2 = 1500
learning_rate = 0.01
# Creating model using the Sequential in tensorflow
def build_model_using_sequential():
  model = Sequential([
    Dense(hidden_units1, kernel_initializer='normal', activation='relu'),
    Dropout(0.2),
    Dense(hidden_units2, kernel_initializer='normal', activation='relu'),
    Dense(2, kernel_initializer='normal', activation='linear')
  ])
  return model
# build the model
model = build_model_using_sequential()

msle = MeanSquaredLogarithmicError()
model.compile(
    loss=msle, 
    optimizer=Adam(learning_rate=learning_rate), 
    metrics=[msle]
)
# train the model
history = model.fit(
    x_train_scaled.values, 
    y_train.values, 
    epochs=15, 
    batch_size=150,
    validation_split=0.2
)
def plot_history(history, key):
  plt.plot(history.history[key])
  plt.plot(history.history['val_'+key])
  plt.xlabel("Epochs")
  plt.ylabel(key)
  plt.legend([key, 'val_'+key])
  plt.show()
# Plot the history
plot_history(history, 'mean_squared_logarithmic_error')
predictions = model.predict(x_test_scaled)
real_pred = []
im_pred = []
for i in range(len(predictions)):
  if(predictions[i][0] < 0):
    predictions[i][0] = -predictions[i][0]
  if(predictions[i][1] < 0):
    predictions[i][1] = -predictions[i][1]  
  real_pred.append(predictions[i][0])
  im_pred.append(predictions[i][1])
X_test['real'] = y_test.iloc[:,0:1]
X_test['real_pred'] = real_pred
X_test['im'] = y_test.iloc[:,1:2]
X_test['im_pred'] = im_pred

X_test.to_csv('hello.csv', index=False)

print("For real part ",metrics.mean_squared_log_error(X_test['real'],X_test['real_pred']))
print("For imaginary part ",metrics.mean_squared_log_error(X_test['im'],X_test['im_pred']))

#X_test['real'] = y_test