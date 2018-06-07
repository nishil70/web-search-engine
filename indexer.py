import os
import sys
import pickle
sys.setrecursionlimit(10000)


def create_index(path1):
    # Open all files in current directory
    token_files = [file for file in os.listdir(path1) if file.endswith(".token")]
    inverted_index = {}
    output_path = "D_INDEXED_FILE/"

    for x, y in enumerate(token_files):
        print(str(x) + ": Indexing: " + str(y))
        w_count = 0  # Reset word count
        r_path = os.path.join(path1, y)
        with open(r_path, 'rb') as f:  # Open file for writing
            while True:  # Load each pickle file
                try:
                    content = pickle.load(f)
                except EOFError:
                    break

            for w in content:  # For each word in the list of tokens
                if w in inverted_index.keys():
                    w = inverted_index[w]  # Capture ii entry for existing word
                    w[1] += 1  # increment term frequency
                    if y in w[2].keys():  # File in y word's posting list
                        ld = w[2][y]
                        ld[0].append(w_count)
                        ld[1] += 1
                    else:  # Word is in II, but not posting for y
                        w[2][y] = [[w_count], 1]
                    w[0] = len(w[2])
                else:  # Create inverted index entry for the new word
                    ld = {y: [[w_count], 1]}
                    inverted_index[w] = [1, 1, ld]
                w_count += 1
                # print("printing inverted index: ",inverted_index)

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    pickle.dump(inverted_index, open(output_path + 'index', 'wb'))
    return inverted_index


# '''output_path = r'C:\Users\nishi\PycharmProjects\Tokenization\C_TOKEN_FILES'
# D_INDEXED_FILE = r'C:\Users\nishi\PycharmProjects\Tokenization\D_INDEXED_FILE'
# inverted_index = create_index(output_path)

# print("Printing the inverted index: ", inverted_index)

# '''
