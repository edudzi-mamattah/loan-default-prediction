# Loan Defaulter Prediction using Machine Learning & Deep Learning 

*Project Duration: March 2022 - April 2022*

## About this project

A project conducted on a publicly available  <a href ="https://www.kaggle.com/datasets/yasserh/loan-default-dataset?select=Loan_Default.csv."> Kaggle dataset </a>  (34 columns by 148,670 rows) to predict whether a person who takes a loan for a mortgage would default on the payment. 

## Data Preparation & Cleaning

The data was loaded into a data frame (using R). When it was loaded into the data frame, the empty cells were converted to NA values, to make their identification easier in R Studio. 

After that, the structure of the data was checked. Certain columns were removed because their values were either completely skewed towards one of two possible factors or because the column had the same value throughout the entire data frame.  


NAs were removed from the categorical columns by complete case removal- because attempting to impute NAs for such columns with their modal value could heavily imbalance the dataset. Also, this was a safer option as I could not be sure that the data that was missing from those columns were missing completely at random (MCAR). 

A complete case removal of all numerical NAs was not very feasible as a lot of NAs in one column corresponded to almost all the values of certain factors in other columns, so some imputation had to be done. 

Where appropriate, cells were imputed based on the types of columns they were contained in. Other columns were forced into their right data type as specified in the Data dictionary.

After the cleaning steps, I saved the data frame I had gotten at that point as a .Rda file, just so I could know that I had a cleaned data frame stored somewhere – in the event of any mishap. That file had 143,942 rows and 30 columns.
After making that file, I was ready to go into exploratory data analysis.


## Exploratory Data Analysis (EDA)

For exploratory data analysis, outliers were removed from columns whose data was made up of more than 1% of outliers. Boxplots were plotted to observe the types of outliers (whether lower bound or upper bound outliers).

Outliers were removed with the assumption that most of the data was lognormally distributed – as the data in question was mostly economic data. Correlations between variables were checked to ensure there was no multicollinearity, and the skewness and kurtosis and overall distributions of values within columns were investigated.

Principal component analysis (PCA) of the numerical columns at an 80% proportion of explained variance was undertaken. This was to reduce the dimensionality of the dataset. Only the first 5 PCs fulfilled this criteria.

Upon completion of this step, the data shape was 25 columns by 133,500.



## Machine Learning Prediction (Conditional Inference Tree) - R

A conditional inference tree was used to carry out the machine learning implementation, as it provided for a high degree of interpretability. These trees work like decision trees by recursiely partitioning data by performing a univariate split on dependent variables; however, conditional inference trees employ significance test methods to select variables; instead of selecting them by maximising information measures.  


I implemented this in R Studio using the “caret” and “party” libraries. I began by splitting the cleaned data frame into a training and test data set. I split the data in a 70% and 30% ratio, with the former going to the training data set. I saved both train and test data sets as .csv files to be used for deep learning later. After that was finished, I proceeded to write the model formula (to predict the "Status" variable - wheher a person defaults on loan repayment or not).

The tree produced an accuracy of 0.89, sensitivity of 0.97, specificity of 0.64 and Kappa statistic value of 0.67.


## Deep Learning Prediction (ANN) - Python

For the deep learning implementation, an artificial neural network with two fully connected layers was employed; for which the first layer consisted of 1024 neurons with a SoftMax activation layer, and the second layer consisted of 2 neurons with a sigmoid activation layer.

Training and test data was generated in R as .csv files and worked on in the Python/Jupyter Notebook environment.

Likelihood encoding (from the sklearn.preprocessing library's LabelEncoder) was used to encode the data within the data frames, and then the data was split into training and testing sets and trained for 75 epochs with a learning rate of 1e-2 with a categorical cross entropy loss function. 
Likelihood encoding was used to measure the effect between the target variable and the categorical predictor. It works by measuring the effect of the factor level on the output data using a logistic regression model, and the log odds of that effect is encoded into each categorical column using a map function.

The neural network yielded the following results

![neural-network-results](https://github.com/edudzi-mamattah/loan-default-prediction/blob/main/Neural%20Network%20Results.PNG)



---

NB: I only kept the structure and hyperparameters of the neural network as it is for educational purposes. I am aware that the model's performance can be greatly improved by tweaking these values.



