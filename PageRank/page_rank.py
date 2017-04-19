import numpy as np
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
    matrix_dim = len(matrix)
    vector = [1/matrix_dim for i in range(matrix_dim)]
    old_vector = [0 for i in range(matrix_dim)]
    itr_count = 0

    while not has_converged(old_vector, vector, epsilon) and itr_count < max_itr:
        old_vector = vector
        mult = np.matmul(matrix, vector)
        vector = mult + (1-beta)/matrix_dim
        itr_count = itr_count + 1

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
    matrix = np.zeros([num_urls, num_urls])
    url_count = 0

    for url in data.keys():
        row_num = 0
        if url in url_dict:
            row_num = url_dict[url]
        else:
            url_dict[url] = url_count
            row_num = url_count
            url_count = url_count + 1

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

    matrix = np.multiply(matrix, (beta))

    return np.rot90(np.fliplr(matrix))

with open('parent_to_children_urls_0.pickle', 'rb') as f:
    data = pickle.load(f)

data = {'a': ['b','c','d'], 'b':['a','d'], 'c':['c'], 'd':['b', 'c']}

url_dict = {}
matrix = create_pr_matrix(data, .8, url_dict)
pr_dict = calculate_page_ranks(matrix, .8, url_dict, .0001, 100)
print(pr_dict)