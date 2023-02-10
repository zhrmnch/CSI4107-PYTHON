import nltk
from pathlib import Path
import re
from  math import log
from nltk.tokenize import word_tokenize
from nltk.stem import *
import time


def readAllFile(path):
    '''
    Reads all the files

    This function is inspired by the following stackoverflow thread:
    https://stackoverflow.com/questions/26695903/python-how-to-read-all-files-in-a-directory

    @return: return all files as string

    '''

    fileToString = ''

    for child in Path(path).iterdir():
        if child.is_file():
            fileToString += child.read_text()

    return fileToString

def retrievingStopwords():
    '''
    Reads file and make a list of stopwords

    @param: stopwordArray: array of words containing stop words - took from instructions

    @return: list of stopwords
    '''
    stopwordArray= []
    with open('src\stopwords.txt') as myFile:
        for line in myFile:
            stopwordArray.append((line.split())[0])
    return stopwordArray

def removes_stopWord_and_stemming(document_index):
    '''
    Removes stopwords in the values of the dictionary, we are updating the original dictionary then stems the words

    @param: corpusToken: all tokens in the given corpus
    @param: stopwordsToken: list of all stop words
    @param: tokensWithoutStopwords: all tokens in the given corpus excluding the stopwords

    @return: string without stopwords and tags 
    '''

    stopwordsToken = retrievingStopwords()

    stemmer = PorterStemmer()

    for k,v in document_index.items():
        document_index[k] = word_tokenize(v)
        document_index[k] = [stemmer.stem(i) for i in document_index[k]]
        document_index[k] = [word for word in document_index[k] if not word in stopwordsToken]
    return document_index


def documentParser(corpus):
    '''

    @param corpus: string value of all documents
    @return: return dictionary that key is the document number and value is the rest of document
    '''
    docRegx = '<DOC>((.|\\n)+?)</DOC>'
    dividerRegex = '<DOCNO>(.+?)</DOCNO>(.+)'

    document_index = {}

    tmpdoc = re.findall(docRegx, corpus)

    if tmpdoc:
        for match in tmpdoc:
            docList = re.findall(dividerRegex, match[0], flags=re.DOTALL)
            if docList:
                #to remove punctuationa and markups and numbers
                document_index[docList[0][0]] = re.sub("\d+","",re.sub("[^\w\s]|_"," ",re.sub("<[^>]*>", "",docList[0][1])))

    else:
        print("No match found.")

    return document_index

def pre_process_corpus(corpus):
    '''
    returns document index
    @param corpus:
    @return:
    '''

    document_index = removes_stopWord_and_stemming(documentParser(corpus))
    return document_index


def df_to_idf(vocab, document_index):
    '''
    Transforms the df into the idf for each word of the vocabulary
    @param vocab: The inverse index
    @param document_index: The document index
    @return:
    '''

    for word in vocab.keys():
        vocab[word]['idf'] = log(len(document_index)/vocab[word]['df'], 2)
    return vocab

def calculateWeights(inverse_index):
    '''
       Calculates the weight of each word in each document
       @param inverse_index:
       @return:
    '''

    weights = {}
    for k, v in inverse_index.items():  # v is { df: # , idf: #,  docf: { docno: tf}}
        weights[k] = {}
        for docno in v['docf'].keys():
            weights[k][docno] = inverse_index[k]['idf'] * inverse_index[k]['docf'][docno]
    return weights

def inverseIndex(document_index):
    '''
    calculate a matrix containing all the inverse indeces
    @param document_index:
    @return: dictiory with f values
    '''


    #make dictionary of all words and their occurance over the corpus vocab = {word:{ df: # , docf: { docno: tf}}}
    vocab = {}
    for k,v in document_index.items(): # iterate through all documents
        max = 0
        for word in v:
            # Case where the word does not exist in the vocabulary
            if not word in vocab.keys():
                #adding the word to the vocabulary and document number - update the df
                vocab[word] = {'docf':{}}
                vocab[word]['df'] = 1
                vocab[word]['docf'][k] = 1
            else:
                # Case where we add a document where the word exists for the first time
                if k not in vocab[word]['docf'].keys():
                    vocab[word]['docf'][k] = 1
                    vocab[word]['df'] += 1
                # Case if the word appears multiple time in the document
                else:
                    vocab[word]['docf'][k] += 1
            # Finding the word with highest frequency for each document
            if vocab[word]['docf'][k] > max:
                max = vocab[word]['docf'][k]
        for word in vocab.keys():
            if k in vocab[word]['docf'].keys():
                vocab[word]['docf'][k] = vocab[word]['docf'][k] / max
    inverse_index = df_to_idf(vocab, document_index)

    return inverse_index

