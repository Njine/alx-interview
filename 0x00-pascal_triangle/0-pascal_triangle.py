#!/usr/bin/python3
'''A Pascal's triangle module.'''

def pascal_triangle(n):
    '''Generate Pascal's triangle up to the specified number of rows.'''
    triangle = []
    if type(n) is not int or n <= 0:
        return triangle
    for i in range(n):
        row = []
        for j in range(i + 1):
            if j == 0 or j == i:
                row.append(1)
            elif i > 0 and j > 0:
                row.append(triangle[i - 1][j - 1] + triangle[i - 1][j])
        triangle.append(row)
    return triangle

