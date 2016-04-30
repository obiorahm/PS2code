import os.path
from operator import xor
from parse import *
from node import Node

# DOCUMENTATION
# ========================================
# this function outputs predictions for a given data set.
# NOTE this function is provided only for reference.
# You will not be graded on the details of this function, so you can change the interface if 
# you choose, or not complete this function at all if you want to use a different method for
# generating predictions.

def create_predictions(tree, predict):
    '''
    Given a tree and a url to a data_set. Create a csv with a prediction for each result
    using the classify method in node class.
    '''
    pred_file = open('./output/predictions.txt','w+')
    pred_val = ''
    ppredict, attribute_meta_data = parse(predict, True)

    for item in ppredict:
        pred_val = pred_val + str(tree.classify(item)) + '\n'

    pred_file.write(pred_val)
    pred_file.close()
