import numpy as np

#This is the Global Linear Least sqaures approximation module

def least_squares_approximation(x, y):
    A = np.vstack([x, np.ones(len(x))]).T
    m, c = np.linalg.lstsq(A, y, rcond=None)[0]
    return m, c

def predict(x, m, c):
    return m * x + c