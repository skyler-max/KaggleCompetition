import re
import string
import wordninja
from spellchecker import SpellChecker


with open("./stopwords.txt", "r", encoding='utf-8') as f:
    stop = f.read().split('\n')

#去掉url
def cl_url(tweet):
    url = re.compile(r'https?://\S+|www\.\S+')
    return url.sub(r'', tweet)

#去掉标签<>
def cl_html(tweet):
    html = re.compile(r'<.*?>')
    return html.sub(r'', tweet)

#去掉emoji
def cl_emoji(tweet):
    emoji = re.compile("["u"\U0001F600-\U0001F64F"  # emoticons
                          u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                          u"\U0001F680-\U0001F6FF"  # transport & map symbols
                          u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                          u"\U00002702-\U000027B0"
                          u"\U000024C2-\U0001F251"
                       "]+", flags=re.UNICODE)
    return emoji.sub(r'', tweet)

#去掉标点符号
def cl_punct(tweet):
    p = string.punctuation.replace('.', '')
    table = str.maketrans('', '', p + '÷ªû¢òïó')
    return tweet.translate(table)

#去掉标点符号
def cl_stop(tweet):
    words = tweet.split()
    for word in words:
        if word in stop:
            words.remove(word)
    return ' '.join(words).strip()

#拼写检查
def spell_check(tweet):
    spell = SpellChecker()
    correct = []
    misspelled = spell.unknown(tweet.split())
    for word in tweet.split():
        if word in misspelled:
            word = spell.correction(word)
            correct.append(word)
        else:
            correct.append(word)
    return ' '.join(correct)

#去掉数词
def cl_num(tweet):
    for i, ch in enumerate(list(tweet)):
        if '0' <= ch <= '9':
            tweet = tweet.replace(ch, '')
    return tweet

#处理黏着词
def cl_split_attached_words(tweet):
    words = wordninja.split(tweet)
    return" ".join(words)

#去掉过短词
def cl_shortwords(tweet):
    words = tweet.split()
    for word in words:
        if word.isalpha():
            words = [word for word in words if len(word) > 1]
        else:
            words = [word for word in words]
    return " ".join(words)