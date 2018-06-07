import preprocessing
import tokenization
import vectorspacemodel
import pickle
import collections
import os
import math
import operator
from itertools import islice

def take(n, iterable):
    # "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

directory = os.getcwd()
links_path = os.path.join(directory, 'links')

# Getting Index from pickle dump
with open("D_INDEXED_FILE/index", 'rb') as f:
    while True:
        try:
            index = pickle.load(f)
        except EOFError:
            break
inv_index = index

# Getting Document vectors from pickle dump
dv = {}
vec_files = [file for file in os.listdir("D_INDEXED_FILE/vectors/.") if file.endswith("vector")]
# x = index, y = filename
for x, y in enumerate(vec_files):
    #  Open all of the token lists
    with open("D_INDEXED_FILE/vectors/" + y, 'rb') as ff:
        while True:
            try:
                vector = pickle.load(ff)
            except EOFError:
                break
    dv[y] = vector
# By here you will get all document vectors in dv variable

#print("Document vectors are: ", dv)

query = input("Enter the query: ")
query_vector = []


idf,terms = vectorspacemodel.get_idf(inv_index)
od = collections.OrderedDict(sorted(idf.items()))
#print("idf is: ", idf)
#print("terms are: ", terms)

processed_query = preprocessing.parse_query(query.lower())
#print("processed query is: ", processed_query)
tokenized_query = tokenization.query_tokenization(processed_query)
#print("tokenized query is: ", tokenized_query)

# This code makes the query vector and normalizes it
for x,y in enumerate((od.items())):
    for i in tokenized_query.split():
        if i == y[0]:
            #print(y[1])
            if [y[1],x] in query_vector:
                query_vector.remove([y[1], x])
                query_vector.append([y[1]+y[1],x])
            else:
                query_vector.append([y[1],x])

#print("Unnormalized query vector is: ", query_vector)

# Normalizing here
weight = 0.0
for i in range(len(query_vector)):
    weight = weight + (query_vector[i][0] ** 2)
weight = math.sqrt(weight)
# print("weight is: ", weight)
for i in range(len(query_vector)):
    query_vector[i][0] = query_vector[i][0] / weight

#print("the Normalized query vector is: ", query_vector)

# Calculate Similarity between query vector and all document vectors
similarity = {}
for k in dv.keys():
    sim = float(0)
    for i in range(len(query_vector)):
        di = query_vector[i][1]
        #import pdb; pdb.set_trace()
        for j in range(len(dv[k])):
            dj = dv[k][j][1]
            if di == dj:
                mul = query_vector[i][0] * dv[k][j][0]
                sim += mul
                #print (mul)
                break
            elif di < dj:
                break
    similarity[k] = sim
    #print("document vector is: ", dv[k])
    #print("query vector is: ", v1)
    #print ("similarity is: ", sim)
        #print(sim)

#print("cosine similarity is: ", similarity)

sorted_x = sorted(similarity.items(), key=operator.itemgetter(1), reverse=True)
#print("Sorted Cosine Similarity",sorted_x)
top_7 = take(7, sorted_x)
#print("Top 7 documents are: ", top_7)

# Getting the links file to match file with link
with open(links_path, 'rb') as f:
    while True:
        try:
            web_links = pickle.load(f)
        except EOFError:
            break
#print("All the web links are: ", web_links)



#print("Top 10 documents are:\n ", ("\n".join(str(x[0][0:-7]) for x in top_5)).strip())
print("Our Search Results are: ")
for x in top_7:
    #print("".join(str(x[0][0:-7])))
    if x[1] == float(0):
        print("No relevant documents found!")
        break
    else:
        for j in web_links.keys():
            if "".join(str(x[0][0:-7])) == j[0:-5]:
                print(repr(web_links[j]).strip('\''))

# print("Total document vectors are: ", len(dv))
# print("Total unique terms for index are: ", len(inv_index))
# print("Total unique terms from terms are: ", len(terms))
# print("Toal unique terms from idf are: ", len(idf))