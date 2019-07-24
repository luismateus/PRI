import os, os.path, csv
import pandas as pd
import json
import whoosh.index as index
from whoosh.index import create_in
from whoosh.fields import *
import nltk
from nltk.tree import Tree

def getNamedEntities(cont_chunk, input):
    chunk = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(input)))
    cur_chunk = []

    for i in chunk:
        if type(i) == Tree:
            cur_chunk.append(" ".join([token for token, pos in i.leaves()]))
        elif cur_chunk:
            named_entity = " ".join(cur_chunk)
            if named_entity not in cont_chunk:
                cont_chunk[named_entity] = 1
                cur_chunk = []
            else:
                cont_chunk[named_entity] += 1
        else:
            continue
    return cont_chunk

# Main code
##################################################
csv.field_size_limit(sys.maxsize)

#Create the schema to store the manifestos
schema = Schema(content=TEXT(stored=True), 
                id=ID(stored=True), 
                party=ID(stored=True),
                date=DATETIME(stored=True), 
                title=TEXT(stored=True))

#Create directory to store index
if not os.path.exists("index"):
    os.mkdir("index")

ix = create_in("index", schema)
ix = index.open_dir("index")

writer = ix.writer()

#Dictionary with { id: content}
dicCont = {}
#Dictionary with { id: (party, date, title) }
dicFields = {}

arrayData = []


with open('en_docs_clean.csv',encoding = 'utf-8') as csv_file:
    
    reader = csv.reader(csv_file, delimiter= ',', quotechar='"')

    for n, row in enumerate(reader):

        #Ignore first row
        if n:
            #Group content if same id was read
            if row[1] in dicCont.keys():
                dicCont[row[1]] += row[0]

            #Create new manifesto
            else:
                dicCont[row[1]] = row[0]
                dicFields[row[1]] = (row[2], row[3], row[4])

    for k in dicCont.keys():
        fields = dicFields.get(k)

        #Add all manifestos to the index
        arrayData.append([dicCont.get(k),k,fields[0],fields[1],fields[2]]) #for exercice 3 (possible 2)
        writer.add_document(content = dicCont.get(k),
                            id = k,
                            party = fields[0],
                            date = fields[1],
                            title = fields[2]
                            )
writer.commit()

partyGrouping = dict()
if not os.path.exists("indexed_entities"):
    for i in range(0, len(arrayData)):
        if arrayData[i][2] not in partyGrouping:
            partyGrouping[arrayData[i][2]] = dict()
        print('running %d out of %d times' % (i+1, len(arrayData)))
        print('analysing %s' % arrayData[i][2])
        getNamedEntities(partyGrouping[arrayData[i][2]], arrayData[i][0])
    with open("indexed_entities", "w") as write_file:
        json.dump(partyGrouping, write_file)
else:
    with open("indexed_entities", "r") as read_file:
        partyGrouping = json.load(read_file)
