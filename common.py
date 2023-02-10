from pathlib import Path
from nltk.tokenize import word_tokenize
from nltk.stem import *
from math import log



def readAllFile(path):
    '''
    Reads all the files in the given path

    This function is inspired by the following stackoverflow thread:
    https://stackoverflow.com/questions/26695903/python-how-to-read-all-files-in-a-directory

    @return: String value of all read files

    '''

    fileToString = ''

    #iterate in all the paths
    for child in Path(path).iterdir():
        if child.is_file():
            fileToString += child.read_text()

    return fileToString


def retrievingStopwords():
    '''
    Reads a file containing all stopwords and make a set of it

    @param: stopwordArray: array of words containing stop words (the files are taken from instructions)
    @return: a list containing all stopwords
    '''
    stopwordArray= {}
    with open('src\stopwords.txt') as myFile:
        for line in myFile:
            stopwordArray[line.split()[0]] = None
    return stopwordArray

def removes_stopWord_and_stemming(document_dict):
    '''
    Removes stopwords in the values of the dictionary, we are updating the original dictionary then stems the words

    @param: corpusToken: all tokens in the given corpus
    @param: stopwordsToken: list of all stop words
    @param: tokensWithoutStopwords: all tokens in the given corpus excluding the stopwords

    @return: string without stopwords and tags
    '''

    stopwordsToken = set(retrievingStopwords().keys())

    stemmer = PorterStemmer()
    document_with_tokens ={}

    for k,v in document_dict.items():
        document_with_tokens[k] = word_tokenize(v)
        document_with_tokens[k] = [stemmer.stem(i) for i in document_with_tokens[k]]
        document_with_tokens[k] = [word for word in document_with_tokens[k] if word not in stopwordsToken]
    return document_with_tokens

def df_to_idf(vocab, document_index):
    '''
    Transforms the dictionary conitaining df and calculate idf and update the dictionary with its value
    @param vocab: The inverse index
    @param document_index: The document index
    @return:
    '''

    for word in vocab.keys():
        vocab[word]['idf'] = log(len(document_index)/vocab[word]['df'], 2)
    return vocab

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



