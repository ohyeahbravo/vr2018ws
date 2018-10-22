#!/usr/bin/python3

import math

# storing a 4x4 transformation matrix
class TMatrix:

    size = 4

    # Exercise 1.1
    # create an identity matrix
    # code same as https://stackoverflow.com/a/40269891 we can change but...
    def identity(self, n):

        # initialize all values as 0s
        m = [[0 for x in range(n)] for y in range(n)]

        # OR
        # m = [0] * n
        # for i in range(n):
        #     m[i] = [0] * n

        # all diagonal values are 1s
        for i in range(n):
            m[i][i] = 1

        return m

    # Exercise 1.1
    # create a matrix while individually setting the values
    # ... from a list?
    # NOTE : not sure if this is correct
    def matrix(self, n, l):
        
        m = [[l[x+n*y] for x in range(n)] for y in range(n)]
        
        # OR
        # m = []
        # for y in range(n):
        #     m.append([])
        #     for x in range(n):
        #         m[y].append(l[x+n*y])    

        return m

    # Exercise 1.1
    # returns the product of the stored transformation matrix with other_matrix
    # NOTE : not sure if this is correct
    def mult(self, other_matrix):
        pass

    # illustrate that your code is working by multiplying A * B
    # and printing the result
    def run(self):
        l = []
        for i in range(1, 17):
            l.append(i)
        
        A = self.identity(self.size)
        print(A)

if __name__ == "__main__":
    TMatrix().run()