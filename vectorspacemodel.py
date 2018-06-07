import math
import os
import pickle
import sys
sys.setrecursionlimit(10000)


# Get Index into the memory
def load_index():
    with open("D_INDEXED_FILE/index", 'rb') as f:
        while True:
            try:
                index = pickle.load(f)
            except EOFError:
                break
    return index


# Get Idf of all terms
def get_idf(index):
    token_files = [file for file in os.listdir("C_TOKEN_FILES/.") if file.endswith(".token")]
    # Count of Docs
    N = len(token_files)
    idf = {}
    for i, j in index.items():
        # using Standard IDF formula log(N/df)
        idf[i] = math.log10(N / j[0])

    # Get sorted dictionary here
    unique_sorted_terms = list(index.keys())
    unique_sorted_terms = sorted(unique_sorted_terms)

    return idf, unique_sorted_terms


# Create document vectors for each tokenized file
def get_document_vectors(index, idf, terms):
    token_files = [file for file in os.listdir("C_TOKEN_FILES/.") if file.endswith(".token")]
    document_vector = {}

    # x = index, y = filename
    for x, y in enumerate(token_files):
        filename = y[:-5] + "vector"
        print(str(x) + ": Weighing: " + str(y) + " -> " + filename)
        with open("C_TOKEN_FILES/" + y, 'rb') as f:  # Open all of the token lists
            while True:
                try:
                    pickle_vector = pickle.load(f)
                except EOFError:
                    break

        # Vectors will only have non-zero entries
        vectors = []
        for i, j in enumerate(terms):
            if j in pickle_vector:
                tf = index[j][2][y][1]
                if tf is not None:
                    vectors.append([tf * idf[j], i])
        # print("vector is: ", vectors)

        # ---------- Normalize the vector ---------------------------
        weight = 0.0
        for i in range(len(vectors)):
            weight = weight + (vectors[i][0] ** 2)
        weight = math.sqrt(weight)
        # print("weight is: ", weight)
        for i in range(len(vectors)):
            vectors[i][0] = vectors[i][0] / weight
        # print("Normalized vector is: ", vectors)
        document_vector[y] = vectors
        # Create a pickle file for document vector
        if not os.path.exists('D_INDEXED_FILE/vectors/'):
            os.makedirs('D_INDEXED_FILE/vectors/')
        pickle.dump(vectors, open('D_INDEXED_FILE/vectors/' + filename, 'wb'))
    return document_vector

