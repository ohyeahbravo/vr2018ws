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

    

if __name__ == "__main__":
    run()