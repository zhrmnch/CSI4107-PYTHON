import pandas as pd
import numpy as np
from scipy.spatial.distance import cosine

def similarity_measure(query_vector, doc_weights, is_cosine = True):
    '''
    calculate the distance between the query vector and the document vector
    @param query_vector: a query vector
    @param doc_weights: the weights of each document by term
    @param is_cosine: uses the cosine distance if true, else it uses the dot product
    @return: returns a Pandas Series with the similarity measure for each document given a certain query
    '''
    # transforming the weight dictionary into a dataframe
    dt = pd.DataFrame(doc_weights)
    # transforming the query_vector to a Panda array
    q = pd.Series(query_vector)
    q = q[q != 0]
    # taking the subset of the vocabulary with query terms
    dt = dt[q.index.intersection(dt.columns)]

    if q.index.difference(dt.columns).size != 0:
        dt[q.index.difference(dt.columns)] = 0
    # dropping irrelevant document
    dt = dt.dropna(how = 'all')
    # Giving a wight of zero if term id not in document
    dt = dt.fillna(0)
    # applying the chosen similarity function
    if not is_cosine:
        return dt.apply(lambda row: np.dot(row, q.array), axis=1)
    else:
        return dt.apply(lambda row: 1-cosine(row, q.array), axis=1)



def ranking(similarity_pd):
    '''
    Ranks the documents by similarity to the query
    @param similarity_pd: Pandas Series with the similarity measure for each document given a certain query
    @return: Pandas Series with sorted documents by similarity to the query
    '''
    sim = similarity_pd.to_frame()
    sim['rank'] = similarity_pd.rank(ascending=False, method='first')
    return sim.sort_values( by=['rank'])







