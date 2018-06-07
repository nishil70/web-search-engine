# For tokenizing the input files
import os
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords, wordnet
from nltk import pos_tag
from nltk.tokenize import sent_tokenize, word_tokenize
import pickle

def get_word_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    if tag.startswith('V'):
        return wordnet.VERB
    if tag.startswith('N'):
        return wordnet.NOUN
    if tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''


# Tokenize the file "TOKEN"

def tokenize_files(path):
    filenames = [file for file in os.listdir(path + ".")]
    lemmatizer = WordNetLemmatizer()
    ps = PorterStemmer()
    output_pathname = "C_TOKEN_FILES/"

    for x, y in enumerate(filenames):
        doc = []
        with open(os.path.join(path, y), 'rb') as f:
            filename = y[:-4] + ".token"
            print(str(x) + ": Tokenizing: " + str(y) + " -> " + filename)

            sentence = sent_tokenize(f.read().decode("utf-8"))
            for s1 in sentence:
                token1 = word_tokenize(s1)
                words = [w.lower() for w in token1 if w.isalpha() or w.isalnum()]

                # stop list
                stop_words = set(stopwords.words('english'))
                filtered = [w for w in words if not w in stop_words]
                tag_tokens = pos_tag(filtered)

                # Lemmatization  and Stemming

                for i in range(0, len(filtered)):
                    if get_word_pos(tag_tokens[i][1]):
                        w = lemmatizer.lemmatize(filtered[i], get_word_pos(tag_tokens[i][1]))
                        w = ps.stem(w)
                    else:
                        w = ps.stem(filtered[i])
                    doc.append(w)

            if not os.path.exists(output_pathname):
                os.makedirs(output_pathname)
            # print (doc)
            pickle.dump(doc, open(output_pathname + filename, 'wb'))


# For testing tokenization seperately
# tokenize('1.TXT/')
# '''
# input_path = r'C:\Users\nishi\PycharmProjects\Tokenization\Input Files'
# tokenize(input_path)
# '''


# Function for tokenizing the search query
def query_tokenization(query):
    lemmatization = WordNetLemmatizer()
    stem = PorterStemmer()
    sentence = sent_tokenize(query)
    query_token = ""
    for s2 in sentence:
        token2 = word_tokenize(s2)
        words = [w.lower() for w in token2 if w.isalpha() or w.isalnum()]

        # stop list
        stop_words = set(stopwords.words('english'))
        filtered = [w for w in words if not w in stop_words]
        tag_tokens = pos_tag(filtered)

        # Lemmatization and Stemming

        for a in range(0, len(filtered)):
            if get_word_pos(tag_tokens[a][1]):
                w = lemmatization.lemmatize(filtered[a], get_word_pos(tag_tokens[a][1]))
                w = stem.stem(w)
            else:
                w = stem.stem(filtered[a])
            query_token = query_token + ' ' + w
    return query_token


