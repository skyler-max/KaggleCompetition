import pandas as pd
import json

from collections import defaultdict
from cleanfx import*


def main_process(sets, name):
    count = defaultdict(int)
    data = defaultdict(list)
    for set in sets:
        num = set[0]
        target = set[1]  # target
        rtweet = set[2].lower().strip('\n').replace(':D', ' ').replace('åê', ' ').replace('ûó', ' ')  # text
        # print(rtweet)

        # 数据清洗
        tweet = cl_url(rtweet)  # 1.去除网址
        count["url"] += 1
        tweet = cl_html(tweet)  # 2.去除HTML
        count["html"] += 1
        tweet = cl_punct(tweet) # 3.去除标点符号
        count["emoji"] += 1
        tweet = cl_num(tweet)   # 4.去除数字
        count["stop"] += 1
        tweet = cl_emoji(tweet)  # 5.去除表情
        count["punctuation"] += 1
        tweet = cl_stop(tweet)  # 6.去除停用词
        count["number"] += 1
        tweet = cl_split_attached_words(tweet) # 7.去掉黏着词
        count["attached_words"] += 1
        tweet = cl_shortwords(tweet)  # 8.去掉短词
        count["shortwords"] += 1
        tweet = spell_check(tweet)  # 9.拼写检查
        count["spellcheck"] += 1

        print(str(num + 1))
        # print('\"' + rtweet + '\"')
        # print('INTO >> \"' + tweet + '\"')

        # if rtweet == tweet:  # 如果没有对tweet进行操作
        #     print("NO CHANGE")

        data["id"].append(num+1)
        data["text"].append(tweet)
        data["target"].append(target)

    freq_train = []
    freq_test = []

    if name == "train":
        freq_train = data["text"]  # 统计train词频
        with open("./freq_train.json", "w", encoding="utf-8") as f:
            json.dump(freq_train, f, indent=1)
        save = pd.DataFrame({  # DataFrame格式化
            "id": data["id"],
            "text": data["text"],
            "target": data["target"]
        })
    else:
        freq_test = data["text"]  # 统计test词频
        with open("./freq_test.json", "w", encoding="utf-8") as f:
            json.dump(freq_test, f, indent=1)
        save = pd.DataFrame({  # DataFrame格式化
            "id": data["id"],
            "text": data["text"]
        })
    save.to_csv("./clean_data_{}_3.csv".format(name), index=False)  # 存入csv文件
    cf = pd.Series(count)
    print(cf)
    # 保存清洗完毕的数据


if __name__ == '__main__':
    # 读取数据
    test_tweet = pd.read_csv("./test.csv")
    train_tweet = pd.read_csv("./train.csv")

    test_ncount = test_tweet.shape[0]  # 测试集数据条数
    train_ncount = train_tweet.shape[0]  # 训练集数据条数

    print('there are {} rows, {} columns in test set'.format(test_tweet.shape[0], test_tweet.shape[1]))
    print('there are {} rows, {} columns in train set'.format(train_tweet.shape[0], train_tweet.shape[1]))
    print("---------")

    targn_0 = train_tweet.target.value_counts()[0]  # non-disaster的tweet条数
    targn_1 = train_tweet.target.value_counts()[1]  # disaster的tweet条数

    # 将text和target集合在一起
    tr_sets = [[i, train_tweet.target[i], train_tweet.text[i]] for i in range(train_tweet.shape[0])]
    te_sets = [[i, "", test_tweet.text[i]] for i in range(test_tweet.shape[0])]

    main_process(tr_sets, "train")
    print("----------")
    main_process(te_sets, "test")

