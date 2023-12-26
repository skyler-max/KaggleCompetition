import csv
with open('C:\\Users\\34214\Desktop\\train_tweet.csv','r') as csvfile:
    reader1 = csv.reader(csvfile)
    reader2 = csv.reader(csvfile)
    column_keyword = [row[2] for row in reader1]
    column_text = [row[4] for row in reader2]
    print(len(column_keyword))
    print(len(column_text))
    # for i in range(len(column_keyword)):
    #     if column_keyword[i] != "":
    #         text = column_text[i]
    #         print(text)