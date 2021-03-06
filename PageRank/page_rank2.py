import numpy as np
from scipy.sparse import lil_matrix
from scipy import io
import pickle

def has_converged(old_arr, new_arr, epsilon):
    if len(old_arr) != len (new_arr):
        return False

    for num in range(len(old_arr)):
        diff = abs(old_arr[num] - new_arr[num])
        if diff > epsilon:
            return False

    return True


def calculate_page_ranks(matrix, beta, url_dict, epsilon, max_itr):
    matrix_dim = matrix.shape[0]
    vector = [1/matrix_dim for i in range(matrix_dim)]
    old_vector = [0 for i in range(matrix_dim)]
    itr_count = 0

    while not has_converged(old_vector, vector, epsilon) and itr_count < max_itr:
        old_vector = vector
        mult = np.matmul(matrix, vector)
        vector = mult + (1-beta)/matrix_dim
        itr_count = itr_count + 1
        print('iteration: {}'.format(itr_count))

    url_arr_indexed = [None for i in range (matrix_dim)]

    for url in url_dict:
        url_arr_indexed[url_dict[url]] = url

    url_to_pr = {}
    for i in range(len(vector)):
        url_to_pr[url_arr_indexed[i]] = vector[i]

    return url_to_pr


def get_num_links(link_dict):
    links_seen = set()
    count = 0

    for url in link_dict:
        if url not in links_seen:
            links_seen.add(url)
            count = count + 1

        for outlink in link_dict[url]:
            if outlink not in links_seen:
                links_seen.add(outlink)
                count = count + 1

    return count

def create_pr_matrix(data, beta, url_dict):
    num_urls = get_num_links(data)
    matrix = lil_matrix((num_urls, num_urls))
    url_count = 0

    for url in data.keys():
        row_num = 0
        if url in url_dict:
            row_num = url_dict[url]
        else:
            url_dict[url] = url_count
            row_num = url_count
            url_count = url_count + 1

        if row_num % 100 == 0 :
            print('row: '  + str(row_num))

        num_outlinks = len(data[url])

        matrix_row = [0 for i in range(num_urls)]
        cell_value = 1/num_outlinks
        for outlink in data[url]:
            col_num = 0
            if outlink in url_dict:
                col_num = url_dict[outlink]
            else:
                url_dict[outlink] = url_count
                col_num = url_count
                url_count = url_count + 1

            matrix_row[col_num] = cell_value

        matrix[row_num] = matrix_row

    matrix = np.multiply(matrix, beta)

    return matrix

# with open('parent_to_children_urls_0.pickle', 'rb') as f:
#     data = pickle.load(f)
#
# data = {'a': ['b','c','d'], 'b':['a','d'], 'c':['c'], 'd':['b', 'c']}

def get_page_ranks(data, load_matrix):
    url_dict = {}
    if load_matrix:
        # with open('./pagerank_matrix.pickle', 'rb') as handle:
        matrix = io.mmread('./pagerank_matrix.pickle.mtx')
    else:
        matrix = create_pr_matrix(data, .8, url_dict)
        #write matrix to file
        # with open('./pagerank_matrix.pickle', 'wb') as handle:
        io.mmwrite('./pagerank_matrix.pickle', matrix)

    pr_dict = calculate_page_ranks(matrix, .8, url_dict, .0001, 100)
    return pr_dict


#load data and run page rank
full_parent_to_children_urls_dic = {}
i = 0
while i < 15:
    try:
        with open('../crawl-pr/data/parent_to_children_urls_{}.pickle'.format(i), 'rb') as handle:
            parent_to_children_urls_dic = pickle.load(handle)

        for key in parent_to_children_urls_dic:
            full_parent_to_children_urls_dic[key] = parent_to_children_urls_dic[key]

    except:
        print('nothing found for i: {}'.format(i))
    i += 1

print('total urls found: {}'.format(len(full_parent_to_children_urls_dic)))
results = get_page_ranks(full_parent_to_children_urls_dic, True)

with open('./pagerank.pickle', 'wb') as handle:
    pickle.dump(results, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print('pr file written out')