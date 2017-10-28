from bs4 import BeautifulSoup
import re
import math

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
    with open("../Text_Only_Ascii_Coll_MWI_NoSem") as infile:
        soup = BeautifulSoup(infile, "lxml")
        number_documents = len(soup.find_all("doc"))
        vars= soup.find_all("doc")
        i=1
        for el in vars:
            docno= el.find("docno").contents[0]
            score = 1.23
            with open("./runs/ExempleRunArslenMarouane_01_01_Text_Only.txt", "a") as res:
                if i>1500:
                    break
                res.write(str(request) + " " + "Q0" + " " + str(docno) + " " + str(i) + " " + str(score) + " " + "ArslenMarouane" + " " + "/article[1]" + "\n")
                i=i+1
        infile.close()
        print(request)
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

print("okok")


###### DEBUG #######

#for key,val in (TFList.items()):
#    print (key, "=>", val)
#
#for key,val in (TFIDFListQueries.items()):
#    print (key, "=>", val)
#
#for key,val in (IDFList.items()):
#    print (key, "=>", val)
