# -*- coding: utf-8 -*-

'''
@Time    : 2020/11/4 14:53
@Author  : 林英超
@FileName: Main.py
@Software: PyCharm
@Description: 
 
'''
from sklearn.ensemble import RandomForestClassifier

import Model


# 主函数，调用所有方法
def main():
    X_train, Y_train = Model.generate_train_data()
    X_test = Model.generate_test_data()
    test_id = Model.get_test_id()
    X_train_tf, X_test_tf = Model.get_vector(X_train, X_test)
    print('正在建模......请稍后......')
    bdt = RandomForestClassifier(n_estimators=150)
    bdt.fit(X_train_tf, Y_train)
    predict_list = bdt.predict(X_test_tf)
    # predict_list = Model.model_generator(X_train_tf, Y_train, X_test_tf)
    Model.write('./RF.csv', predict_list, test_id)
    print('建模成功！请查看数据！')


main()
