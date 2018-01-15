from collections import Counter
import numpy as np
import pandas as pd
import operator
from bs4 import BeautifulSoup
import glob
from numpy.core.umath import NAN
import re
from math import *
import csv
from lxml import etree
from builtins import print
from functions import *
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

ps = PorterStemmer()

stopWords = set(stopwords.words('english'))

list0 = ["olive", "oil", "health", "benefit"]
list1 = ["notting", "hill", "film", "actors"]
list2 = ["probabilistic", "models", "in", "information", "retrieval"]
list3 = ["web", "link", "network", "analysis"]
list4 = ["web", "ranking", "scoring", "algorithm"]
list5 = ["supervised", "machine", "learning", "algorithm"]
list6 = ["operating", "system", "mutual", "exclusion"]
listoflists = []
listoflists.append(list0)
listoflists.append(list1)
listoflists.append(list2)
listoflists.append(list3)
listoflists.append(list4)
listoflists.append(list5)
listoflists.append(list6)
list_queries = [["olive", "oil", "health", "benefit"], ["notting", "hill", "film", "actors"],
                ["probabilistic", "models", "in", "information", "retrieval"]
    , ["web", "link", "network", "analysis"], ["web", "ranking", "scoring", "algorithm"],
                ["supervised", "machine", "learning", "algorithm"], ["operating", "system", "mutual", "exclusion"]]
biglist = ['algorithm', 'benefit', 'operating', 'supervised', 'film', 'actors',
           'learning', 'analysis', 'link', 'models', 'system', 'machine',
           'exclusion', 'information', 'retrieval', 'health', 'oil', 'mutual',
           'network', 'ranking', 'hill', 'probabilistic', 'olive', 'notting', 'in',
           'web', 'scoring']

list_requests = ["2009011", "2009036", "2009067", "2009073", "2009074", "2009078", "2009085"]
number_request = 0
number_result = 1
df = pd.DataFrame([])
files = glob.glob("../coll/*.xml")
i = 1
number_of_words = 0
query_stem = []
for q in biglist:
    query_stem.append(ps.stem(q))
list_queries = [[ps.stem(token) for token in query] for query in list_queries]
i = 0
docs = []
docsApperance = {}
for file in files:
    docs.append(file.split("/")[2].split('.')[0])

for file in sorted(files):
    with open(file, encoding="utf8") as infile:
        soup = BeautifulSoup(infile, "xml")
        docno = soup.find("id").contents[0]
        links = soup.find_all("link")
        for i in range(0,len(links)):
            if links[i].attrs != {}:
                docNum=0
                if 'xlink:href' in links[i].attrs:
                    try:
                        docNum = links[i].attrs['xlink:href'].split('/')[2].split('.')[0]
                    except IndexError:
                        docNum=0
                    if docNum in docs:
                        if docNum not in docsApperance:
                            docsApperance[docNum] = 1
                        else:
                            docsApperance[docNum] += 1
        score = 0
        word_of_doc = 0
        text = soup.get_text()
        x = ''.join(map(lambda c: '' if c in '0123456789!@#$%^&*()[]{};:,./<>?\|`~-=_+' else c, text))
        words = word_tokenize(x)
        wordsFiltered = []
        for w in words:
            if w not in stopWords:
                wordsFiltered.append(ps.stem(w))
        word_of_doc = len(wordsFiltered)
        number_of_words = number_of_words + word_of_doc
        a = Counter(wordsFiltered).most_common()
        temp_dict = {}
        array = []

        for key, value in a:
            if key in query_stem:
                temp_dict[key] = value
                array.append(key)
                for query in list_queries:
                    index = list_queries.index(query)
                    bellow = len(query) - 1
                    temp_dict["q" + str(index)] = 0
                    for i in range(len(query) - 1):
                        if (query[i] in wordsFiltered) and (query[i + 1] in wordsFiltered):
                            nearIndex = wordsFiltered.index(query[i + 1]) - wordsFiltered.index(query[i])
                            if (nearIndex == 1):
                                a = 1 / bellow
                                temp_dict["q" + str(index)] += a
        missing_words = set(query_stem) - set(array)

        if len(temp_dict.keys()) != 0:
            dict = {}
            for word in missing_words:
                dict[word] = 0
            dict.update(temp_dict)
            dict["word_of_doc"] = word_of_doc
            df = df.append(pd.DataFrame([dict], index=[docno], columns=dict.keys()))
        i = i + 1
        infile.close()
