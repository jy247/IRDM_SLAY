import numpy as np
import pickle


def calculate_page_ranks(matrix, beta):
    matrix_dim = len(matrix)
    vector = [1/matrix_dim for i in range(matrix_dim)]

    for i in range(10):
        mult = np.matmul(matrix, vector)
        vector = mult + (1-beta)/matrix_dim

    print(vector)


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

def create_pr_matrix(data, beta):
    num_urls = get_num_links(data)
    matrix = np.zeros([num_urls, num_urls])
    rows_in_matrix = set([])
    url_dict = {}
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

#data = {'a': ['b','c','d'], 'b':['a','d'], 'c':['c'], 'd':['b', 'c']}

matrix = create_pr_matrix(data, .8)
calculate_page_ranks(matrix, .8)