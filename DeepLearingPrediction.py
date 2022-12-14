# -*- coding: utf-8 -*-
"""
Automatically generated by Colaboratory.

Author: Edudzi Mamattah
"""

# from google.colab import drive # Mount the google drive for data loading
# drive.mount('/content/drive')

import numpy as np #helps for array operation
import matplotlib.pyplot as plt #helps with graphical plots
import pandas as pd #helps to read the data
from sklearn.model_selection import train_test_split #helps to split training data and testing data
from sklearn.preprocessing import LabelEncoder #helps to encode bool/text variables to be numerical values
from sklearn.preprocessing import OneHotEncoder #helps for label one-hot encoding 
from sklearn.metrics import accuracy_score #helps to evaluate the prediction accuracy
import keras #helps for ANN model construction
import tensorflow as tf #helps for ANN model construction
from sklearn.linear_model import LogisticRegression

# Load the train and test set gotten from R

train = pd.read_csv('loan_df_train.csv')  #Load data with the corresponding path in google drive 
test = pd.read_csv('loan_df_test.csv')

# Checking the shape of the data
print (train.shape)
print (test.shape)

train.head(6)

test.head(6)

# Conversion of the data frame in R, to a .csv added an extra column, so I will remove them 
del train['Unnamed: 0']
del test['Unnamed: 0']

train.head(6)

test.head(6)

print (train.info())

print(test.info())

"""Rearranging the column order so that the target variable is the last column. I will do this for both data frames."""

test = test[["loan_limit", "Gender", "approv_in_adv","loan_type","loan_purpose","Credit_Worthiness","open_credit","business_or_commercial","term","Neg_ammortization","interest_only","lump_sum_payment","occupancy_type","total_units","credit_type","co.applicant_credit_type","age","submission_of_application","Region","PC1","PC2","PC3","PC4","PC5","Status"]]

train = train[["loan_limit", "Gender", "approv_in_adv","loan_type","loan_purpose","Credit_Worthiness","open_credit","business_or_commercial","term","Neg_ammortization","interest_only","lump_sum_payment","occupancy_type","total_units","credit_type","co.applicant_credit_type","age","submission_of_application","Region","PC1","PC2","PC3","PC4","PC5","Status"]]

print (train.info())

print(test.info())

# Creating copies of the data frames for the sake of redundancy. 
# Just in case something unfortunate happens, it would not affect the main data frame 
train_temp = train.copy()
test_temp = test.copy()

"""Using a Likelihood encoding method to encode the variables in the data frames"""

lb = LabelEncoder()
# would first encode the non-numerical column variables with type object
cat_cols = [col for col in train_temp.columns if train_temp[col].dtype == 'object']

for col in cat_cols:
    train_temp[col] = lb.fit_transform(train_temp[col])

cat_cols = [col for col in test_temp.columns if test_temp[col].dtype == 'object']

for col in cat_cols:
    test_temp[col] = lb.fit_transform(test_temp[col])

#function for encoding
def likelihood_encoding(df, cat_cols, target_variable = "Status"):
    # cat_cols.remove(target_variable)
    df_temp = df.copy()
    for col in cat_cols:
        effect = {}
        print(col)
        for category in df[col].unique():
            print(category)

            try:
                temp = df[df[col] == category]
                lr = LogisticRegression()
                X = temp.drop(target_variable, axis = 1, inplace = False)
                y = temp[target_variable]
                # print(temp.drop(target_variable, axis = 1).isnull().sum())
                lr.fit(X, y)

                effect[category] = accuracy_score(y, lr.predict(X))
            except Exception as E:
                print(E)
        
        for key, value in effect.items():
            effect[key] = np.log(effect[key] / (1 - effect[key] + 1e-6))
            
        df_temp.loc[:, col] = df_temp.loc[:, col].map(effect)
    return df_temp

cat_cols = [col for col in train_temp.columns if train_temp[col].dtype == 'object']
train_temp = likelihood_encoding(train_temp, cat_cols)

cat_cols = [col for col in test_temp.columns if test_temp[col].dtype == 'object']
test_temp = likelihood_encoding(test_temp, cat_cols)

train_temp.head()

test_temp.head()

"""Encoding objects of the boolean data type

"""

cat_cols = [col for col in train_temp.columns if train_temp[col].dtype == 'bool']

for col in cat_cols:
    train_temp[col] = lb.fit_transform(train_temp[col])

cat_cols = [col for col in test_temp.columns if test_temp[col].dtype == 'bool']

for col in cat_cols:
    test_temp[col] = lb.fit_transform(test_temp[col])

cat_cols = [col for col in train_temp.columns if train_temp[col].dtype == 'bool']
train_temp = likelihood_encoding(train_temp, cat_cols)

cat_cols = [col for col in test_temp.columns if test_temp[col].dtype == 'bool']
test_temp = likelihood_encoding(test_temp, cat_cols)

train_temp.iloc[:,19:24]

# Creating a copy of the encoded data frames
train_tp = train_temp.copy()
test_tp = test_temp.copy()

train_le = np.zeros_like(train_tp)     # create a matrix of zeros in the shape of train_tp and store in train_le     # Set up a matrix for encoded data 
train_le[:,19:24] = train_tp.iloc[:,19:24]      # This selects the all rows from train_le and copies all rows of train_tp into it. and then copies columns 19 to 23 into the train_le
for i in range(1, train_tp.shape[1]):           # Encode the data using label encoder
   le = LabelEncoder().fit(train_tp.iloc[:,i])  #fit first to let the encoder know the distinct numbers
   train_le[:,i] = le.transform(train_tp.iloc[:,i]) # transform to the distinct encoding starting from 0 to n

print(train_le)

test_le = np.zeros_like(test_tp)     
test_le[:,19:24] = test_tp.iloc[:,19:24]       
for i in range(1, test_tp.shape[1]):   
   le = LabelEncoder().fit(test_tp.iloc[:,i])   
   test_le[:,i] = le.transform(test_tp.iloc[:,i])

X_train, y_train = train_le[:,:-1], train_le[:,-1:]
X_test, y_test = test_le[:,:-1], test_le[:,-1:]

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

onehot = OneHotEncoder()                     #An objective for one-hot package
onehot.fit(y_train)                          #Transform labels to be the one-hot format
y_train_onehot = onehot.transform(y_train).toarray() #Transform training labels to be one-hot format
y_test_onehot = onehot.transform(y_test).toarray()   #Transform testing labels to be one-hot format

model = keras.Sequential()                         
model.add(keras.layers.Dense(1024, input_shape=(24,))) 
model.add(keras.layers.Activation("sigmoid"))          
model.add(keras.layers.Dense(2))                       
model.add(keras.layers.Activation("softmax"))          
model.compile(tf.keras.optimizers.SGD(learning_rate = 1e-2), 'categorical_crossentropy', metrics='acc')
model.summary()
model.fit(X_train, y_train_onehot, epochs = 75, batch_size = 1024, verbose = 2) #training the model with some hyper-parameters

prediction = model.predict(X_test)            # Predict the testing set
print (model.evaluate(X_test, y_test_onehot)) # Evaluation the prediction, and accuracy in the test set is 0.9617

from sklearn.metrics import confusion_matrix, classification_report

y_pred=np.argmax(prediction, axis=1)
y_test=np.argmax(y_test_onehot, axis=1)


print(confusion_matrix(y_test, y_pred))

"""Model classification report"""

print(classification_report(y_test, y_pred))