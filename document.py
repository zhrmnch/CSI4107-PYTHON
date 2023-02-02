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


def parseDocumentCorpus(corpus):
    '''

    '''
    tagRegex = '<head>(.+?)</head>|<text>((.|\\n)+?)</text>'
    corpusWithDuplicates = []

    headTextCorpusMatch = re.findall(tagRegex,corpus)

    if headTextCorpusMatch:
        for match in headTextCorpusMatch:
            for submatch in match:
                corpusWithDuplicates = corpusWithDuplicates + removeStopWord(submatch)

        vocabulary = set(corpusWithDuplicates) 
        return vocabulary

    else:
        print("No match found.")


if __name__ == '__main__':

    '''

    corpusDocument = readAllFile("src\coll")
    with open("corpus.txt", "w") as textFile:
            textFile.write(corpusDocument)
    
    '''
    corpusDocumentTmp =""

    with open('test.txt') as myFile:
        for line in myFile:
            corpusDocumentTmp += line


    vocabulary = parseDocumentCorpus(str.lower(corpusDocumentTmp))
    with open("bow.txt", "w") as textFile2:
        for item in vocabulary:
            textFile2.write(item+'\n')
    