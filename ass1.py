#!/usr/bin/python3

import math

# storing a 4x4 transformation matrix
class TMatrix:

    size = 4

    # initialize all values as 0s
    m = [[]]

    # Exercise 1.1
    # create a matrix
    def __init__(self, l = None):

        # initialize all values as 0s
        self.m = [[0 for x in range(self.size)] for y in range(self.size)]

        # identity matrix
        if l is None:
            # all diagonal values are 1s
            for i in range(self.size):
                self.m[i][i] = 1
        
        # set values individulaly from a list
        else:
            self.m = [[l[x+self.size*y] for x in range(self.size)] for y in range(self.size)]

    # Exercise 1.1
    # returns the product of the stored transformation matrix with other_matrix
    def mult(self, other_matrix):
        result = TMatrix()
        result.m = [[0 for x in range(result.size)] for y in range(result.size)]
        for i in range(self.size):
            for j in range(self.size):
                for k in range(other_matrix.size):
                    result.m[i][k] += self.m[i][j] * other_matrix.m[j][k]

        return result

    # Exercise 1.4
    # returns the product of the stored transformation matrix with a vector
    def mult_vec(self, vector):
        result = Vector4()
        for i in range(self.size):
            for j in range(len(vector.l)):
                result.l[i] += self.m[i][j] * vector.l[j]

        return result

# Exercise 1.3
class Vector4:
    l = []

    def __init__(self, a = 0, b = 0, c = 0, d = 0):
        new = []
        new.append(a)
        new.append(b)
        new.append(c)
        new.append(d)
        self.l = new

# Exercise 1.2
# Translation matrix
def make_trans_mat(x, y, z):
    result = TMatrix()
    result.m[0][3] = x
    result.m[1][3] = y
    result.m[2][3] = z

    return result

# Exercise 1.2
# Rotation matrix
def make_rot_mat(degree, axis):
    result = TMatrix()
    degree_sin = math.sin(math.radians(degree))
    degree_cos = math.cos(math.radians(degree))
    if axis == 'x':
        result.m[1][1] = degree_cos
        result.m[1][2] = -(degree_sin)
        result.m[2][1] = degree_sin
        result.m[2][2] = degree_cos
    elif axis == 'y':
        result.m[0][0] = degree_cos
        result.m[0][2] = degree_sin
        result.m[2][0] = -(degree_sin)
        result.m[2][2] = degree_cos
    elif axis == 'z':
        result.m[0][0] = degree_cos
        result.m[0][1] = -(degree_sin)
        result.m[1][0] = degree_sin
        result.m[1][1] = degree_cos

    return result

# Exercise 1.2
# Scaling matrix
def make_scale_mat(sx, sy, sz):
    result = TMatrix()
    result.m[0][0] = sx
    result.m[1][1] = sy
    result.m[2][2] = sz

    return result

# Exercise 1.3
# Euclidean distance between two homogeneous points (Vector4)
def euclidean_distance(point1, point2):
    sum = 0
    for i in range(len(point1.l)):
        # print(math.pow((point1.l[i] - point2.l[i]), 2))
        sum += math.pow((point1.l[i] - point2.l[i]), 2)

    return math.sqrt(sum)

def run():

    # Exercise 1.1
    # Showing that it works by multiplying A and B
    print("Constructing matrix A")
    l = []
    for i in range(1, 17):
        l.append(i)
    a = TMatrix(l)
    print("Matrix A: ")
    print(a.m)

    print("Constructing matrix B")
    l = []
    for i in range(1, 16, 2):
        l.append(i)
    for i in range(2, 17, 2):
        l.append(i)
    b = TMatrix(l)
    print("Matrix B: ")
    print(b.m)

    print("Multiplying A and B")
    c = a.mult(b)
    print("Result: ")
    print(c.m)

    # Exercise 1.2
    # Showing that it works
    print("Translation matrix")
    print(make_trans_mat(1, 2, 3).m)

    print("Rotation matrix 1")
    print(make_rot_mat(45, 'x').m)

    print("Rotation matrix 2")
    print(make_rot_mat(90, 'y').m)

    print("Rotation matrix 3")
    print(make_rot_mat(120, 'z').m)

    print("Scaling matrix")
    print(make_scale_mat(1, 2, 3).m) 

    # Exercise 1.3
    # Showing that it works
    print("Euclidean distance")
    vector = Vector4(2, 4, 6, 2)
    rotcev = Vector4(0, 0, 0, 1)
    print("Vector 1")
    print(vector.l)
    print("Vector 2")
    print(rotcev.l)
    print(euclidean_distance(vector, rotcev))

    # Exercise 1.4
    # Showing that it works
    print("Multiplying A with v")
    v = Vector4(1, 2, 3, 1)
    print(a.mult_vec(v).l)

    # Exercise 1.5
    # NOTE: we found these angles by trying the rotation ourselves
    # using physical objects in the real world
    print("Rotation ambiguity")
    r90x = make_rot_mat(90, 'x')
    r_a_z = make_rot_mat(90, 'z')
    r_b_y = make_rot_mat(270, 'y')
    mult_a_z = r90x.mult(r_a_z)
    mult_b_y = r_b_y.mult(r90x)
    print("alpha")
    print(mult_a_z.m)
    print("beta")
    print(mult_b_y.m)


if __name__ == "__main__":
    run()