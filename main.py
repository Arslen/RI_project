from collections import Counter
import numpy as np
import pandas as pd
import operator
from bs4 import BeautifulSoup
from numpy.core.umath import NAN
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from math import *
import csv

from builtins import print
from functions import *


list0 = ["olive","oil","health","benefit"]
list1 = ["notting","hill","film","actors"]
list2 = ["probabilistic","models","in","information","retrieval"]
list3 = ["web","link","network","analysis"]
list4 = ["web","ranking","scoring","algorithm"]
list5 = ["supervised","machine","learning","algorithm"]
list6 = ["operating","system","mutual","exclusion"]
listoflists = []
listoflists.append(list0)
listoflists.append(list1)
listoflists.append(list2)
listoflists.append(list3)
listoflists.append(list4)
listoflists.append(list5)
listoflists.append(list6)
list_queries= [["olive","oil","health","benefit"],["notting","hill","film","actors"],["probabilistic","models","in","information","retrieval"]
    ,["web","link","network","analysis"],["web","ranking","scoring","algorithm"],["supervised","machine","learning","algorithm"],["operating","system","mutual","exclusion"]]
biglist =   ['algorithm','benefit','operating','supervised','film','actors',
            'learning','analysis','link','models','system','machine',
            'exclusion','information','retrieval','health','oil','mutual',
            'network','ranking','hill','probabilistic','olive','notting','in',
            'web','scoring']


list_requests = ["2009011", "2009036", "2009067", "2009073", "2009074", "2009078", "2009085"]
number_request = 0
number_result = 1
#./Text_Only_Ascii_Coll_MWI_NoSem


with open("../Text_Only_Ascii_Coll_MWI_NoSem") as infile:
    soup = BeautifulSoup(infile, "lxml")
    number_documents = len(soup.find_all("doc"))
    vars = soup.find_all("doc")
    list_dataframe=[]
    for request in list_requests:
        index = list_requests.index(request)
        df = pd.DataFrame([])
        i=1
        number_of_words=0

        for el in vars:
            docno = el.find("docno").contents[0]
            score=0
            word_of_doc=0
            for x in el.find_all(text=True, recursive=False):
                word_of_doc = len(x.split())
                number_of_words = number_of_words+ word_of_doc
                a = Counter(x.split()).most_common()
                temp_dict={}
                array = []
                for key, value in a:
                    if key in list_queries[index]:
                        temp_dict[key]=value
                        array.append(key)
                missing_words = set(list_queries[index])-set(array)

                if len(temp_dict.keys())!= 0:
                    dict = {}
                    for word in missing_words:
                        dict[word] = 0
                    dict.update(temp_dict)
                    data = pd.DataFrame([dict],index= [docno],columns=dict.keys())
                    e = pd.Series(word_of_doc)
                    data = data.assign(word_of_doc=e.values)
                    df = df.append(data)

                    '''tf = 0
                    idf = 0 
                    score = 0
                    words = len(Counter(x.split()))
                    for key_dict, value_dict in dict.items():
                        print(key_dict, str(value_dict))
                        a = int(value_dict)
                        tf = tf + 1 + log(a)
                        idf = idf + log(9804 / a)
                        score = (tf * idf) + score
                    print(score)'''
        df.loc['Total'] = df.sum()
        list_dataframe.append(df)
    index=0
    for df in list_dataframe:
        #ltn function
        '''score_dict = {}
        print(index)
        for i, row in df.iterrows():
            score=0
            for word in list_queries[index]:
                if (row[word]!= 0) & (df.at['Total', word]!= 0) :
                    score = score+(1+log(row[word])*(log(len(vars)/df.at['Total',word])))
            score_dict[i]=score
        score_dict = sorted(score_dict.items(), key=operator.itemgetter(1), reverse=True)
        score_dict.pop(0)
        #df = df.sort_values(by=['score'], ascending=False)
        '''
        # bm25 function 232
        score_dict = {}
        b=0.75
        k=1.5
        for i, row in df.iterrows():
            score=0
            for word in list_queries[index]:
                if (row[word]!= 0) & (df.at['Total', word]!= 0) :
                    avdl=df.ix[i,"word_of_doc"]/number_of_words
                    upper= ((1+k)*row[word])#*(log((len(vars)-df.at['Total',word]+0.5)/(df.at['Total',word]+0.5)))
                    bellow= row[word]+(k*((1-b)+(b*(number_documents/avdl))))
                    score = score+(upper/bellow)
            score_dict[i]=score
        score_dict = sorted(score_dict.items(), key=operator.itemgetter(1), reverse=True)
        score_dict.pop(0)



        f=1
        for i, row in score_dict:
            with open("./runs/ArslenMarouane_04_02_bm25_articles_k1.5b0.75.txt", "a") as res:
                if f > 1500:
                    break
                else:
                    if i !="Total":
                        res.write(str(list_requests[index]) + " " + "Q0" + " " + str(i) + " " + str(f) + " " + str(row) + " " + "ArslenMarouane" + " " + "/article[1]" + "\n")
                        f = f + 1
        index = index +1
    infile.close()

        #TFList = TFListLTN(biglist, soup.find_all("doc"))
        #IDFList = IDFListLTN(biglist, number_documents, soup.find_all("doc"))
print("done")
# Create TF IDF List of words in documents
#for i in TFList.keys():
    #TFList[i][:] = [x * IDFList[i] for x in TFList[i]]


# Create TF IDF List of words in query

#TFIDFListQueries = defaultdict(list)
#for l in listoflists:
    #for i in l:
        #TFIDFListQueries[listoflists.index(l)].append((1/len(l))*IDFList[i])



###### DEBUG #######

#for key,val in (TFList.items()):
#    print (key, "=>", val)
#
#for key,val in (TFIDFListQueries.items()):
#    print (key, "=>", val)
#
#for key,val in (IDFList.items()):
#    print (key, "=>", val)
