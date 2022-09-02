import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist

a = np.random.randint(0, 100, [2, 4])
b = np.random.randint(0, 100, [5, 4])

print(a,'\n')
print(b, '\n')

def dist_1(a, b):
    return [np.sqrt(np.sum((a[:,np.newaxis]-b)**2, axis=2))]

def dist_2(a, b):
    return np.linalg.norm(a[:,np.newaxis]-b, axis=2)

def dist_3(a,b):
    return cdist(a,b)

if __name__=='__main__':
    
    print(dist_1(a, b), '\n')

    print(dist_2(a,b), '\n')

    print(dist_3(a,b), '\n')



