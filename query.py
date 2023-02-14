import re
import common

def parse_query_with_title(query_corpus):
    '''
    extract each query with respect to the title
    @param query_corpus: string of all queries
    @return: dictionary containing all queries
    '''
    extract_query_regx = '<top>(.+?)</top>'
    extract_content_regex = '<num>(.+?)<title>(.+?)<desc>'

    all_queries = re.findall(extract_query_regx, query_corpus, flags=re.DOTALL)
    queries ={}
    if all_queries:
        for query in all_queries:
            q = re.findall(extract_content_regex, query, flags=re.DOTALL)
            num = re.sub("\n", "", q[0][0])
            queries[num] = re.sub("\d+", "", re.sub("[^\w\s]|_", " ", re.sub("<[^>]*>", "", q[0][1])))
    else:
        print("No match found.")
    return queries



def parse_query_with_title_desc(query_corpus):
    '''
    extract each query with respect to the title and description
    @param query_corpus: string of all queries
    @return: dictionary containing all queries
    '''

    extract_query_regx = '<top>(.+?)</top>'
    extract_content_regex = '<num>(.+?)<title>(.+?)<narr>'

    queries = {}

    all_queries = re.findall(extract_query_regx, query_corpus, flags=re.DOTALL)

    if all_queries:
        for query in all_queries:
            q = re.findall(extract_content_regex, query, flags = re.DOTALL)
            num = re.sub("\n","",q[0][0])
            #to remove punctuationa and markups and numbers
            queries[num] = re.sub("\d+","",re.sub("[^\w\s]|_"," ",re.sub("<[^>]*>", "", q[0][1])))

    else:
        print("No match found.")

    return queries



def pre_process_query_corpus_with_title_desc(query_corpus):
    '''
    return query index
    @param query_corpus:
    @return:
    '''
    return common.removes_stopWord_and_stemming(parse_query_with_title_desc(query_corpus))

def pre_process_query_corpus_with_title(query_corpus):
    '''
    return query index
    @param query_corpus:
    @return:
    '''
    return common.removes_stopWord_and_stemming(parse_query_with_title(query_corpus))


def query_vectors(inverse_index_doc, query_index):
    '''
    calculate a matrix containing all tf-idf of the terms in all given queries
    @param inverse_index_doc: the inversed index of the documents corpus
    @param query_index: the query index
    @return: dictionary with f values
    '''

    #make dictionary of all words and their occurance over the corpus vectors = {num:{ word: weight}}
    vectors = {}
    for k,v in query_index.items(): # iterate through all queries
        max = 0
        vectors[k] ={}
        for word in v:
            # Case where the word does not exist in the vocabulary
            if word not in vectors[k].keys():
                # adding the word
                vectors[k][word] = 1
            else:
                # incrementing the word frequency
                vectors[k][word] += 1
            if vectors[k][word] > max:
                max = vectors[k][word]
        for word in vectors[k].keys():
            # normalizing the frequencies
            if word in inverse_index_doc:
                # weighting the terms wiq = (0.5 + 0.5 tfiq)∙idfi
                vectors[k][word] = inverse_index_doc[word]['idf'] * (0.5 + 0.5 * vectors[k][word] / max)
            else:
                # Gives a weight of zero to words that do not appear in the corpus
                vectors[k][word] = 0
    return vectors

