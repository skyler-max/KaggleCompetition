from collections import defaultdict

import json
import jieba


if __name__ == '__main__':
    freq = defaultdict(int)
    with open("./freq_train.json", "r", encoding="utf-8") as f:
        lis = json.load(f)
    # with open("./freq_test.json", "r", encoding="utf-8") as f:
    #     lis = json.load(f)
    for l in lis:
        for w in jieba.lcut(l):
            freq[w] += 1
    print("words " + str(len(freq.keys())))
    print("------------")
    # for fr in freq.items():
    #     if fr[1] == 1:
    #         print(fr[0])
    #         print(spell_check(fr[0]))
    #         print("----")
    with open("./freq_train_result.json", "w", encoding="utf-8") as f:
        json.dump(freq, f, indent=1, ensure_ascii=False)
    # with open("./freq_test_result.json", "w", encoding="utf-8") as f:
    #     json.dump(freq, f, indent=1)