df.loc['Total'] = df.sum()
df_words = {}
for word in query_stem:
    df_words[word] = (df[word] != 0).sum()
df = df.append(pd.DataFrame([df_words], index=["df_words"], columns=df_words.keys()))
index = 0
for request in list_requests:
    #ltn function
    '''score_dict = {}

    ltc_sqrt = 0
    for i, row in df.iterrows():
        score=0
        if (i !="df_words") & (i!="Total"):
            for word in list_queries[index]:
                if (row[word]!= 0) & (df.at['Total', word]!= 0) :
                    score = score+(1+log(row[word])*(log(len(files)/df.at['df_words',word])))
            # link network weight, if there is a doc which appearing n time in the link tag of the corpus, we add the link network weight,
            # it's calculated by multiplying the current score with (N/Number of docs in the corpus)
            if i in docsApperance:
                score += score * (docsApperance[i] / len(files))
            if row["q" + str(index)]:
                score += score * row["q" + str(index)]
            score_dict[i]=score
            ltc_sqrt = ltc_sqrt + (score * score)
    '''
    # ltc function
    score_dict = {}
    ltc_sqrt = 0
    for i, row in df.iterrows():
        score = 0
        ltc_sqrt = 0
        if (i != "df_words") & (i != "Total"):
            for word in list_queries[index]:
                if (row[word] != 0) & (df.at['Total', word] != 0):
                    ltn = (1 + log(row[word])) * (log(len(files) / df.at['df_words', word]))
                    ltc_sqrt = ltc_sqrt + (ltn * ltn)
                    score = score + ltn
            # ltc function
            print(ltc_sqrt)
            try:
                score_dict[i] = float(score) / float(math.sqrt(ltc_sqrt))
            except ZeroDivisionError:
                score_dict[i] = 0

    score_dict = sorted(score_dict.items(), key=operator.itemgetter(1), reverse=True)

    # df = df.sort_values(by=['score'], ascending=False)
    # bm25 function 232
    '''score_dict = {}
    b = 1
    k = 1.5
    avdl = df.ix["Total", "word_of_doc"] / len(files)
    for i, row in df.iterrows():
        score = 0
        for word in list_queries[index]:
            if (row[word] != 0) & (df.at['Total', word] != 0):
                upper = ((1 + k) * row[word]) * (
                log((len(files) - (df.at['df_words', word] - 1) + 0.5) / ((df.at['df_words', word] - 1) + 0.5)))
                bellow = row[word] + (k * ((1 - b) + (b * (df.ix[i, "word_of_doc"] / avdl))))
                score = score + (upper / bellow)
        if row["q" + str(index)]:
            score += score * row["q" + str(index)]
        score_dict[i] = score
    score_dict = sorted(score_dict.items(), key=operator.itemgetter(1), reverse=True)
    '''
    f = 1
    for i, row in score_dict:
        with open("./runs/ArslenMarouane_08_02_ltc_xml.txt", "a") as res:
            if f > 1500:
                break
            else:
                if (i != "Total") & (i != "df_words"):
                    res.write(str(request) + " " + "Q0" + " " + str(i) + " " + str(f) + " " + str(
                        row) + " " + "ArslenMarouane" + " " + "/article[1]" + "\n")
                    f = f + 1
    index = index + 1

    # TFList = TFListLTN(biglist, soup.find_all("doc"))
    # IDFList = IDFListLTN(biglist, number_documents, soup.find_all("doc"))
print("done")
# Create TF IDF List of words in documents
# for i in TFList.keys():
# TFList[i][:] = [x * IDFList[i] for x in TFList[i]]


# Create TF IDF List of words in query

# TFIDFListQueries = defaultdict(list)
# for l in listoflists:
# for i in l:
# TFIDFListQueries[listoflists.index(l)].append((1/len(l))*IDFList[i])


###### DEBUG #######

# for key,val in (TFList.items()):
#    print (key, "=>", val)
#
# for key,val in (TFIDFListQueries.items()):
#    print (key, "=>", val)
#
# for key,val in (IDFList.items()):
#    print (key, "=>", val)