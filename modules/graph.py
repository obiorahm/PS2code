from random import shuffle
from ID3 import *
from operator import xor
from parse import parse
import matplotlib.pyplot as plt
import os.path
from pruning import validation_accuracy

depth=0

def get_graph_accuracy_partial(train_set, attribute_metadata, validate_set, numerical_splits_count, pct):
    number=len(train_set)*pct
    partial=random.sample(train_set, int(number))
    n= ID3(partial, attribute_metadata, numerical_splits_count, depth)
    accuracy=validation_accuracy(n, validate_set)
    return accuracy

def get_graph_data(train_set, attribute_metadata, validate_set, numerical_splits_count, iterations, pct):
    array=[]
    for i in range(1,iterations+1):
        sum=0
        for j in range(0,i):
            sum=sum+get_graph_accuracy_partial(train_set, attribute_metadata, validate_set, numerical_splits_count, pct)
        array.append(float(sum)/i)
    return array
    
# get_graph will plot the points of the results from get_graph_data and return a graph
def get_graph(train_set, attribute_metadata, validate_set, numerical_splits_count, depth, iterations, lower, upper, increment):
    t = np.arange(lower, upper,increment)
    data=[]
    for k in range(0,len(t)+1):
        data.append(get_graph_data(train_set, attribute_metadata, validate_set, numerical_splits_count, iterations, k))
    plt.plot(t, data)
    plt.show()
    
attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "opprundifferential",'is_nominal': False}]
data_set = [[1, 0.27], [0, 0.42], [0, 0.86], [0, 0.68], [0, 0.04], [1, 0.01], [1, 0.33], [1, 0.42], [1, 0.42], [0, 0.51], [1, 0.4]]
numerical_splits_count = [5, 5]
val_set = [[1, 0.5],[0,0.3],[0,0.9],[1,0.9],[1,0.27]]
print get_graph_accuracy_partial(data_set, attribute_metadata, val_set, numerical_splits_count, 0.5)
print get_graph_data(data_set, attribute_metadata, val_set, numerical_splits_count, 4, 0.5)
get_graph(data_set, attribute_metadata, val_set, numerical_splits_count, depth, 3, 0,1,0.5)
