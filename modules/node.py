# DOCUMENTATION
# =====================================
# Class node attributes:
# ----------------------------
# children - a list of 2 if numeric and a dictionary if nominal.  
#            For numeric, the 0 index holds examples < the splitting_value, the 
#            index holds examples >= the splitting value
#
# label - is None if there is a decision attribute, and is the output label (0 or 1 for
#	the homework data set) if there are no other attributes
#       to split on or the data is homogenous
#
# decision_attribute - the index of the decision attribute being split on
#
# is_nominal - is the decision attribute nominal
#
# value - Ignore (not used, output class if any goes in label)
#
# splitting_value - if numeric, where to split
#
# name - name of the attribute being split on

class Node:
    def __init__(self):
        # initialize all attributes
        self.label = None
        self.decision_attribute = None
        self.is_nominal = None
        self.value = None
        self.splitting_value = None
        self.children = {}
        self.name = None

    def classify(self, instance):
        '''
        given a single observation, will return the output of the tree
        '''
	# Your code here
        if (self.label != None):
            return self.label
        elif self.is_nominal:
            return self.children[instance[self.decision_attribute]].classify(instance)
        elif (instance[self.decision_attribute] < self.splitting_value):
            return self.children[0].classify(instance)
        else:
            return self.children[1].classify(instance)
        pass

    def print_tree(self, indent = 0):
        '''
        returns a string of the entire tree in human readable form
        '''
        # Your code here
        print (pre_print(self ,indent = 0))        
        pass


    def print_dnf_tree(self):
        '''
        returns the disjunct normalized form of the tree.
        '''
        print print_dnf(order_dnf(self,[]))

def order_dnf(n,all =[]):
    if (n.label != None):
        return ['('] + all + [n.label] + [')'] + ['$']
    elif (n.is_nominal == True):
        lst_attr =[]
        for key in n.children:
            attr = order_dnf(n.children[key], all + [str(n.name) + " = " + str(key)])
            lst_attr = lst_attr + attr
        return lst_attr
    elif(n.splitting_value != None):
        lst_attr =[]
        cmpr_sign = [" <  "," >= "]
        for item in n.children:
            attr = order_dnf(item, all + [str(n.name) + cmpr_sign[n.children.index(item)] + str(n.splitting_value)])
            lst_attr = lst_attr + attr
        return lst_attr
    else:
        return ['('] + all + [')'] + ['$']
    
def print_dnf(lst):
    dnf = lst[0]
    len_lst = len(lst)
    prev = True
    for i in range(1,len_lst - 1):
        if (lst[i] == "(" or lst[i] == ")"):
            dnf = dnf + lst[i]
            prev = True
        elif lst[i] == "$":
            dnf = dnf + " or \n"
            prev = True
        else:
            if prev:
                dnf = dnf + str(lst[i])
            else:
                dnf = dnf + " and " +str(lst[i])
            prev = False            
    return dnf + "\n"
    
      
        

def pre_print(n ,indent = 0):
    tab = "\t"* indent
    if (n.label != None):
        return tab + "leaf: " + str(n.label) + "\n"
    elif (n.is_nominal == True):
        x = ''
        for key in n.children:
            tab += x + (str(n.name)+ " = " + str(key) + "\n" + pre_print(n.children[key], indent + 1))
            x = "\t"* indent
        return tab
    elif (n.splitting_value != None):
        cmpr_sign = [" <  "," >= "]
        x = ''
        for item in n.children:
            tab += x + str(n.name) + cmpr_sign[n.children.index(item)] + str(n.splitting_value) + "\n" + pre_print(item, indent + 1)
            x = "\t" * indent
        return tab
    else:
        return ''


def text_for_print(n):
    if (n.label != None):
        return "leaf: " + str(n.label)
    elif (n.is_nominal == True):
        return str(n.name)
    elif (n.splitting_value != None):
        return str(n.name) + " < " + str(n.splitting_value)
    else:
        return ' '

def try_print():
    n0 = Node()
    n0.label = 1
    n0.name = "attrib2"
    n1 = Node()
    n1.label = 0
    n1.name = "attrib3"
    n = Node()
    n.label = None
    n.decision_attribute = 1
    n.is_nominal = True
    n.name = "attrib1"
    n.children = {1: n0, 2: n1}
    n.print_dnf_tree()
    return n.print_tree()

def more_print():
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
    n.print_dnf_tree()
    return n.print_tree()

def much_more_print():
    n2 = Node()
    n2.name = "attrib2"
    n2.label = 1

    n3 = Node()
    n3.name = "attrib3"
    n3.label = 0 
    
    n0 = Node()
    n0.name = "attrib0"
    n0.label = 1

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
    n.print_dnf_tree()
    return n.print_tree()

def even_more_print():
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
    n1.label = 7

    
    n = Node()
    n.label = None
    n.decision_attribute = 1
    n.is_nominal = True
    n.name = "attrib"
    n.children = {1: n0, 2: n1}
    n.print_dnf_tree()
    return n.print_tree()

def exceeding_more_print():
    n2 = Node()
    n2.name = "attrib2"
    n2.label = 1

    n3 = Node()
    n3.name = "attrib3"
    n3.label = 0 
    
    n0 = Node()
    n0.name = "attrib0"
    n0.splitting_value = 0.27
    n0.children = (n2, n3)

    n4 = Node()
    n4.name = "attrib4"
    n4.label = 2

    n5 = Node()
    n5.name = "attrib5"
    n5.label = 3
    
    n1 = Node()
    n1.name = "attrib1"
    n1.label = 7

    
    n = Node()
    n.label = None
    n.decision_attribute = 1
    n.is_nominal = True
    n.name = "attrib"
    n.children = {1: n0, 2: n1}
    n.print_dnf_tree()
    return n.print_tree()


