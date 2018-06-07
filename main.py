import sys
import pickle
import preprocessing
import tokenization
import indexer
import vectorspacemodel

sys.setrecursionlimit(10000)

preprocessing.preprocess_html("A_HTML_FILES/")

#input_path = r'C:\Users\nishi\PycharmProjects\Tokenization\1.TXT'
tokenization.tokenize_files("B_TEXT_FILES/")

inv_index = indexer.create_index('C_TOKEN_FILES/')
pickle.dump(inv_index,open('D_INDEXED_FILE/index','wb'))

idf,terms = vectorspacemodel.get_idf(inv_index)
dv = vectorspacemodel.get_document_vectors(inv_index, idf, terms)
