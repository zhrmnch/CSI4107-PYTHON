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
    Reads a file containing all stopwords and make a dictionary of stopwords {stopword: None}
    used dictionary for speed

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




def calculate_weights(inverse_index):
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

