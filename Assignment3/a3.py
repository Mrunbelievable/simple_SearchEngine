from pathlib import Path
import json
from bs4 import BeautifulSoup
import re
import math
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk import word_tokenize
from stop_words import get_stop_words
from collections import defaultdict
import nltk



analysis_root_dir = "/Users/hanson/Desktop/ANALYST"
id_url = {}
real_id_url = {}
real_word_posting = {}
word_posting = {}
#遍历analyst文件里的所有json文件
def parse_dir(root_dir):
        path = Path(root_dir)
 
        all_json_file = list(path.glob('**/*.json'))
         
        parse_result = []
        word_posting = {}
        
        doc_id = 1
        all_document = {} # contain {id:text, }
        result = {} # index result
        submit = './report/submit2.json'
        for json_file in all_json_file:
               with json_file.open() as f:
                     all_words = []
                     position = {}
                     json_result = json.load(f)
                     bs = BeautifulSoup(json_result['content'], "html.parser")
                     text = bs.get_text().replace('\n',' ').replace('\r','').replace('\t','')
                     # store {id:text}
                     all_document[doc_id] = text
#                     print(text)
                     # store {id:url}
                     id_url[doc_id] = json_result['url']

                     # update inverted index
                     result.update((build_index(all_document, doc_id, text)))
                     # update {id:url} info
                     real_id_url.update(id_url)
               # writing inverted index into a json file
               with open(submit, 'w') as file:
                 json.dump(result, file , indent=4, separators=(',', ': '))

               # write {id:url, }into a json file
               with open('/Users/hanson/Desktop/report/doc_id.json','w') as file_2:
                json.dump(real_id_url, file_2, indent=4, separators=(',', ': '))
               # increse id
               doc_id+=1
#               break
               
def getPosting(word,text,doc_id):
    words_posting = {}
    id_words_posting = {}
    for each in re.finditer(word, text):
        if word in words_posting:
           words_posting[word].append(each.start())
        else:
           words_posting = {word:[each.start()]}
    return words_posting

# 以下版本的 build_index 是返回一个index 包含 单词出现的文章集合

def build_index(docu_set, doc_id, text):

      all_words = []
      token_words = []
      position = {}

      for i in docu_set.values():
           token_words = tokenize(i)
           all_words.extend(token_words)

      set_all_words=set(all_words)
      
      # store {id: word:{position} }
      for words in all_words:
        position.update(getPosting(words,text,doc_id))
      word_posting[doc_id] = position
      with open('/Users/hanson/Desktop/report/word_position.json','w') as file_3:
        json.dump(word_posting, file_3, indent=4, separators=(',', ': '))
      # compute tf_idf
      word_tf_idf = computeWord_tf(all_words)
      id_tf_idf = ()
      result = {}
      invert_index=dict()
      # create inverted index
      for b in set_all_words:
          temp=[]
          for j in docu_set.keys():
              field = docu_set[j]
              split_field = tokenize(field)
              #split_field=field.split()
              if b in split_field:
                  id_tf_idf = (j,word_tf_idf[b])
                  temp.append(id_tf_idf)
          invert_index[b]=temp
      return invert_index



def tokenize(text):
       words = []
       list = re.findall(r"[a-zA-Z]{3,}", text)
       word_freq = [item.lower() for item in list ]
       for i in word_freq:
         if i not in get_stop_words('english'):
             words.append(i.lower())
       return words

def computeWord_tf(Token):
  word_freq = dict()
  tf = {}
  for t in Token:
     if t in word_freq:
        word_freq[t] += 1
     else:
        word_freq[t] = 1

  for key in word_freq.keys():
     tf[key] = word_freq[key] /len(word_freq)
  idf={}
  word_doc=defaultdict(int)
  doc_num=len(Token)
  for i in word_freq.keys():
    for j in Token:
        if i in j:
            word_doc[i]+=1
  for i in word_freq.keys():
    idf[i]=math.log(doc_num/word_doc[i]+1)
  word_tf_idf={}
  for i in word_freq.keys():
    word_tf_idf[i]=tf[i]*idf[i]
  
  return word_tf_idf


parse_dir(analysis_root_dir)
