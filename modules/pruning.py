from node import Node
from ID3 import *
from operator import xor

# Note, these functions are provided for your reference.  You will not be graded on their behavior,
# so you can implement them as you choose or not implement them at all if you want to use a different
# architecture for pruning.

def reduced_error_pruning(root,training_set,validation_set):
    '''
    take the a node, training set, and validation set and returns the improved node.
    You can implement this as you choose, but the goal is to remove some nodes such that doing so improves validation accuracy.
    '''
    # Your code here
    accuracy = validation_accuracy(root, validation_set)
    new_root = root
    if (root.label == None and (not root.children)):
        return root
    elif (root.label != None):
        del new_root
        
    pass
# 

def validation_accuracy(tree,validation_set):
    '''
    takes a tree and a validation set and returns the accuracy of the set on the given tree
    '''
    # Your code here
    count_correct = 0
    total_number = len(validation_set)
    for example in validation_set:
        classification = tree.classify(example)
        if classification == example[0]:
            count_correct +=1
    return float(count_correct)/float(total_number)
        
    pass

def test_validation_accuracy():
    attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "opprundifferential",'is_nominal': False}]
    data_set = [[1, 0.27], [0, 0.42], [0, 0.86], [0, 0.68], [0, 0.04], [1, 0.01], [1, 0.33], [1, 0.42], [1, 0.42], [0, 0.51], [1, 0.4]]
    numerical_splits_count = [5, 5]
    n = ID3(data_set, attribute_metadata, numerical_splits_count, 0)
    print validation_accuracy(n,data_set)

    numerical_splits_count = [1, 1]
    n = ID3(data_set, attribute_metadata, numerical_splits_count, 5)
    print validation_accuracy(n,data_set)

    numerical_splits_count = [5, 5]
    n = ID3(data_set, attribute_metadata, numerical_splits_count, 5)
    print validation_accuracy(n,data_set)
