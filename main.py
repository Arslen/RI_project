from bs4 import BeautifulSoup
import re
import math
from functions import *


list0 = ["olive","oil","health","benefit"]
list1 = ["notting","hill","film","actors"]
list2 = ["probabilistic","models","in","information","retrieval"]
list3 = ["web","link","network","analysis"]
list4 = ["web","ranking","scoring","algorithm"]
list5 = ["supervised","machine","learning","algorithm"]
list6 = ["operating","system","mutual","exclusion"]
biglist =   ['algorithm','benefit','operating','supervised','film','actors',
            'learning','analysis','link','models','system','machine',
            'exclusion','information','retrieval','health','oil','mutual',
            'network','ranking','hill','probabilistic','olive','notting','in',
            'web','scoring']


list_requests = ["2009011", "2009036", "2009067", "2009073", "2009074", "2009078", "2009085"]
number_request = 0
number_result = 1
#./Text_Only_Ascii_Coll_MWI_NoSem

with open("./Text_Only_Ascii_Coll_MWI_NoSem") as fp:
    soup = BeautifulSoup(fp, "lxml")
    number_documents = len(soup.find_all("doc"))
    # with open("./results", "w") as res:
    #     res.write(
    #             list_requests[number_request] + " " +
    #             "Q0" + " " +
    #              + " " +
    #             number_result + " " +
    #             score + " " +
    #             "ArslenMarouane" + " " +
    #             "/article[1]" + "\n"
    #              )

    for key,val in (TFListLTN(biglist, soup.find_all("doc"))).items():
        print (key, "=>", val)

    #print (IDFList(list0, number_documents, soup.find_all("doc")))
