import re
import math
from collections import defaultdict

########## Miscellaneous functions ##########
def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search




#############################################



##################   LTN   ##################

def TFListLTN(l, list_doc):
    lis = defaultdict(list)
    #final_ls = [0] * len(l)
    #c = 0
    for doc in list_doc:
        for i in l:
            count = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(i), doc.contents[1]))
            if count != 0:
                lis[l[l.index(i)]].append(1 + math.log(count))
            else:
                lis[l[l.index(i)]].append(0)
    return lis


def IDFListLTN(l, number_documents, list_doc):
    ls = [0] * len(l)
    final_ls = {}
    c = 0
    for doc in list_doc:
        for i in l:
            if findWholeWord(i)(doc.contents[1]):
                ls[l.index(i)] += 1
    for x in ls:
        if x != 0:
            final_ls[l[c]] = math.log(number_documents/x)
            c += 1
        else:
            final_ls[l[c]] = math.log(number_documents)
            c += 1
    return final_ls



#############################################



##################   LTC   ##################




#############################################
