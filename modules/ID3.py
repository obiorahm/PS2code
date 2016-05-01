import math
from node import Node
import sys

count_mma = 0

def make_child_nominal(n,data_set, attr_pos, attribute_metadata, numerical_splits_count, depth):
    n.children = dict()
    split_dict = split_on_nominal(data_set, attr_pos)
    for key in split_dict:
        is_empty(n,split_dict[key], attribute_metadata, numerical_splits_count, depth, key)
    is_empty(n,modedict(split_dict), attribute_metadata, numerical_splits_count, depth, 'unknown')
    return n

def make_child_numeric(n,data_set, attr_pos, attr_val, attribute_metadata, numerical_splits_count, depth):
    n.children = []
    n.splitting_value = attr_val
    split_dict = split_on_numerical(data_set, attr_pos, attr_val)
    is_empty(n, split_dict[0], attribute_metadata, numerical_splits_count, depth,'flag')
    is_empty(n, split_dict[1], attribute_metadata, numerical_splits_count, depth,'flag')
    is_empty(n, split_dict[modelst(split_dict[0],split_dict[1])], attribute_metadata, numerical_splits_count, depth, 'flag')
    return n


def test_numeric_splits(n, data_set, attr_pos, attr_val, attribute_metadata, numerical_splits_count, depth):
    if numerical_splits_count[attr_pos] == 0:
        n.label = mode(data_set)
        global count_mma
        count_mma = count_mma - 1
        print count_mma
        return n
    else:
        numerical_splits_count[attr_pos] -=1
        return make_child_numeric(n, data_set, attr_pos, attr_val, attribute_metadata, numerical_splits_count, depth)    

def make_children(n, data_set, attr_pos, attr_val, attribute_metadata, numerical_splits_count, depth):
    n.is_nominal = (attr_val == False)
    if n.is_nominal:
        return make_child_nominal(n,data_set, attr_pos, attribute_metadata, numerical_splits_count, depth)
    else:
        return test_numeric_splits(n, data_set, attr_pos, attr_val, attribute_metadata, numerical_splits_count, depth)


def is_empty(n,data_set, attribute_metadata, numerical_splits_count, depth,flag_nominal):
    global count_mma
    if (not data_set):
        n.label = mode(data_set)
        global count_mma
        count_mma = count_mma - 1
        print count_mma
    elif(flag_nominal == 'flag'):
        n.children.append(ID3(data_set, attribute_metadata, numerical_splits_count, depth))
    else:
        n.children[flag_nominal] = ID3(data_set, attribute_metadata, numerical_splits_count, depth)


def ID3(data_set, attribute_metadata, numerical_splits_count, depth):
    '''
    See Textbook for algorithm.
    Make sure to handle unknown values, some suggested approaches were
    given in lecture.
    ========================================================================================================
    Input:  A data_set, attribute_metadata, maximum number of splits to consider for numerical attributes,
	maximum depth to search to (depth = 0 indicates that this node should output a label)
    ========================================================================================================
    Output: The node representing the decision tree learned over the given data set
    ========================================================================================================

    '''
    # Your code here
    n = Node()

    if (n.label != None):
        return n
    elif (depth == 0):
        n.label = mode(data_set)
        return n    
    elif (not attribute_metadata):
        n.label = mode(data_set)
        return n
    elif check_homogenous(data_set):
        n.label = check_homogenous(data_set)
        return n
    else:
        global count_mma
        count_mma = count_mma + 1
        print count_mma

        attr_pos, attr_val = pick_best_attribute(data_set, attribute_metadata, numerical_splits_count)
        n.decision_attribute = attr_pos
        n.name = attribute_metadata[attr_pos]['name']
        depth -=1
        return make_children(n, data_set, attr_pos, attr_val, attribute_metadata, numerical_splits_count, depth)

