import re
import time
import common


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

    document_index = common.removes_stopWord_and_stemming(documentParser(corpus))
    return document_index


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

    corpusquery = common.readAllFile("query")

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





