import numpy as np
import pickle
with open('parent_to_children_urls_0.pickle', 'rb') as f:
    data = pickle.load(f)

data = [['a', ['b', 'c', 'd']], ['b', ['a', 'd']], ['c', ['c']], ['d', ['b', 'c']]]
num_urls = len(data)
matrix = np.zeros([num_urls, num_urls])
rows_in_matrix = set([])
url_dict = {}
url_count = 0


for row in range(len(data)):
    url = data[row][0]

    # Account for duplicates
    if url in rows_in_matrix:
        continue

    row_num = 0
    if url in url_dict:
        row_num = url_dict[url]
    else:
        url_dict[url] = url_count
        row_num = url_count
        url_count = url_count + 1

    num_outlinks = len(data[row][1])

    matrix_row = [0 for i in range(num_urls)]
    cell_value = 1/num_outlinks
    for num in range(num_outlinks):
        url_outlink = data[row][1][num]
        col_num = 0
        if url_outlink in url_dict:
            col_num = url_dict[url_outlink]
        else:
            url_dict[url_outlink] = url_count
            col_num = url_count
            url_count = url_count + 1

        matrix_row[col_num] = cell_value

    matrix[row_num] = matrix_row


print(matrix)

