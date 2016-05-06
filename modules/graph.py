from random import *
from ID3 import *
from operator import xor
from parse import parse
import matplotlib.pyplot as plt
import numpy as np
import os.path
import random
from pruning import *





def get_graph(train_set, attribute_metadata, validate_set, numerical_splits_count, depth, iterations, lower, upper, increment):
    tree_acc = []
    t = []

    for i in range(0,100, 20):
        split_count = [numerical_splits_count[1]] * len(numerical_splits_count)
        number=float(len(train_set))*(float(i)/100.0)
        partial=random.sample(train_set, int(number))   
        n = ID3(partial, attribute_metadata, split_count, depth)
        x = validation_accuracy(n, validate_set)
        print number, x
        tree_acc.append(x)
        t.append(number)
    plt.plot(t,tree_acc)
    plt.show()
    
    
