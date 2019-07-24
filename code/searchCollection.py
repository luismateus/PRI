import sys, re
import whoosh.index as index
from whoosh import scoring
from whoosh.qparser import QueryParser

#Auxiliary functions
###################################################

def manifCountPerParty(results):

    print("Manifestos per party found in search results:")
    print()

    for k in results.keys():
        print("    " + k + " : " + str(len(results.get(k))))

    print()

def initDic(parties, keywords):
    dic = {}

    for wor in keywords: 
        wor = wor.lower() 
        dic[wor] = {}
        for par in parties:
            dic[wor][par] = 0

    return dic

def keywordCountPerParty(keywords, results):

    #Create dictionary with keyword as key and dictionary of counts per party as value
    wordDic = initDic(results.groups(), keywords)
    
    #Iterate and preproccess each document text from results
    for res in results:
        text = res['content']
        text = re.sub(r'[^\w\s]','',text).lower().split()

        #Count keyword occurences per party
        for word in text:
            if word in wordDic.keys():
                wordDic[word][res['party']] += 1
    
    for key in wordDic.keys():
        print("The keyword '" + key + "' was mentioned by:")
        print()

        for party in wordDic[key].keys():
            print("    " + party + " -> " + str(wordDic[key][party]) + " times ")
    
        print()

# Main code
###############################################

#Obtain keywords from arg
keyArr = sys.argv[1:]
keywords = ' '.join(keyArr)

ix = index.open_dir("index")

with ix.searcher() as s:
    qp = QueryParser("content", schema=ix.schema)
    q = qp.parse(keywords)
    results = s.search(q, limit=None, groupedby='party', terms=True )
    
    print("Results for -> " + keywords + ":")
    print()

    for i,r in enumerate(results):
        print("    " + r['id'] + "  " + r['title'])
        print()
    

    manifCountPerParty(results.groups())
    
    keywordCountPerParty(keyArr, results)