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


def inverse_index_query(document_inverted_index,query_index):
    '''
    calculate a matrix containing all tf-idf s for all given queries
    @param document_index:
    @return: dictionary with f values
    '''

    #make dictionary of all words and their occurance over the corpus vocab = {word:{ df: # , docf: { docno: tf}}}
    vocab = {}
    for k,v in query_index.items(): # iterate through all documents
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
            vocab[word]['idf'] = document_inverted_index[word]['idf']

    return vocab


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

