#!/usr/bin/python3
# Hiyeon Kim, 118654
# Lars Meyer, 114719

import math

# storing a 4x4 transformation matrix
# added a comment for test (ignore it Lars!)
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
'''
FEEDBACK: To compute the distance in Euclidean space, 
all points have to be normalized by their homogeneous component.
For the first point, the homogeneous component is 2.
'''
def normalize(point):
    if point.l[3] != 0:
        v = Vector4()
        v.l = [dim / point.l[3] for dim in point.l]
        return v

def euclidean_distance(apoint1, apoint2):

    # normalize the vectors by their homogeneous component
    point1 = normalize(apoint1)
    point2 = normalize(apoint2)

    sum = 0
    for i in range(len(point1.l)):
        # print(math.pow((point1.l[i] - point2.l[i]), 2))
        sum += math.pow((point1.l[i] - point2.l[i]), 2)

    return math.sqrt(sum)

def run():

    # Exercise 1.1
    # Showing that it works by multiplying A and B
    print("Exercise 1.1")
    l = []
    for i in range(1, 17):
        l.append(i)
    a = TMatrix(l)
    print("Matrix A: ")
    print(a.m)
    print()

    l = []
    for i in range(1, 16, 2):
        l.append(i)
    for i in range(2, 17, 2):
        l.append(i)
    b = TMatrix(l)
    print("Matrix B: ")
    print(b.m)
    print()

    print("Multiplying A and B")
    c = a.mult(b)
    print("Result: ")
    print(c.m)
    print()

    # Exercise 1.2
    # Showing that it works
    print("Exercise 1.2")
    print("Translation matrix:")
    print(make_trans_mat(1, 2, 3).m)
    print()

    print("Rotation matrix 1:")
    print(make_rot_mat(45, 'x').m)
    print()

    print("Rotation matrix 2:")
    print(make_rot_mat(90, 'y').m)
    print()

    print("Rotation matrix 3:")
    print(make_rot_mat(120, 'z').m)
    print()

    print("Scaling matrix:")
    print(make_scale_mat(1, 2, 3).m)
    print()

    # Exercise 1.3
    # Showing that it works
    print("Exercise 1.3")
    vector = Vector4(2, 4, 6, 2)
    rotcev = Vector4(0, 0, 0, 1)
    print("Vector 1")
    print(vector.l)
    print()

    print("Vector 2")
    print(rotcev.l)
    print()

    print("Euclidean distance")
    print(euclidean_distance(vector, rotcev))
    print()

    # Exercise 1.4
    # Showing that it works
    print("Exercise 1.4")
    print("Multiplying A with v. Result:")
    v = Vector4(1, 2, 3, 1)
    print(a.mult_vec(v).l)
    print()

    # Exercise 1.5
    # NOTE: we found these angles by trying the rotation ourselves
    # using physical objects in the real world
    print("Exercise 1.5")
    print("Rotation disambiguities")
    r90x = make_rot_mat(90, 'x')
    r_a_z = make_rot_mat(90, 'z')
    r_b_y = make_rot_mat(270, 'y')
    mult_a_z = r90x.mult(r_a_z)
    mult_b_y = r_b_y.mult(r90x)
    print()
    print("Not rounded:")
    print("alpha = 90°")
    print("Matrix:")
    print(mult_a_z.m)
    print()
    print("beta = 270°")
    print("Matrix:")
    print(mult_b_y.m)
    print()

    mult_a_z_rounded = TMatrix();
    mult_b_y_rounded = TMatrix();

    mult_a_z_rounded.m = [[0 if (abs(x) < 1e-15) else x for x in y] for y in mult_a_z.m]
    mult_b_y_rounded.m = [[0 if (abs(x) < 1e-15) else x for x in y] for y in mult_b_y.m]

    print("Rounded with ε = 10^-15:")
    print("alpha = 90°")
    print("Matrix:")
    print(mult_a_z_rounded.m)
    print()
    print("beta = 270°")
    print("Matrix:")
    print(mult_b_y_rounded.m)
    
if __name__ == "__main__":
    run()