def check_homogenous(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Checks if the attribute at index 0 is the same for the data_set, if so return output otherwise None.
    ========================================================================================================
    Output: Return either the homogenous attribute or None
    ========================================================================================================
    '''
    # Your code here
    curr_item = data_set[0][0]
    changed = False;
    for item in data_set:
        if (curr_item != item[0]):
            changed = True
            break
        else:
            curr_item = item[0]
    if (changed):
        return
    else:
        return item[0]    
    pass
# ======== Test Cases =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  None
# data_set = [[0],[1],[None],[0]]
# check_homogenous(data_set) ==  None
# data_set = [[1],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  1

def max_IGR(attribute_metadata, gain_ratios):
    max_ratio = max(gain_ratios[1:len(gain_ratios)])
    max_ratio_id = gain_ratios.index(max_ratio)
    if (max_ratio == 0):
        return False, False
    elif (attribute_metadata[max_ratio_id]['is_nominal']):
        return max_ratio_id, False
    else:
        return max_ratio_id, max_ratio[1]


def pick_best_attribute(data_set, attribute_metadata, numerical_splits_count):
    '''
    ========================================================================================================
    Input:  A data_set, attribute_metadata, splits counts for numeric
    ========================================================================================================
    Job:    Find the attribute that maximizes the gain ratio. If attribute is numeric return best split value.
            If nominal, then split value is False.
            If gain ratio of all the attributes is 0, then return False, False
            Only consider numeric splits for which numerical_splits_count is greater than zero
    ========================================================================================================
    Output: best attribute, split value if numeric
    ========================================================================================================
    '''
    # Your code here
    if numerical_splits_count == 0:
        return
    gain_ratios = []
    for item in attribute_metadata:
        if (item['is_nominal']):
            gain_ratios.append(gain_ratio_nominal(data_set, attribute_metadata.index(item)))
        else:
            gain_ratios.append(gain_ratio_numeric(data_set, attribute_metadata.index(item), 1))
    return max_IGR(attribute_metadata, gain_ratios)
    
    pass

# # ======== Test Cases =============================
# numerical_splits_count = [20,20]
# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "opprundifferential",'is_nominal': False}]
# data_set = [[1, 0.27], [0, 0.42], [0, 0.86], [0, 0.68], [0, 0.04], [1, 0.01], [1, 0.33], [1, 0.42], [0, 0.51], [1, 0.4]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, 0.51)
# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "weather",'is_nominal': True}]
# data_set = [[0, 0], [1, 0], [0, 2], [0, 2], [0, 3], [1, 1], [0, 4], [0, 2], [1, 2], [1, 5]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, False)

# Uses gain_ratio_nominal or gain_ratio_numeric to calculate gain ratio.

def mode(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Takes a data_set and finds mode of index 0.
    ========================================================================================================
    Output: mode of index 0.
    ========================================================================================================
    '''
    # Your code here
    sum_0 = 0
    sum_1 = 0
    for item in data_set:
        if (item[0] == 0):
            sum_0 += 1
        elif (item[0] == 1):
            sum_1 += 1
    if sum_0>= sum_1:
        return 0
    else:
        return 1
    pass
# ======== Test case =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# mode(data_set) == 1
# data_set = [[0],[1],[0],[0]]
# mode(data_set) == 0

def modelst(lst1, lst2):
    if len(lst1)>= len(lst2):
        return 0
    return 1

def modedict(dict1):
    max_dict = dict1.keys()[0]

    for key in dict1:
        x = len(dict1[key])
        y = len(dict1[max_dict])
        if x >= y:
            max_dict = key
    return max_dict


def plogp(p):
    if (p == 0):
        return 0
    else:
        return p * math.log(p,2)


def entropy(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Calculates the entropy of the attribute at the 0th index, the value we want to predict.
    ========================================================================================================
    Output: Returns entropy. See Textbook for formula
    ========================================================================================================
    '''
    num_training_set = float(len(data_set))
    if (num_training_set == 0):
        return 0
    else:
        split_val_lst = make_lst_attr(data_set, 0)
        return intrinsic_value(data_set, split_val_lst)


# ======== Test case =============================
# data_set = [[0],[1],[1],[1],[0],[1],[1],[1]]
# entropy(data_set) == 0.811
# data_set = [[0],[0],[1],[1],[0],[1],[1],[0]]
# entropy(data_set) == 1.0
# data_set = [[0],[0],[0],[0],[0],[0],[0],[0]]
# entropy(data_set) == 0

def checkdivby0(numerator, denominator):
    if (denominator == 0):
        return 0
    else:
        return (numerator/denominator)

def make_lst_attr(data_set, attribute):
    attr_dict = split_on_nominal(data_set, attribute)
    attr_lst = []
    for key in attr_dict:
        attr_lst.append(attr_dict[key])
    return attr_lst


def gain_ratio_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  Subset of data_set, index for a nominal attribute
    ========================================================================================================
    Job:    Finds the gain ratio of a nominal attribute in relation to the variable we are training on.
    ========================================================================================================
    Output: Returns gain_ratio. See https://en.wikipedia.org/wiki/Information_gain_ratio
    ========================================================================================================
    '''
    # Your code here
    lst_values = make_lst_attr(data_set, attribute)
    return information_gain_ratio(data_set, lst_values)
    pass
# ======== Test case =============================
# data_set, attr = [[1, 2], [1, 0], [1, 0], [0, 2], [0, 2], [0, 0], [1, 3], [0, 4], [0, 3], [1, 1]], 1
# gain_ratio_nominal(data_set,attr) == 0.11470666361703151
# data_set, attr = [[1, 2], [1, 2], [0, 4], [0, 0], [0, 1], [0, 3], [0, 0], [0, 0], [0, 4], [0, 2]], 1
# gain_ratio_nominal(data_set,attr) == 0.2056423328155741
# data_set, attr = [[0, 3], [0, 3], [0, 3], [0, 4], [0, 4], [0, 4], [0, 0], [0, 2], [1, 4], [0, 4]], 1
# gain_ratio_nominal(data_set,attr) == 0.06409559743967516

def IGR_numeric(data_set, attr, split_value):
    ls_tresh, gr_tresh = split_on_numerical(data_set, attr, split_value)
    return information_gain_ratio(data_set, [ls_tresh, gr_tresh])


def gain_ratio_numeric(data_set, attribute, steps = 1):
    '''
    ========================================================================================================
    Input:  Subset of data set, the index for a numeric attribute, and a step size for normalizing the data.
    ========================================================================================================
    Job:    Calculate the gain_ratio_numeric and find the best single threshold value
            The threshold will be used to split examples into two sets
                 those with attribute value GREATER THAN OR EQUAL TO threshold
                 those with attribute value LESS THAN threshold
            Use the equation here: https://en.wikipedia.org/wiki/Information_gain_ratio
            And restrict your search for possible thresholds to examples with array index mod(step) == 0
    ========================================================================================================
    Output: This function returns the gain ratio and threshold value
    ========================================================================================================
    '''
    # Your code here
    lst_ratios =[]
    lst_trhd =[]
    for i in range(0,len(data_set), steps):
        lst_ratios.append(IGR_numeric(data_set, attribute, data_set[i][attribute]))
        lst_trhd.append(data_set[i][attribute])
    ratio_index = lst_ratios.index(max(lst_ratios))
    return lst_ratios[ratio_index], lst_trhd[ratio_index]
    pass
# ======== Test case =============================
# data_set,attr,step = [[1,0.05], [1,0.17], [1,0.64], [0,0.38], [1,0.19], [1,0.68], [1,0.69], [1,0.17], [1,0.4], [0,0.53]], 1, 2
# gain_ratio_numeric(data_set,attr,step) == (0.31918053332474033, 0.64)
# data_set,attr,step = [[1, 0.35], [1, 0.24], [0, 0.67], [0, 0.36], [1, 0.94], [1, 0.4], [1, 0.15], [0, 0.1], [1, 0.61], [1, 0.17]], 1, 4
# gain_ratio_numeric(data_set,attr,step) == (0.11689800358692547, 0.94)
# data_set,attr,step = [[1, 0.1], [0, 0.29], [1, 0.03], [0, 0.47], [1, 0.25], [1, 0.12], [1, 0.67], [1, 0.73], [1, 0.85], [1, 0.25]], 1, 1
# gain_ratio_numeric(data_set,attr,step) == (0.23645279766002802, 0.29)

def split_on_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  subset of data set, the index for a nominal attribute.
    ========================================================================================================
    Job:    Creates a dictionary of all values of the attribute.
    ========================================================================================================
    Output: Dictionary of all values pointing to a list of all the data with that attribute
    ========================================================================================================
    '''
    # Your code here
    attr_dict = dict()
    for item in data_set:
        if (item[attribute] in attr_dict):
            (attr_dict[item[attribute]]).append(item)
        else:
            attr_dict[item[attribute]] = [item]
    return attr_dict
    pass
# ======== Test case =============================
# data_set, attr = [[0, 4], [1, 3], [1, 2], [0, 0], [0, 0], [0, 4], [1, 4], [0, 2], [1, 2], [0, 1]], 1
# split_on_nominal(data_set, attr) == {0: [[0, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3]], 4: [[0, 4], [0, 4], [1, 4]]}
# data_set, attr = [[1, 2], [1, 0], [0, 0], [1, 3], [0, 2], [0, 3], [0, 4], [0, 4], [1, 2], [0, 1]], 1
# split on_nominal(data_set, attr) == {0: [[1, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3], [0, 3]], 4: [[0, 4], [0, 4]]}

def split_on_numerical(data_set, attribute, splitting_value):
    '''
    ========================================================================================================
    Input:  Subset of data set, the index for a numeric attribute, threshold (splitting) value
    ========================================================================================================
    Job:    Splits data_set into a tuple of two lists, the first list contains the examples where the given
	attribute has value less than the splitting value, the second list contains the other examples
    ========================================================================================================
    Output: Tuple of two lists as described above
    ========================================================================================================
    '''
    # Your code here
    gr_trhd_lst = []
    ls_trhd_lst = []
    for item in data_set:
        if (item[attribute]>= splitting_value):
            gr_trhd_lst.append(item)
        else:
            ls_trhd_lst.append(item)
    return ls_trhd_lst, gr_trhd_lst
    pass
# ======== Test case =============================
# d_set,a,sval = [[1, 0.25], [1, 0.89], [0, 0.93], [0, 0.48], [1, 0.19], [1, 0.49], [0, 0.6], [0, 0.6], [1, 0.34], [1, 0.19]],1,0.48
# split_on_numerical(d_set,a,sval) == ([[1, 0.25], [1, 0.19], [1, 0.34], [1, 0.19]],[[1, 0.89], [0, 0.93], [0, 0.48], [1, 0.49], [0, 0.6], [0, 0.6]])
# d_set,a,sval = [[0, 0.91], [0, 0.84], [1, 0.82], [1, 0.07], [0, 0.82],[0, 0.59], [0, 0.87], [0, 0.17], [1, 0.05], [1, 0.76]],1,0.17
# split_on_numerical(d_set,a,sval) == ([[1, 0.07], [1, 0.05]],[[0, 0.91],[0, 0.84], [1, 0.82], [0, 0.82], [0, 0.59], [0, 0.87], [0, 0.17], [1, 0.76]])

def ratio(data_set, item):
    return checkdivby0(float(len(item)), float(len(data_set)))

def information_gain(data_set, lst_values):
    sum_all = 0.0
    for item in lst_values:
        sum_all += (ratio(data_set, item) * entropy(item))
    return (entropy(data_set) - sum_all)

def intrinsic_value(data_set,lst_values):
    sum_all = 0.0
    for item in lst_values:
        sum_all += plogp(ratio(data_set,item))
    return (-1 * sum_all)

def information_gain_ratio(data_set, lst_vals):
    IG = information_gain(data_set, lst_vals)
    IV = intrinsic_value(data_set, lst_vals)
    return checkdivby0(IG,IV)
