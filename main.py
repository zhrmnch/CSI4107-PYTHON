import document
import common
import query
import time
import metric




if __name__ == '__main__':

    print("---> Reading documents")
    start_time = time.time()
    corpus_document = common.readAllFile("test/")
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
    weights = common.calculate_weights(inverse_index_doc)
    with open("target/weights.txt", "w") as textFile2:
        for k,v in weights.items():
            textFile2.write('\n'+ k + '\n')
            textFile2.write(str(v))
    print("--- %s seconds ---" % (time.time() - start_time))


    print("---> Reading Queries ....")
    start_time = time.time()
    corpus_query = common.readAllFile("query")
    print("--- %s seconds ---" % (time.time() - start_time))


    print("---> Pre-processing Queries with Title and Description")
    start_time = time.time()
    query_indexed = query.pre_process_query_corpus_with_title_desc(corpus_query)
    with open("target/query_index.txt", "w") as textFile2:
        for k, v in query_indexed.items():
            textFile2.write('\n' + k + '\n')
            textFile2.write(str(v))
    print("--- %s seconds ---" % (time.time() - start_time))


    print("---> Calculating query vectors")
    start_time = time.time()
    vectors = query.query_vectors(inverse_index_doc, query_indexed)
    with open("target/query_vectors.txt", "w") as textFile2:
        for k, v in vectors.items():
            textFile2.write('\n' + k + '\n')
            textFile2.write(str(v))
    print("--- %s seconds ---" % (time.time() - start_time))


    print("---> Result")
    start_time = time.time()
    with open("target/Result.txt", "w") as textFile2:
        for k, v in vectors.items():
            ranked_series = metric.ranking(metric.similarity_measure(vectors[k], weights))
            for doc_no in ranked_series.index.values.tolist():
                textFile2.write(" "+ k + " Q0 "+doc_no+" "+str(ranked_series.loc[[doc_no]]['rank'][0])+ " " + str(ranked_series.loc[[doc_no]][0][0]) +" test"+'\n')
    print("--- %s seconds ---" % (time.time() - start_time))








