from random import *
from ID3 import *
from node import *
from operator import xor
from parse import parse
import matplotlib.pyplot as plt
import numpy as np
import os.path
import random
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
    t = np.arange(lower+increment, upper,increment)
    data=[]
    for k in range(0,len(t)):
        array=get_graph_data(train_set, attribute_metadata, validate_set, numerical_splits_count, iterations, lower+increment)
        data.append(array[iterations-1])
        lower=lower+increment
    plt.plot(t, data)
    plt.show()
    
