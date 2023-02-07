import nltk
from pathlib import Path
import re
from nltk.tokenize import word_tokenize

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

def removeStopWord(corpus):
    '''
    Removes stopwords within corpus and html tags

    @param: corpusToken: all tokens in the given corpus
    @param: stopwordsToken: list of all stop words
    @param: tokensWithoutStopwords: all tokens in the given corpus excluding the stopwords

    @return: string without stopwords and tags 
    '''

    corpusToken = word_tokenize(corpus)
    stopwordsToken=  retrievingStopwords()
    tokensWithoutStopwords = [word for word in corpusToken if not word in stopwordsToken]
    return tokensWithoutStopwords


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
                #to remove punctuationa and markups
                #TODO re-think about numbers
                dict[docList[0][0]] = re.sub("[^\w\s]"," ",re.sub("<[^>]*>", "",docList[0][1]))

    else:
        print("No match found.")


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

    vocabulary = parseDocumentCorpus(corpusDocument)
    with open("bow.txt", "w") as textFile2:
        for item in vocabulary:
            textFile2.write(item+'\n')
    