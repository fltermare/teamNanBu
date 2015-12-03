import csv
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xgboost as xgb
from sklearn.svm import SVR
from sklearn import ensemble
from sklearn import datasets
from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error

##############################################################################
##############################################################################

# Import data set and process
# X = data
# y = target

print("[*] Read merged training data")
train = pd.read_csv("./csv/trainMerged.csv") #need to change to trainMerged.csv
target = train["Expected"]

#idx= [2,]
data = train.iloc[:,2:-1]
dataT = np.array(data.values.tolist())
targetT = np.array(target.values.tolist())

print("[*] Done")

print("[*] Read merged testing data")
testcsv = pd.read_csv("./csv/testMerged.csv")
testdata = testcsv.iloc[:,2:]

print("[*] Done")

X, y = shuffle(dataT, targetT, random_state=13)
X = X.astype(np.float32)

X_train, y_train = X, y
X_test = testdata

#X2 and y2 is used to compute the mse by dividing the training set into 10 parts
#Use 9 parts for training and 1 part for testing

offset = int(X.shape[0] * 0.9)
X2_train, y2_train = X[:offset], y[:offset]
X2_test, y2_test = X[offset:], y[offset:]

##############################################################
#                                                                                                                                       #
#                            eXtreme Gradient Boosting Regression                                   #
#                                                                                                                                       #
##############################################################

# Fit regression model

if sys.argv[1] == 'xgb':
    print("[*] Running XGB")
    print("[*] Fit regression model")
    params = {'n_estimators': 5000, 'max_depth': 4, 'min_samples_split': 2,'learning_rate': 0.01, 'loss': 'ls'}
    #clf = ensemble.GradientBoostingRegressor(**params)
    #clf.fit(X_train, y_train)

    #clf2 = ensemble.GradientBoostingRegressor(**params)
    #clf2.fit(X2_train, y2_train)
    clf2 = xgb.XGBRegressor(max_depth=6, n_estimators=500, learning_rate=0.05, nthread=1)
    clf2.fit(X2_train, y2_train)
    print("[*] Compute MSE")
    predict1st = clf2.predict(X2_test)
    print(predict1st)
    mse = mean_squared_error(y2_test, predict1st)
    print("MSE: %.4f" % mse)

###############################################################################
# Output the prediction result to predict_gbr.csv

    print("[*] Output the prediction file")
    predict = clf2.predict(X_test)
    iid = np.array(testcsv['Id'])
    predictPair = list(np.vstack((iid.astype(int),predict)).T)

    fw = open("predict_xgb.csv", 'w')
    fw.write("Id,Expected\n")
    k = 0
    for i in range(1,717624):
        #print("[*] For instance " + str(i))
        if i != predictPair[k][0]:
            fw.write(str(i) + ",0.254" + "\n")
        elif i == predictPair[k][0]:
            if predictPair[k][1] < 0:
                fw.write(str(i) + ",0" + "\n")
            else:
                fw.write(str(i) + "," + str(predictPair[k][1]) + "\n")
            k = k+1
    fw.write("717624,0.254" + "\n")
    fw.write("717625,0.254" + "\n")

###############################################################################
# Plot training deviance
# compute test set deviance
    '''
    test_score = np.zeros((params['n_estimators'],), dtype=np.float64)

    for i, y_pred in enumerate(clf2.staged_decision_function(X2_test)):
        test_score[i] = clf2.loss_(y2_test, y_pred)

    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.title('Deviance')
    plt.plot(np.arange(params['n_estimators']) + 1, clf2.train_score_, 'b-', label='Training Set Deviance')
    plt.plot(np.arange(params['n_estimators']) + 1, test_score, 'r-', label='Test Set Deviance')
    plt.legend(loc='upper right')
    plt.xlabel('Boosting Iterations')
    plt.ylabel('Deviance')

###############################################################################
# Plot feature importance
    feature_importance = clf2.feature_importances_
# make importances relative to max importance
    feature_importance = 100.0 * (feature_importance / feature_importance.max())
    sorted_idx = np.argsort(feature_importance)
    pos = np.arange(sorted_idx.shape[0]) + .5
    plt.subplot(1, 2, 2)
    plt.barh(pos, feature_importance[sorted_idx], align='center')
    plt.yticks(pos, np.array(train.columns.tolist()[2:])[sorted_idx])
    plt.xlabel('Relative Importance')
    plt.title('Variable Importance')
    plt.show()
    '''
