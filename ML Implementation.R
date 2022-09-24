---
title: "Machine Learning Prediction"
author: "Edudzi Mamattah"
date: '2022-04-12'
output: html_document
---
#   
# {r setup, include=FALSE}
# knitr::opts_chunk$set(echo = TRUE)
#  

 
load("loan_df_ml.Rda")
 

# ML Implementation


 
set.seed(2)
ind = sample(2, nrow(loan_df_with_pc), replace = TRUE, prob=c(0.7, 0.3))
trainset = loan_df_with_pc[ind == 1,]
testset = loan_df_with_pc[ind == 2,]
 


 
dim(trainset)
dim(testset)
 


 
str(trainset)
 

 
str(testset)
 





# Using the party model, we will create the conditional inference tree
 
library(party)
ctree.model = ctree(Status ~ . , data = trainset)

ctree.model
 

 
plot(ctree.model)
 




 
ctree.predict = predict(ctree.model, testset)
table(ctree.predict, testset$Status)
 



 
library(caret)
confusionMatrix(table(ctree.predict, testset$Status))
 





# To prepare the datasets for deep learning and encoding in python, i will convert the logical variables to factors, so that when I open them in python, they will all be of type object. 

 
trainset$approv_in_adv <- as.factor(trainset$approv_in_adv)
trainset$open_credit <- as.factor(trainset$open_credit)
trainset$business_or_commercial <- as.factor(trainset$business_or_commercial)
trainset$Neg_ammortization <- as.factor(trainset$Neg_ammortization)
trainset$interest_only <- as.factor(trainset$interest_only)
trainset$lump_sum_payment <- as.factor(trainset$lump_sum_payment)
 


 
testset$approv_in_adv <- as.factor(testset$approv_in_adv)
testset$open_credit <- as.factor(testset$open_credit)
testset$business_or_commercial <- as.factor(testset$business_or_commercial)
testset$Neg_ammortization <- as.factor(testset$Neg_ammortization)
testset$interest_only <- as.factor(testset$interest_only)
testset$lump_sum_payment <- as.factor(testset$lump_sum_payment)
 




 
str(testset)
str(trainset)
 



# write training file to csv
# Been commented out because the file has been created already
 
# write.csv(trainset, "loan_df_train.csv")
 


# write test file to csv
# Been commented out because the file has been created already
 
# write.csv(testset, "loan_df_test.csv")
 





