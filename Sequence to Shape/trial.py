from collections import Counter

x = [[(0, 0), (0, 1)], [(0, 0), (0, 2)]]
y = [[(0, 0), (0, 1)], [(0, 0), (0, 1)]]
z = [[(0, 0), (0, 1)], [(0, 1), (0, 0)]]

print(x[0] == x[1])
print(y[0] == y[1])
print(z[0] == z[1])

print(Counter(z[0]) == Counter(z[1]))
