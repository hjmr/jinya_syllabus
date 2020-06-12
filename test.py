import pandas as pd
import pickle

sum_topic_odds = [0,0,0,0,0,0,0,0,0,0,0,0]
def search_goodat_topic(nendo,code,grade):
    taken_class = df[(df['年度']==nendo) & (df['時間割コード']==code)]
    topic_grades = [float(n)*grade for n in taken_class['トピックの確率'].values.tolist()[0]]
    return [x+y for(x,y) in zip(topic_grades,sum_topic_odds)]


df = pd.read_pickle('syllabus.pkl')

# sum_topic_odds = search_goodat_topic(2016,'1C240',4)
# print(sum_topic_odds)
sum_topic_odds = search_goodat_topic(2016,'1C261',4)
print(sum_topic_odds)





array = df['トピックの確率'].values.tolist()
array_float=[]
for row in array:
    row=[float(n) for n in row]
    array_float.append(row)
