import numpy as np

a = np.empty([1,2], dtype=int)

row = []
for num in range(0, 2):
    row.append(num + 3)

a = np.append(a, [row], axis=0)

a[0] = row

b = np.empty([1,2], dtype=int)
rowb = []
for num in range(0, 2):
    rowb.append(num + 5)

b = np.append(b, [row], axis=0)
b[0] = rowb

print(a)
print(b)

result = np.matmul(a, b)

print(result)

