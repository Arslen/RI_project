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
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
ps= PorterStemmer()


stopWords = set(stopwords.words('english'))
tags=["title","bdy","p","sec","table","link","list","header","article"]

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



'''root = etree.fromstring('<foo><bar>Data</bar><bar><baz>data</baz>'
                        '<baz>sasa</baz></bar></foo>')

tree = etree.ElementTree(root)
for e in root.iter():
    if "sasa" in str(etree.tostring(e,method="text")):
        print (tree.getpath(e))
'''       
list_requests = ["2009011", "2009036", "2009067", "2009073", "2009074", "2009078", "2009085"]
number_request = 0
number_result = 1
df = pd.DataFrame([])
files = glob.glob("../coll/*.xml")
i=1
number_of_words=0
number_of_titles=0
number_of_section=0
query_stem = []
for q in biglist:
    query_stem.append(ps.stem(q))
list_queries = [[ps.stem(token) for token in query] for query in list_queries]
i=0
dict_path = {}
for file in sorted(files):
    with open(file, encoding="utf8") as infile:
        soup = BeautifulSoup(infile, "xml")
        docno = soup.find("id").contents[0]
        score=0
        word_of_doc=0
        text=soup.get_text()
        dict_path[docno]={}
        xml = bytes(bytearray(soup.article.prettify(), encoding='utf-8')) 
        a=etree.XML(xml)
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        root = etree.fromstring(xml, parser=parser)
        tree = etree.ElementTree(root)
        number_of_section = number_of_section+ sum(1 for _ in root.iter("sec"))
        number_of_titles = number_of_titles+ sum(1 for _ in root.iter("title"))
        
        '''for query in list_queries:
            
            path= ''
            for w in query:
                if w in b:
                    for child in soup.descendants:
                        if child.name is not None:
                            if w in child.contents[0]:
                                tab = []
                                tab.append(child.name)
                                l = soup.find(child.name).parent()
                                path = "/"
                                for parent in soup.find(child.name).parents:
                                    if parent is not None:
                                        tab.append(parent.name)
                                for word_tab in reversed(tab):
                                    if word_tab in tags:
                                        path = path + word_tab + '/'
            '''
        x=''.join(map(lambda c: '' if c in '0123456789!@#$%^&*()[]{};:,./<>?\|`~-=_+' else c, text))            
        words = word_tokenize(x)
        wordsFiltered = []
        paths=[]
        index = list_queries.index(query)
        occurence= {}
        print(docno)
        for w in biglist:
            occurence[w]= 0
            for e in root.iter("sec"):
                if w in str(etree.tostring(e,encoding='UTF-8',method="text")):
                    occurence[w] = occurence[w]+str(etree.tostring(e,encoding='UTF-8',method="text")).split().count(w)
                    print (tree.getpath(e))
            for e in root.iter(w):
                if w in str(etree.tostring(e,encoding='UTF-8',method="text")):
                    occurence[w] = occurence[w]+str(etree.tostring(e,encoding='UTF-8',method="text")).split().count(w)
                    print (tree.getpath(e))
        print(occurence)
                    #print(w)
                    
                    #paths.append(tree.getpath(e))
        #dict_path[docno][w]=paths
        for w in words:
            if w not in stopWords:
                wordsFiltered.append(ps.stem(w))
        word_of_doc = len(wordsFiltered)
        number_of_words = number_of_words+ word_of_doc
        a = Counter(wordsFiltered).most_common()
        temp_dict={}
        array = []

        for key, value in a:
            if key in query_stem:
                temp_dict[key]=value
                array.append(key)
        missing_words = set(query_stem)-set(array)

        if len(temp_dict.keys())!= 0:
            dict = {}
            for word in missing_words:
                dict[word] = 0
            dict.update(temp_dict)
            dict["word_of_doc"]=word_of_doc
            df = df.append(pd.DataFrame([dict], index=[docno], columns=dict.keys()))
        i=i+1
        infile.close()
df.loc['Total'] = df.sum()
df_words={}
for word in query_stem:
    df_words[word]=(df[word] != 0).sum()
df=df.append(pd.DataFrame([df_words], index=["df_words"], columns=df_words.keys()))
index=0
print(df)
for request in list_requests:
    #ltn function
    score_dict = {}
    ltc_sqrt = 0
    for i, row in df.iterrows():
        score=0
        if (i !="df_words") & (i!="Total"):
            for word in list_queries[index]:
                if (row[word]!= 0) & (df.at['Total', word]!= 0) :
                    score = score+(1+log(row[word])*(log(len(files)/df.at['df_words',word])))
            score_dict[i]=score
            ltc_sqrt = ltc_sqrt + (score * score)
    for i, row in score_dict.items():
        score_dict[i] = row / math.sqrt(ltc_sqrt)
    score_dict = sorted(score_dict.items(), key=operator.itemgetter(1), reverse=True)
    #df = df.sort_values(by=['score'], ascending=False)

    # bm25 function 232
    '''score_dict = {}
    b=1
    k=1.5
    avdl = df.ix["Total", "word_of_doc"] / len(files)
    for i, row in df.iterrows():
        score=0
        for word in list_queries[index]:
            if (row[word]!= 0) & (df.at['Total', word]!= 0) :
                upper= ((1+k)*row[word])*(log((len(files)-df.at['df_words',word]+0.5)/(df.at['df_words',word]+0.5)))
                bellow= row[word]+(k*((1-b)+(b*(df.ix[i,"word_of_doc"]/avdl))))
                score = score+(upper/bellow)
        score_dict[i]=score
    score_dict = sorted(score_dict.items(), key=operator.itemgetter(1), reverse=True)
    '''
    f=1
    for i, row in score_dict:
        with open("./runs/ArslenMarouane_04_08_ltc_xml_path.txt", "a") as res:
            if f > 1500:
                break
            else:
                if (i !="Total") & (i != "df_words"):
                    res.write(str(request) + " " + "Q0" + " " + str(i) + " " + str(f) + " " + str(row) + " " + "ArslenMarouane" + " " + str(dict_path[i][request]) + "\n")
                    f = f + 1
    index = index +1

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
