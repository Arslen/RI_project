from collections import Counter
import numpy as np
import pandas as pd
import operator
from bs4 import BeautifulSoup
import glob
from numpy.core.umath import NAN
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from math import *
import csv
from lxml import etree
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
for request in list_requests:
    print(request)
    index=list_requests.index(request)
    df = pd.DataFrame([])
    files = glob.glob("../coll/*.xml")
    number_of_words = 0
    i=0
    for file in sorted(files):
        with open(file, encoding="utf8") as infile:
            soup = BeautifulSoup(infile, "xml")
            docno = soup.find("id").contents[0]
            vars = soup.get_text()
            word_of_doc = len(vars.split())
            a = Counter(vars.split()).most_common()
            temp_dict = {}
            array = []
            for key, value in a:
                if key in list_queries[index]:
                    temp_dict[key] = value
                    array.append(key)
            missing_words = set(list_queries[index]) - set(array)
            if len(temp_dict.keys()) != 0:
                dict = {}
                for word in missing_words:
                    dict[word] = 0
                dict.update(temp_dict)
                data = pd.DataFrame([dict], index=[docno], columns=dict.keys())
                e = pd.Series(word_of_doc)
                data = data.assign(word_of_doc=e.values)
                df = df.append(data)
            i=i+1
            print(i)
            infile.close()

    df.loc['Total'] = df.sum()
    #ltn function
    '''score_dict = {}
    for i, row in df.iterrows():
        score=0
        for word in list_queries[index]:
            if (row[word]!= 0) & (df.at['Total', word]!= 0) :
                score = score+(1+log(row[word])*(log(len(vars)/df.at['Total',word])))
        score_dict[i]=score
    score_dict = sorted(score_dict.items(), key=operator.itemgetter(1), reverse=True)'''
    #score_dict.pop(0)
    #df = df.sort_values(by=['score'], ascending=False)
    # bm25 function 232
    score_dict = {}
    b=0.75
    k=1.5
    for i, row in df.iterrows():
        score=0
        for word in list_queries[index]:
            if (row[word]!= 0) & (df.at['Total', word]!= 0) :
                avdl=df.ix[i,"word_of_doc"]/df.ix['Total', "word_of_doc"]
                upper= ((1+k)*row[word])#*(log((len(vars)-df.at['Total',word]+0.5)/(df.at['Total',word]+0.5)))
                bellow= row[word]+(k*((1-b)+(b*(len(files)/avdl))))
                score = score+(upper/bellow)
        score_dict[i]=score
    score_dict = sorted(score_dict.items(), key=operator.itemgetter(1), reverse=True)
    score_dict.pop(0)

    f=1
    for i, row in score_dict:
        with open("./runs/ArslenMarouane_03_06_bm25_xml_files_k1.5b0.75.txt", "a") as res:
            if f > 1500:
                break
            else:
                if i !="Total":
                    res.write(str(request) + " " + "Q0" + " " + str(i) + " " + str(f) + " " + str(row) + " " + "ArslenMarouane" + " " + "/article[1]" + "\n")
                    f = f + 1


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
