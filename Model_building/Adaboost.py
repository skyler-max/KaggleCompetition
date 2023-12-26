# -*- coding: utf-8 -*-

'''
@Time    : 2020/11/17 10:47
@Author  : 林英超
@FileName: Adaboost.py
@Software: PyCharm
@Description: 测试Adaboost
 
'''

import Main
import Model
import numpy as np
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_gaussian_quantiles

X_train, Y_train = Model.generate_train_data()
X_test = Model.generate_test_data()
X_train_tf, X_test_tf = Model.get_vector(X_train, X_test)
max_score = 0
max_n=0
for n in range(150, 350, 10):

    bdt = RandomForestClassifier(n_estimators=n)
    print('在跑了在跑了')
    bdt.fit(X_train_tf, Y_train)
    # print(bdt.score(X_train_tf, Y_train))
    ss = bdt.score(X_train_tf, Y_train)
    if ss > max_score:
        max_score = ss
        max_n = n
        print(max_score)

