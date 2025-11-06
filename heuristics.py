from math import sqrt

# distanza Manhattan
def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# distanza euclidea "in linea d'aria"
def euclidean_distance(a, b):
    return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

# distanza diagonale o di Chebyshev
def diagonal_distance(a, b):
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return max(dx, dy)
