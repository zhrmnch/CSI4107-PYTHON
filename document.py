import nltk
from pathlib import Path
import re
from nltk.tokenize import word_tokenize
from nltk.stem import *

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

def removeStopWord(dict):
    '''
    Removes stopwords in the values of the dictionary, we are updating the original dictionary

    @param: corpusToken: all tokens in the given corpus
    @param: stopwordsToken: list of all stop words
    @param: tokensWithoutStopwords: all tokens in the given corpus excluding the stopwords

    @return: string without stopwords and tags 
    '''

    stopwordsToken = retrievingStopwords()

    stemmer = PorterStemmer()

    for k,v in dict.items():
        dict[k] = word_tokenize(v)
        dict[k] = [stemmer.stem(i) for i in dict[k]]
        dict[k] = [word for word in dict[k] if not word in stopwordsToken]


def documentParser(corpus):
    '''

    @param corpus: string value of all documents
    @return: return dictionary that key is the document number and value is the rest of document
    '''
    docRegx = '<DOC>((.|\\n)+?)</DOC>'
    dividerRegex = '<DOCNO>(.+?)</DOCNO>(.+)'

    dict = {}

    tmpdoc = re.findall(docRegx, corpus)

    if tmpdoc:
        for match in tmpdoc:
            docList = re.findall(dividerRegex, match[0], flags=re.DOTALL)
            if docList:
                #to remove punctuationa and markups and numbers
                dict[docList[0][0]] = re.sub("\d+","",re.sub("[^\w\s]|_"," ",re.sub("<[^>]*>", "",docList[0][1])))

    else:
        print("No match found.")

    return dict

def calculateF(dict):
    '''
    calculate the f value ; frequency of term i in document j
    @param dict:
    @return: dictiory with f values
    '''


    #make dictionary of all words and their occurance over the corpus vocab = {word:{ df: # , docf: { docno: tf}}}
    vocab = {}
    for k,v in dict.items():
        max = 0
        for word in v:
            if not word in vocab.keys():
                vocab[word] = {'docf':{}}
                vocab[word]['df'] = 1
                vocab[word]['docf'][k] = 1
            else:
                vocab[word]['df'] += 1
                if k not in vocab[word]['docf'].keys():
                    vocab[word]['docf'][k] = 1
                else:
                    vocab[word]['docf'][k] += 1
            if vocab[word]['docf'][k] > max:
                max = vocab[word]['docf'][k]
        for word in vocab.keys():
            if k in vocab[word]['docf'].keys():
                vocab[word]['docf'][k] = vocab[word]['docf'][k] / max
    #TODO df to idf

if __name__ == '__main__':


    corpusDocument = readAllFile("test")
    with open("corpustest.txt", "w") as textFile:
            textFile.write(corpusDocument)
    
    '''
    corpusDocumentTmp =""

    with open('test.txt') as myFile:
        for line in myFile:
            corpusDocumentTmp += line
'''

    vocabulary = documentParser(corpusDocument)
    with open("bow.txt", "w") as textFile2:
        for item in vocabulary:
            textFile2.write(item+'\n')




