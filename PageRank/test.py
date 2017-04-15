import numpy as np

a = np.zeros([5, 2], dtype=int)

row = []
for num in range(0, 2):
    row.append(num + 3)

a[3] = row
#
# a[0] = row
#
print(a)

# b = np.empty([1,2], dtype=int)
# rowb = []
# for num in range(0, 2):
#     rowb.append(num + 5)
#
# b = np.append(b, [row], axis=5)
# b[0] = rowb
#
# print(a)
# print(b)
#
# result = np.matmul(a, b)
#
# print(result)