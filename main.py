import document
import common
import query
import time
import metric
import json
'''
This class is used to run the experiment and generate Json files according to each step.
'''


def read_document():
    '''
    reads all the documents in the src/coll
    @return: None
    '''
    print("---> Reading documents")
    start_time = time.time()
    corpus_document = common.readAllFile("src/coll")
    with open("target/corpus_test.json", "w") as json_file:
        json.dump(corpus_document, json_file)
    print("--- %s seconds ---" % (time.time() - start_time))


def pre_process_document():
    '''
    pre-process document to use in IR system
    @return: None
    '''
    with open('target/corpus_test.json') as json_file:
        corpus_document = json.load(json_file)
    print("---> Pre-processing Document")
    start_time = time.time()
    doc_indexed = document.pre_process_corpus(corpus_document)
    with open("target/doc_index.json","w") as json_file:
        json.dump(doc_indexed,json_file)
    print("--- %s seconds ---" % (time.time() - start_time))

def calculate_inverse_index_document():
    '''
    calculates inverse index for the documents
    @return: None
    '''
    with open('target/doc_index.json') as json_file:
        doc_indexed = json.load(json_file)
    print("---> Calculating inverse index")
    start_time = time.time()
    inverse_index_doc = document.inverse_index_document(doc_indexed)
    with open("target/inverse_index.json", "w") as json_file:
        json.dump(inverse_index_doc, json_file)
    print("--- %s seconds ---" % (time.time() - start_time))

def calculate_weight_document():
    '''
    calculates weights for document
    @return: None
    '''
    with open('target/inverse_index.json') as json_file:
        inverse_index_doc = json.load(json_file)
    print("---> Calculating Weights")
    start_time = time.time()
    weights = common.calculate_weights(inverse_index_doc)
    with open("target/weights.json", "w") as json_file:
        json.dump(weights, json_file)
    print("--- %s seconds ---" % (time.time() - start_time))

def reading_queries():
    '''
    reading all test queries
    @return: None
    '''
    print("---> Reading Queries ....")
    start_time = time.time()
    corpus_query = common.readAllFile("query")
    with open("target/corpus_query.json", "w") as json_file:
        json.dump(corpus_query, json_file)
    print("--- %s seconds ---" % (time.time() - start_time))

def pre_process_query_title_w_des():
    '''

    pre process of queri with title and its description
    @return: None
    '''
    with open('target/corpus_query.json') as json_file:
        corpus_query = json.load(json_file)
    print("---> Pre-processing Queries with Title and Description")
    start_time = time.time()
    query_indexed_w_des = query.pre_process_query_corpus_with_title_desc(corpus_query)
    with open("target/query_index_w_des.json", "w") as json_file:
        json.dump(query_indexed_w_des, json_file)
    print("--- %s seconds ---" % (time.time() - start_time))

def calculate_query_vector_w_desc():
    '''
    calculates query vestor including description
    @return: None
    '''
    with open('target/query_index_w_des.json') as json_file:
        query_indexed_w_des = json.load(json_file)
    with open('target/inverse_index.json') as json_file:
        inverse_index_doc = json.load(json_file)
    print("---> Calculating query vectors")
    start_time = time.time()
    vectors_w_des = query.query_vectors(inverse_index_doc, query_indexed_w_des)
    with open("target/query_vectors_w_des.json", "w") as json_file:
        json.dump(vectors_w_des, json_file)
    print("--- %s seconds ---" % (time.time() - start_time))

def result_w_des():
    '''
    calculates similarity measures and rank to generate the result  when we include description
    @return: None
    '''
    with open('target/query_vectors_w_des.json') as json_file:
        vectors_w_des = json.load(json_file)
    with open('target/weights.json') as json_file:
        weights = json.load(json_file)
    print("---> Result")
    start_time = time.time()
    with open("target/result_w_des.txt", "w") as textFile2:
        for k, v in vectors_w_des.items():
            ranked_series = metric.ranking(metric.similarity_measure(vectors_w_des[k], weights))
            for doc_no in ranked_series.index.values.tolist():
                textFile2.write(
                    " " + k + " Q0 " + doc_no + " " + str(ranked_series.loc[[doc_no]]['rank'][0]) + " " + str(
                        ranked_series.loc[[doc_no]][0][0]) + " test" + '\n')
    print("--- %s seconds ---" % (time.time() - start_time))

def pre_process_query_title():
    '''
    pre process of queri with title
    @return: None
    '''
    with open('target/corpus_query.json') as json_file:
        corpus_query = json.load(json_file)
    print("---> Pre-processing Queries with Title ")
    start_time = time.time()
    query_indexed = query.pre_process_query_corpus_with_title(corpus_query)
    with open("target/query_index.json", "w") as json_file:
        json.dump(query_indexed, json_file)
    print("--- %s seconds ---" % (time.time() - start_time))

def calculate_query_vector():
    '''
    calculates query vestor
    @return: None
    '''
    with open('target/query_index.json') as json_file:
        query_indexed = json.load(json_file)
    with open('target/inverse_index.json') as json_file:
        inverse_index_doc = json.load(json_file)
    print("---> Calculating query vectors")
    start_time = time.time()
    vectors = query.query_vectors(inverse_index_doc, query_indexed)
    with open("target/query_vectors.json", "w") as json_file:
        json.dump(vectors, json_file)
    print("--- %s seconds ---" % (time.time() - start_time))


def result():
    '''
    calculates similarity measures and rank to generate the result
    @return: None
    '''
    with open('target/query_vectors.json') as json_file:
        vectors = json.load(json_file)
    with open('target/weights.json') as json_file:
        weights = json.load(json_file)
    print("---> Result")
    start_time = time.time()
    with open("target/result.txt", "w") as textFile2:
        for k, v in vectors.items():
            ranked_series = metric.ranking(metric.similarity_measure(vectors[k], weights))
            for doc_no in ranked_series.index.values.tolist():
                textFile2.write(
                    " " + k + " Q0 " + doc_no + " " + str(ranked_series.loc[[doc_no]]['rank'][0]) + " " + str(
                        ranked_series.loc[[doc_no]][0][0]) + " test" + '\n')
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    read_document()
    pre_process_document()
    calculate_inverse_index_document()
    calculate_weight_document()
    reading_queries()
    print("---> TEST WITH TITLE AND DESCRIPTION")
    pre_process_query_title_w_des()
    calculate_query_vector_w_desc()
    result_w_des()
    print("---> TEST WITH TITLE")
    pre_process_query_title()
    calculate_query_vector()
    result()



