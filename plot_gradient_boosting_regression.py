import csv
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.svm import SVR
from sklearn import ensemble
from sklearn import datasets
from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error

###############################################################################
##############################################################################

# Import data set and process
# X = data
# y = target
print("[*] Read merged training data")
train = pd.read_csv("./csv/trainMerged.csv") #need to change to trainMerged.csv
target = train["Expected"]
data = train.ix[:,2:-1].fillna(0)
dataT = np.array(data.values.tolist())
targetT = np.array(target.values.tolist())
print("[*] Done")

print("[*] Read merged testing data")
testcsv = pd.read_csv("./csv/testMerged.csv")
testdata = testcsv.ix[:,2:].fillna(0)
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
#                                                            #
#            Gradient Boosting Regression                    #
#                                                            #
##############################################################

# Fit regression model

if sys.argv[1] == 'gbr':
    print("[*] Running Gradient Boost Regression")
    print("[*] Fit regression model")
    params = {'n_estimators': 5000, 'max_depth': 4, 'min_samples_split': 2,'learning_rate': 0.01, 'loss': 'ls'}
    #clf = ensemble.GradientBoostingRegressor(**params)
    #clf.fit(X_train, y_train)

    clf2 = ensemble.GradientBoostingRegressor(**params)
    clf2.fit(X2_train, y2_train)

    print("[*] Compute MSE")
    mse = mean_squared_error(y2_test, clf2.predict(X2_test))
    print("MSE: %.4f" % mse)

###############################################################################
# Output the prediction result to predict_gbr.csv
    '''
    print("[*] Output the prediction file")
    predict = clf.predict(X_test)
    iid = np.array(testcsv['Id'])
    predictPair = list(np.vstack((iid.astype(int),predict)).T)

    fw = open("predict_gbr.csv", 'w')
    fw.write("Id,Expected\n")
    k = 0
    for i in range(1,717624):
        print("[*] For instance " + str(i))
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
    '''
###############################################################################
# Plot training deviance
# compute test set deviance
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

################################################################
#                                                              #
#                  Support Vector Regression                   #
#                                                              #
################################################################
elif sys.argv[1] == 'svr':
# Add noise to targets
        #y[::5] += 3 * (0.5 - np.random.rand(8))
# Fit regression model
# Set the parameters
    print("[*] Running Support Vector Regression")
    print("[*] Fit regression model")
    svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1, max_iter=30000)
    #svr_lin = SVR(kernel='linear', C=1e3)
    #svr_poly = SVR(kernel='poly', C=1e3, degree=2)

# Fit and predict y2 is used to compute mse, the real output is y
    y_rbf = svr_rbf.fit(X_train, y_train).predict(X_test)
    #y2_rbf = svr_rbf.fit(X2_train, y2_train).predict(X2_test)
    #y_lin = svr_lin.fit(X_train, y_train).predict(X_test)
    #y2_lin = svr_lin.fit(X2_train, y2_train).predict(X2_test)
    #y_poly = svr_poly.fit(X_train, y_train).predict(X_test)
    #y2_poly = svr_poly.fit(X2_train, y2_train).predict(X2_test)
# Compute mse by deviding the training data into 10 parts, and use 1 part as the testing data to do validation
    #print("[*] Compute MSE")
    #mse_rbf = mean_squared_error(y2_test, y2_rbf)
    #mse_lin = mean_squared_error(y2_test, y2_lin)
    #mse_poly = mean_squared_error(y2_test, y2_poly)

    #print("MSE(RBF): %.4f" % mse_rbf)
    #print("MSE(LIN): %.4f" % mse_lin)
    #print("MSE(POLY): %.4f" % mse_poly)

# Output the prediction to predict_svr.csv
    print("[*] Output the prediction file")
    predict = y_rbf
    iid = np.array(testcsv['Id'])
    predictPair = list(np.vstack((iid.astype(int),predict)).T)

    fw = open("predict_svr.csv", 'w')
    fw.write("Id,Expected\n")
    k = 0
    for i in range(1,717624):
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
