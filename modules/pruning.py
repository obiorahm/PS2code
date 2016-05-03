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
    #tree = copy_node(root)
    
    #accuracy, new_tree = better_prunned_tree(tree, validation_set)
    #print accuracy
    #print "the final tree length of nodes ", len(breadth_first_search(new_tree,[new_tree]))

    #return new_tree
    pass

def better_prunned_tree(tree, validation_set):
    org_tree = copy_node(tree)
    new_tree = tree
    lst_nodes = breadth_first_search(new_tree,[new_tree])
    init_accuracy = validation_accuracy(new_tree, validation_set)
    lst_nodes.reverse()
    print len(lst_nodes)
    for node in lst_nodes:
        y = node
        for item in [0,1, 2]:
            x = copy_node(y)
            y = prune_node(y, item)
            print "the number of nodes is", len(breadth_first_search(new_tree,[new_tree]))
            accuracy = validation_accuracy(new_tree, validation_set)
            print accuracy
            if accuracy > init_accuracy:
                return accuracy, new_tree
            elif (accuracy == init_accuracy):
                org_tree = copy_node(new_tree)
            #else:
                #node = copy_node(x)
        print "twin accuracy"
    print "had to stop"
    return init_accuracy, org_tree

        
def prune_node(node, item):
    node.label = item

    node.is_nominal = None

    node.splitting_value = None
    node.children = {}


    return node 
    

def breadth_first_search(root, queue,):
    if root.label != None:
        return queue
    else:
        children = get_children(root)
        queue = queue + children
        for item in children:
            queue = breadth_first_search(item, queue)
        return queue          
        
        
    
def get_children(root):
    queue = []
    if root.label != None:
        return queue
    elif root.is_nominal:
        for key in root.children:
            if root.children[key].label == None:
                queue.append(root.children[key])
    else:
        for item in root.children:
            if item.label == None:
                queue.append(item)
    return queue
        


def copy_node(node):
    new_node = Node()
    new_node.label = node.label
    new_node.decision_attribute = node.decision_attribute
    new_node.is_nominal = node.is_nominal
    new_node.value = node.value
    new_node.splitting_value = node.splitting_value

    if node.is_nominal:
        new_node.children = {}
        for key in node.children:
            new_node.children[key] = copy_node(node.children[key])
    else:
        new_node.children = []
        for i in range(len(node.children)):
            new_node.children.append(copy_node(node.children[i]))
    new_node.name = node.name

    return new_node
    


    
def validation_accuracy(tree, validation_set):
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

    n =reduced_error_pruning(n,data_set,[[1, 0.11], [0, 0.42], [0, 0.86], [0, 0.55], [0, 0.66], [1, 0.01], [1, 0.11], [1, 0.84], [1, 0.42], [0, 0.51], [1, 0.4]])

    return n

def test_breadth_first_search():
    n0 = Node()
    n0.label = 1
    n1 = Node()
    n1.label = 0
    n = Node()
    n.label = None
    n.decision_attribute = 1
    n.is_nominal = True
    n.name = "whatever"
    n.children = {1: n0, 2: n1}
    print n.print_tree()
    print breadth_first_search(n)
    return n

def more_tests():
    n2 = Node()
    n2.name = "attrib2"
    n2.label = 1

    n3 = Node()
    n3.name = "attrib3"
    n3.label = 0 
    
    n0 = Node()
    n0.name = "attrib0"
    n0.is_nominal = True
    n0.children = {1: n2, 2: n3}

    n4 = Node()
    n4.name = "attrib4"
    n4.label = 2

    n5 = Node()
    n5.name = "attrib5"
    n5.label = 3
    
    n1 = Node()
    n1.name = "attrib1"
    n1.is_nominal = True
    n1.children = {1: n4, 2: n5}

    n = Node()
    n.label = None
    n.decision_attribute = 1
    n.is_nominal = True
    n.name = "attrib"
    n.children = {1: n0, 2: n1}
    print n.print_dnf_tree()
    print n.print_tree()
    print breadth_first_search(n, [n])

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
    
    print n.print_tree()
    n = reduced_error_pruning(n,data_set,[[1, 0.11], [0, 0.42], [0, 0.86], [0, 0.55], [0, 0.66], [1, 0.01], [1, 0.11], [1, 0.84], [1, 0.42], [0, 0.51], [1, 0.4]])
    print n.print_tree()
    return n
 



