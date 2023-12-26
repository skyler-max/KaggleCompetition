# Tf-idf函数：用于文本转向量
from sklearn.feature_extraction.text import TfidfVectorizer
# 还原词根函数：用于还原每个单词
from gensim.parsing import PorterStemmer
# 随机森林分类器
from sklearn.ensemble import RandomForestClassifier
# SVM分类器
from sklearn.svm import SVC
# 贝叶斯分类器
from sklearn.naive_bayes import MultinomialNB
# csv:用于表格读取
import csv


def generate_train_data():
    """
    :return:训练集列表[text1_string, text2_string, text3_string, ...]，训练集标签[label1, label2, label3...]
    """
    # 训练集X特征
    X_train = []
    # 生成词根还原类
    pstem = PorterStemmer()
    # 训练集Y标签
    Y_train = []
    with open('./cleaned_data_train.csv', 'r', encoding='utf-8') as train_set:
        for line in train_set:
            # 对文本去乱码
            text = line.split(',')[1].replace('\x9d', '').replace('\x81', '').strip()
            # 获得单词列表
            words = text.split()
            # 列表生成式：对每个单词还原词根
            text = [pstem.stem(word) for word in words]
            # 将文本列表转化为字符串
            text = ' '.join(text)
            # 加入训练集X特征
            X_train.append(text)
            # 获取分类标签
            label = line.split(',')[2].strip()
            # 加入Y标签
            Y_train.append(label)
        # 去除第一个元素：id
        X_train.pop(0)
        # 去除第一个元素：target
        Y_train.pop(0)
    return X_train, Y_train


def generate_test_data():
    """
    :return: 测试集列表[text1_string, text2_string, text3_string, ...]
    """
    # 测试集X特征
    X_test = []
    # 生成词根还原类
    pstem = PorterStemmer()
    with open('./cleaned_data_test.csv', 'r', encoding='GB2312') as test_set:
        for line in test_set:
            # 对文本去乱码
            text = line.split(',')[1].replace('\x9d', '').replace('\x81', '').strip()
            # 获得单词列表
            words = text.split()
            # 列表生成式：对每个单词还原词根
            text = [pstem.stem(word) for word in words]
            # 将文本列表转化为字符串
            text = ' '.join(text)
            # 加入训练集X特征
            X_test.append(text)
        # 去除第一个元素：id
        X_test.pop(0)
    return X_test


def get_test_id():
    # 获取提交数据中的id
    test_Id = []
    with open('./sample_submission1.csv', 'r', encoding='utf-8') as test_id:
        for line in test_id:
            #获取id,便于填写数据
            id = line.split(',')[0]
            # 加入列表
            test_Id.append(id)
    # 去除第一个元素：id
    test_Id.pop(0)
    return test_Id


def get_vector(X_train, X_test):
    """
    :param X_train:训练集X特征列表
    :param X_test: 测试集X特征列表
    :return: 训练集向量列表，测试集向量列表
    """
    # 转向量
    # 生成tf-id类
    tf_id_vec = TfidfVectorizer(ngram_range=(1, 3))
    # 训练集X特征转向量
    X_tf_train = tf_id_vec.fit_transform(X_train)
    # 测试集X特征转向量
    X_tf_test = tf_id_vec.transform(X_test)
    return X_tf_train, X_tf_test


def model_generator(X_tf_train, Y_train, X_tf_test):
    # 随机森林预测结果
    Y1 =[]
    # SVM预测结果
    Y2 =[]
    # 贝叶斯预测机构
    Y3 =[]
    # 随机森林
    RF = RandomForestClassifier()
    # 训练
    RF.fit(X_tf_train, Y_train)
    # 预测
    Y_test1 = RF.predict(X_tf_test)
    # 结果放进Y1
    Y1 = [each for each in Y_test1]

    # SVM
    SVM = SVC()
    # 训练
    SVM.fit(X_tf_train, Y_train)
    # 预测
    Y_test2 = SVM.predict(X_tf_test)
    # 结果放进Y2
    Y2 = [each for each in Y_test2]

    # 贝叶斯训练
    NB = MultinomialNB(alpha=1).fit(X_tf_train, Y_train)
    Y_test3 = NB.predict(X_tf_test)
    # 结果放进Y3
    Y3 = [each for each in Y_test3]

    #Y1+Y2+Y3投票
    y_test = []
    for i in range(len(Y_test1)):
        voter = int(Y_test1[i]) + int(Y_test2[i]) + int(Y_test3[i])
        if voter <= 1:
            y_test.append('0')
        else:
            y_test.append('1')
    return y_test


def write(path, pred, test_id):
    """
    :param path: 写入路径
    :param pred: 预测结果列表
    :param test_id: 测试样本id列表
    :return: 输出文本
    """
    with open(path, 'w', encoding='utf-8', newline='' "") as f:
        # csv写者类
        csv_write = csv.writer(f)
        # 第一行属性名
        data_title = ['id', 'target']
        # 写入第一行
        csv_write.writerow(data_title)
        # 将预测结果写入每一行
        for i in range(len(pred)):
            data_row = [test_id[i], str(pred[i])]
            csv_write.writerow(data_row)

