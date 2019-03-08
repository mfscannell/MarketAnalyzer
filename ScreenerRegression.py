from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import numpy as np
import csv
import graphviz
import pydotplus

import os     
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'


data = {}
numColsIncludingY = 12

with open('ForLinearRegressionReducedSlopeOnly.csv', 'r') as f:
    rows = list(csv.reader(f, delimiter=','))
    dataArray = np.array(rows[1:], dtype=np.float)
    data['featureNames'] = rows[0][:numColsIncludingY - 1]
    data['X'] = dataArray[:, 0:numColsIncludingY - 1]
    data['Y'] = dataArray[:, numColsIncludingY - 1]

#print(dataArray)
print(data['featureNames'])
#print(data['X'])
#print(data['Y'])

clf = LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial').fit(data['X'], data['Y'])

#print('LOGISTIC REGRESSION COEFFICIENTS')
#print(clf.coef_)

reg = LinearRegression().fit(data['X'], data['Y'])
yPred = reg.predict(data['X'])
print('LINEAR REGRESSION COEFFICIENTS')
print(reg.coef_)
print('Variance score: %.2f' % r2_score(data['Y'], yPred))



