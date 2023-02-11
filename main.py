import document
import common
import query
import time




if __name__ == '__main__':

    print("---> Reading documents")
    start_time = time.time()
    corpus_document = common.readAllFile("src/coll")
    with open("target/corpus_test.txt", "w") as textFile:
            textFile.write(corpus_document)
    print("--- %s seconds ---" % (time.time() - start_time))


    print("---> Pre-processing Document")
    start_time = time.time()
    doc_indexed = document.pre_process_corpus(corpus_document)
    with open("target/doc_index.txt", "w") as textFile2:
        for k,v in doc_indexed.items():
            textFile2.write('\n'+ k+'\n')
            textFile2.write(str(v))
    print("--- %s seconds ---" % (time.time() - start_time))


    print("---> Calculating inverse index")
    start_time = time.time()
    inverse_index_doc = document.inverse_index_document(doc_indexed)
    with open("target/inverse_index.txt", "w") as textFile2:
        for k,v in inverse_index_doc.items():
            textFile2.write('\n'+ k + '\n')
            textFile2.write(str(v))
    print("--- %s seconds ---" % (time.time() - start_time))


    print("---> Calculating Weights")
    start_time = time.time()
    weights = common.calculateWeights(inverse_index_doc)
    with open("target/weights.txt", "w") as textFile2:
        for k,v in weights.items():
            textFile2.write('\n'+ k + '\n')
            textFile2.write(str(v))
    print("--- %s seconds ---" % (time.time() - start_time))


    print("---> Reading Queries ....")
    start_time = time.time()
    corpus_query = common.readAllFile("query")
    print("--- %s seconds ---" % (time.time() - start_time))

    print("---> Pre-processing Queries with Title")
    start_time = time.time()
    query_indexed = query.pre_process_query_corpus_with_title(corpus_query)
    with open("target/query_index.txt", "w") as textFile2:
        for k, v in query_indexed.items():
            textFile2.write('\n' + k + '\n')
            textFile2.write(str(v))
    print("--- %s seconds ---" % (time.time() - start_time))


    print("---> Calculating Inverse Index Queries")
    start_time = time.time()
    inverse_index_query = query.inverse_index_query(query_indexed)
    with open("target/query_inverse_index.txt", "w") as textFile2:
        for k, v in inverse_index_query.items():
            textFile2.write('\n' + k + '\n')
            textFile2.write(str(v))
    print("--- %s seconds ---" % (time.time() - start_time))


    print("---> Calculating Weights for query")
    start_time = time.time()
    weights_query = common.calculateWeights(inverse_index_query)
    with open("target/weights_query.txt", "w") as textFile2:
        for k, v in weights_query.items():
            textFile2.write('\n' + k + '\n')
            textFile2.write(str(v))
    print("--- %s seconds ---" % (time.time() - start_time))





