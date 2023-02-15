import re
import time
import common
'''
    Consists of methods to parse document, generate indexed documents. 
'''

def documentParser(corpus):
    '''

    parse string documents into a dictionary containing
    @param corpus: string value of all documents
    @return: return dictionary that key is the document number and value is the rest of document : {key= document no. : value= document content}
    '''

    docRegx = '<DOC>((.|\\n)+?)</DOC>'
    dividerRegex = '<DOCNO>(.+?)</DOCNO>(.+)'

    document_dict = {}

    tmpdoc = re.findall(docRegx, corpus)

    if tmpdoc:
        for match in tmpdoc: # for each match for each document
            docList = re.findall(dividerRegex, match[0], flags=re.DOTALL)
            if docList:
                #to remove punctuationa and markups and numbers
                document_dict[docList[0][0]] = re.sub("\d+","",re.sub("[^\w\s]|_"," ",re.sub("<[^>]*>", "",docList[0][1])))

    else:
        print("No match found.")

    return document_dict

def inverse_index_document(document_index):
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
    inverse_index = common.df_to_idf(vocab, document_index)

    return inverse_index

def pre_process_corpus(corpus):
    '''
    receive string containing all the documents in form of string and returns indexed document(parse + stemming + removing stopwords)
    @param corpus: string of all documents
    @return:dictionary of documents with {key=document number , value= tokens of document without stop words and stemmed}
    '''

    document_index = common.removes_stopWord_and_stemming(documentParser(corpus))
    return document_index
