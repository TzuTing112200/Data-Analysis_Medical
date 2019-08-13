#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import time
import random
from sklearn.svm import SVC
import json
from sklearn import metrics
from sklearn.model_selection import train_test_split

Data = []

print(1, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
rf = open('Classifier.json', 'r')
for r in rf.readlines():
    dic = json.loads(r)
    for key in dic:
        Data.append((dic[key][0],dic[key][1]))
rf.close()

print(2, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
X = []
y = []
i = 0
while i < 50000:
    (tX, ty) = random.choice(Data)
    if ty == 9:
        ty = 0
    elif ty == 6:
        ty = 1
    else:
        ty = 2
    
    if i % 3 == ty:
        X.append(tX)
        y.append(ty)
        i += 1
		
jsonObj = "50000筆 80% 分三類(9->0, 6->1, 2) 預測第一位數\n"

X_train = []
y_train = []
X_test = []
y_test = []
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
print(3, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
clf = SVC(gamma='auto', probability=True)
print(4, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
clf.fit(X_train, y_train)
print(5, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
y_pred = clf.predict(X_test)

print(metrics.precision_score(y_test, y_pred, average='micro'))
print(metrics.precision_score(y_test, y_pred, average='macro'))
print(metrics.recall_score(y_test, y_pred, average='micro'))
print(metrics.recall_score(y_test, y_pred, average='macro'))

tmp = metrics.classification_report(y_test, y_pred)
jsonObj += metrics.classification_report(y_test, y_pred)
jsonObj += ("-" * 50) + '\n'
print(tmp)

fileObject = open('PRval.json', 'a')
fileObject.write(jsonObj)
fileObject.close()

print("all done")