def parse_query(query_corpus):
    '''
    return the query
    @param query_corpus:
    @return:
    '''

    queryRegx = '<top>((.|\\n)+?)</top>'
    dividerRegex = '<num>(.+)' # match[o] = num and match[1] the rest

    query = {}

    tmpquery = re.findall(queryRegx, query_corpus)

    if tmpquery:
        for match in tmpquery:
            num = (re.findall(dividerRegex,match[0]))[0]
            if num:
                #to remove punctuationa and markups and numbers
                query[num] = re.sub("\d+","",re.sub("[^\w\s]|_"," ",re.sub("<[^>]*>", "", match[0])))
    else:
        print("No match found.")

    return query


def pre_process_query_corpus(query_corpus):
    '''
    return query index
    @param query_corpus:
    @return:
    '''
    return removes_stopWord_and_stemming(parse_query(query_corpus))



if __name__ == '__main__':
    '''

    start_time = time.time()
    print("Reading documents ....")

    corpusDocument = readAllFile("test")
    with open("corpustest.txt", "w") as textFile:
            textFile.write(corpusDocument)

    print("--- %s seconds ---" % (time.time() - start_time))


    print("Index all documents ....")
    start_time = time.time()
    doc_indexed = pre_process_corpus(corpusDocument)
    with open("docIndex.txt", "w") as textFile2:
        for k,v in doc_indexed.items():
            textFile2.write('\n'+ k+'\n')
            textFile2.write(str(v))

    print("--- %s seconds ---" % (time.time() - start_time))


    print("Calculating inverse index ....")
    start_time = time.time()
    inverse_index = inverseIndex(doc_indexed)
    with open("inverseindex.txt", "w") as textFile2:
        for k,v in inverse_index.items():
            textFile2.write('\n'+ k + '\n')
            textFile2.write(str(v))

    print("--- %s seconds ---" % (time.time() - start_time))

    print("Calculating Weights ....")
    start_time = time.time()
    weights = calculateWeights(inverse_index)
    with open("weights.txt", "w") as textFile2:
        for k,v in weights.items():
            textFile2.write('\n'+ k + '\n')
            textFile2.write(str(v))
    print("--- %s seconds ---" % (time.time() - start_time))
'''
    start_time = time.time()
    print("Reading queries ....")

    corpusquery = readAllFile("query")

    print("--- %s seconds ---" % (time.time() - start_time))

    print("Index all queries ....")
    start_time = time.time()
    quey_indexed = pre_process_query_corpus(corpusquery)
    with open("queryIndex.txt", "w") as textFile2:
        for k, v in quey_indexed.items():
            textFile2.write('\n' + k + '\n')
            textFile2.write(str(v))

    print("--- %s seconds ---" % (time.time() - start_time))

    print("Calculating inverse index for query....")
    start_time = time.time()
    inverse_index_query = inverseIndex(quey_indexed)
    with open("inverseindexquery.txt", "w") as textFile2:
        for k, v in inverse_index_query.items():
            textFile2.write('\n' + k + '\n')
            textFile2.write(str(v))

    print("--- %s seconds ---" % (time.time() - start_time))

    print("Calculating Weights for query ....")
    start_time = time.time()
    weightsquery = calculateWeights(inverse_index_query)
    with open("weightsquery.txt", "w") as textFile2:
        for k, v in weightsquery.items():
            textFile2.write('\n' + k + '\n')
            textFile2.write(str(v))
    print("--- %s seconds ---" % (time.time() - start_time))





