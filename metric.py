import pandas as pd
import numpy as np
from scipy.spatial.distance import cosine
import json

'''
    Includes functionality that generate similarity measurements and ranking. 
'''

def similarity_measure(query_vector, doc_weights, is_cosine = True):
    '''
    calculate the distance between the query vector and the document vector
    @param query_vector: a query vector
    @param doc_weights: the weights of each document by term
    @param is_cosine: uses the cosine distance if true, else it uses the dot product
    @return: returns a Pandas Series with the similarity measure for each document given a certain query
    '''
    # transforming the query_vector to a Panda array
    q = pd.Series(query_vector)
    # transforming the weight dictionary into a dataframe
    dt = pd.DataFrame.from_dict({k: doc_weights[k] for k in q.index if k in doc_weights.keys()})
    # If a word in the query does not exist in the corpus
    if q.index.difference(dt.columns).size != 0:
        dt[q.index.difference(dt.columns)] = 0
    # Giving a weight of zero if term is not in document
    dt = dt.fillna(0)
    # applying the chosen similarity function
    if not is_cosine:
        return dt.apply(lambda row: np.dot(row, q.array), axis=1)
    else:
        return dt.apply(lambda row: 1 - cosine(row, q.array), axis=1)



def ranking(similarity_pd):
    '''
    Ranks the documents by similarity to the query
    @param similarity_pd: Pandas Series with the similarity measure for each document given a certain query
    @return: Pandas Series with sorted documents by similarity to the query
    '''
    sim = similarity_pd.to_frame()
    sim['rank'] = similarity_pd.rank(ascending=False, method='first')
    return sim.sort_values( by=['rank'])







