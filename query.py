import re
import common

def parse_query_with_title(query_corpus):
    '''
    extract each query with respect to the title
    @param query_corpus: string of all queries
    @return: dictionary containing all queries
    '''
def parse_query_with_title_desc(query_corpus):
    '''
    extract each query with respect to the title and description
    @param query_corpus: string of all queries
    @return: dictionary containing all queries
    '''

    queryRegx = '<top>((.|\\n)+?)</top>'
    dividerRegex = '<num>(.+)' # match[o] = num and match[1] the rest

    query = {}

    tmpquery = re.findall(queryRegx, query_corpus)

    if tmpquery:
        for match in tmpquery:
            num = (re.findall(dividerRegex,match[0]))[0]
            if num:
                #to remove punctuationa and markups and numbers
                query[num] = re.sub("\d+","",re.sub("[^\w\s]|_"," ",re.sub("<[^>]*>", "", match[0])))
    else:
        print("No match found.")

    return query


def pre_process_query_corpus(query_corpus):
    '''
    return query index
    @param query_corpus:
    @return:
    '''
    return common.removes_stopWord_and_stemming(parse_query(query_corpus))

