'''
Write a program that receives an order of 4 pancakes and gives the best solution that DFS, 
UCS, Greedy and A* search find to go from the start state to the goal (ordered pancakes).

Author: Dixit Bhatta
Date: 09/22/2018
University of Delaware

'''
from queue import PriorityQueue

'''
FEW GLOBALS DEFINED BELOW THAT ALL FUNCTIONS NEED
THEY ARE NOT MODIFIED BY ANY PIECE OF CODE, ONLY FOR READ
'''

'''
possible states the search can be in, basically permutation of 1234
'''
states = [
    ["1234","1243","1324","1342","1423","1432"], #1
    ["2134","2143","2314","2341","2413","2431"], #2
    ["3124","3142","3214","3241","3412","3421"], #3
    ["4123","4132","4213","4231","4312","4321"]  #4
]

'''
the goal state
'''
goal_state = "4321"

'''
Adjacent edge, cost and heuristics from state a to b
considering there are only 2, 3 or 4 pancakes flipped.
#cost: number of pancakes that are flipped
#heuristic: the number of the largest pancake which is still out of place
'''
adjacency_matrix = [
    [[["1243", 2, 4],["1432", 3, 4],["4321", 4, 0]],#1,1
    [["1234", 2, 4],["1342", 3, 4],["3421", 4, 4]], #1,2
    [["1342", 2, 4],["1423", 3, 4],["4231", 4, 3]], #1,3
    [["1324", 2, 4],["1243", 3, 4],["2431", 4, 4]], #1,4
    [["1432", 2, 4],["1324", 3, 4],["3241", 4, 4]], #1,5
    [["1423", 2, 4],["1234", 3, 4],["2341", 4, 4]]],#1,6
    
    [[["2143", 2, 4],["2431", 3, 4],["4312", 4, 2]],#2,1
    [["2134", 2, 4],["2341", 3, 4],["3412", 4, 4]], #2,2
    [["2341", 2, 4],["2413", 3, 4],["4132", 4, 3]], #2,3
    [["2314", 2, 4],["2143", 3, 4],["1432", 4, 4]], #2,4
    [["2431", 2, 4],["2314", 3, 4],["3142", 4, 4]], #2,5
    [["2413", 2, 4],["2134", 3, 4],["1342", 4, 4]]],#2,6
    
    [[["3142", 2, 4],["3421", 3, 4],["4213", 4, 3]],#3,1
    [["3124", 2, 4],["3241", 3, 4],["2413", 4, 4]], #3,2
    [["3241", 2, 4],["3412", 3, 4],["4123", 4, 3]], #3,3
    [["3214", 2, 4],["3142", 3, 4],["1423", 4, 4]], #3,4
    [["3421", 2, 4],["3214", 3, 4],["2143", 4, 4]], #3,5
    [["3412", 2, 4],["3124", 3, 4],["1243", 4, 4]]],#3,6
    
    [[["4132", 2, 3],["4321", 3, 0],["3214", 4, 4]], #4,1
    [["4123", 2, 3],["4231", 3, 3],["2314", 4, 4]], #4,2
    [["4231", 2, 3],["4312", 3, 2],["3124", 4, 4]], #4,3
    [["4213", 2, 3],["4132", 3, 3],["1324", 4, 4]], #4,4
    [["4321", 2, 0],["4213", 3, 3],["2134", 4, 4]], #4,5
    [["4312", 2, 2],["4123", 3, 3],["1234", 4, 4]]] #4,6
]

'''
Class to represent a Node in the search graph
customize to prioritize costs and then tie-break
using the larger of the node values.

Node object has:
   g_cost: actual cost of the node, number of flips
   h_cost: heuristic cost of the node
   state: the string representation of the state eg. '3214'
   prev_state: the parent of the state in the search graph
   algorithm: the algorithm used to calculate overall cost
'''
class Node(object):
    def __init__(self, g_cost, h_cost, state, prev_state, algorithm):
        self.g_cost = g_cost
        self.h_cost = h_cost
        #define overall costs based on the algorithm
        if algorithm == 'a':
            self.cost = self.g_cost + self.h_cost
        elif algorithm == 'u':
            self.cost = self.g_cost
        elif algorithm == 'g':
            self.cost = self.h_cost
        else:
            self.cost = 0        
        self.state = state
        self.prev_state = prev_state
    def __lt__(self, other):
        #for priority queue, first compare the costs, min first
        #next tie-break using value of the state, max first
        if self.cost < other.cost:
            return True
        elif self.cost == other.cost:
            return self.state > other.state
        return False
    def __contains__(self, x):
        return x in self.state
    def __repr__(self):
        return "(" + str(self.cost) + "," + str(self.g_cost) + "," + str(self.h_cost) + "," + str(self.state) + "," + str(self.prev_state) + ")"

'''
params: any arbitrary state
returns: the indices of the item in the list of states
'''
def get_state_index(state):
    x=0
    y=0
    for i in range(len(states)):
        nested_tuple = states[i]
        for j in range(len(nested_tuple)):
            string = states[i][j]
            if string.find(state) != -1:
                x, y = i,j    
    return (x,y)

'''
params: any arbitrary state
returns: the heuristics of an arbitrary state
'''
def get_state_heuristic(state):
    h = 0
    for i in range(len(adjacency_matrix)):
        nested_tuple = adjacency_matrix[i]
        for j in range(len(nested_tuple)):
            nested_tuple2 = nested_tuple[j]
            for k in range(len(nested_tuple2)):
                string = nested_tuple2[k][0]
                if string.find(state) != -1:
                    h = nested_tuple2[k][2] 
    return h

'''
params: any arbitrary state
returns: a list of children of a state
'''
def get_children(state):
    x,y = get_state_index(state)
    return (adjacency_matrix[x][y])

'''
params: an expanded or child state
returns cost of an expanded state
'''
def get_child_cost(child_state):
    return(child_state[1])

'''
params: an expanded or child state
returns: heuristic cost of the expanded state
'''
def get_child_heuristic(child_state):
    return(child_state[2])

'''
params: an expanded or child state
returns: state value of an expanded state
'''
def get_child_value(child_state):
    return(child_state[0])

'''
params: a state value and the fringe
returns: boolean, check if a value is already in the fringe
'''
def is_in_queue(x, fringe):
    with fringe.mutex:
        tuple_check = [item for item in fringe.queue if x in item]
        if len(tuple_check) == 0:
            return False
        return True

'''
params: a state value and the fringe    
returns: a list of same states (different costs)
         if they already exist in the queue
'''
def replace_in_queue(x, fringe):
    with fringe.mutex:
        tuple_check = [item for item in fringe.queue if x in item]
        return tuple_check

'''
params: a state
returns: boolean, check for goal state
'''
def goal(state):
    if state == goal_state:
        return True
    return False

'''
Function to insert the flip
character in a state
'''
def insert_flip(state,flips):
    index = 4-flips
    new_state = state[:index] + '|' + state[index:]
    return new_state

'''
Function for DFS
'''
def dfs_next(start_state):
    explored = set() # a set of already explored nodes
    
    #the start node with all zero costs, DFS does not consider costs
    node = (Node(0, 'x', start_state, None, 'd'))
    stack = [node] #fringe is a stack, I have simply called it stack
    
    path =[] #path is initially empty
    
    #until stack is not empty
    while stack:
        #print(stack)
        node = stack.pop() #remove item from stack
        #add any unexplored node popped from stack into the path
        if node not in explored:
            #print(node)
            explored.add(node.state)
            path.append(node)
            #print(explored)
            
            #return path as soon as the goal is found
            if goal(node.state):
                print("Goal Found!!")
                return path
            
            #get the children of a node and add them to stack if they are not already explored
            children = get_children(node.state)
            #sorted such that it always takes max available element in next depth-level
            sorted_children = sorted(children, key = get_child_value)
            for child in sorted_children:
                #use the previous cost and add to child
                #only to show path cost, this algorithm ignores all costs
                if node.prev_state:
                    prev_cost = node.g_cost
                else:
                    prev_cost = 0
                
                child_node = Node(get_child_cost(child) + prev_cost, 'x', get_child_value(child), node, 'd')
                if child_node.state not in explored:
                    stack.append(child_node)

'''
Function for UCS
'''
def ucs_next(start_state):
    #start node with g(n) = 0
    #we assume h(n) = 0 all throughout the function
    #since UCS ignores h(n)
    node = (Node(0, 'x', start_state, None, 'u'))
    
    fringe = PriorityQueue() #fringe is a priority queue
    fringe.put(node)
    
    explored = [] #tracks explored nodes
    path = [] #the path to the goal
    
    while True: #continue until path up to goal is returned
        if (fringe.empty()):
            return ["No goal found"]
        #print(fringe.queue)
        
        node = fringe.get() #get the lowest cost item
        
        #print(node.state)
        if goal(node.state):
            path.append(node)
            print("Goal Found!!")
            return path
        
        path.append(node)
        explored.append(node.state)
        
        #get the children of a node
        children = get_children(node.state)
        
        for child in children:
            #use the previous cost and add to child
            if node.prev_state:
                prev_cost = node.cost
            else:
                prev_cost = 0
            
            #creating the child node to be added to the queue/fringe
            child_node = Node(get_child_cost(child) + prev_cost, 'x', get_child_value(child), node, 'u')
            
            if (child_node.state not in explored) and (not (is_in_queue(child_node.state, fringe))):
                fringe.put(child_node)
            elif is_in_queue(child_node.state, fringe):
                #if the same node is found to have smaller cost
                #remove the first one and keep the one with smaller cost
                #which is the same as changig the cost
                other_nodes = replace_in_queue(child_node.state, fringe)
                for item in other_nodes:
                    if child_node.cost < item.cost:
                        item.cost = child_node.cost

'''
Function for Greedy
'''
def greedy_next(start_state):
    node = (Node(0, get_state_heuristic(start_state), start_state, None, 'g'))
    
    fringe = PriorityQueue()
    fringe.put(node)
    
    explored = [] #tracks explored nodes
    path = [] #the path to the goal
    
    while True: #continue until path up to goal is returned
        if (fringe.empty()):
            return ["No goal found"]
        #print(fringe.queue)
        
        node = fringe.get() #get the lowest cost item
        
        #print(node.state)
        if goal(node.state):
            path.append(node)
            print("Goal Found!!")
            return path
        
        path.append(node)
        explored.append(node.state)
        
        #get the children of a node
        children = get_children(node.state)
        
        for child in children:
            #use the previous cost and add to child, only for showing
            #this algorithm does not use this cost for evaluation
            if node.prev_state:
                prev_cost = node.g_cost
            else:
                prev_cost = 0
                
            #adding actual and heuristic cost; actual cost is only kept to track the flips for each step
            child_node = Node(get_child_cost(child) + prev_cost, get_child_heuristic(child), get_child_value(child), node, 'g')
            
            if (child_node.state not in explored) and (not (is_in_queue(child_node.state, fringe))):
                fringe.put(child_node)
            elif is_in_queue(child_node.state, fringe):
                #if the same node is found to have smaller cost
                #remove the first one and keep the one with smaller cost
                #which is the same as changig the cost
                other_nodes = replace_in_queue(child_node.state, fringe)
                for item in other_nodes:
                    if child_node.cost < item.cost:
                        item.cost = child_node.cost

'''
Function for A*
'''
def a_star_next(start_state):
    node = (Node(0, get_state_heuristic(start_state), start_state, None, 'a'))
    
    fringe = PriorityQueue()
    fringe.put(node)
    
    explored = [] #tracks explored nodes
    path = [] #the path to the goal
    
    while True: #continue until path up to goal is returned
        if (fringe.empty()):
            return ["No goal found"]
        #print(fringe.queue)
        node = fringe.get() #get the lowest cost item
        #print(node.state)
        
        if goal(node.state):
            path.append(node)
            print("Goal Found!!")
            return path
        
        path.append(node)
        explored.append(node.state)
        
        #get the children of a node
        children = get_children(node.state)
        
        for child in children:
            #use the previous cost and add to child, only g(n)
            if node.prev_state:
                prev_cost = node.g_cost
            else:
                prev_cost = 0    
            
            #creating the child node to be added to the fringe
            child_node = Node(get_child_cost(child) + prev_cost, get_child_heuristic(child), get_child_value(child), node, 'a')
            
            if (child_node.state not in explored) and (not (is_in_queue(child_node.state, fringe))):
                fringe.put(child_node)
            elif is_in_queue(child_node.state, fringe):
                #if the same node is found to have smaller cost
                #remove the first one and keep the one with smaller cost
                #which is the same as changig the cost
                other_nodes = replace_in_queue(child_node.state, fringe)
                for item in other_nodes:
                    if child_node.cost < item.cost:
                        item.cost = child_node.cost

'''
Display the path using the result
'''
def display_path(result):
    list_path = []
    state = ""
    diff = result.g_cost
    
    #add states backward from goal to initial for full path
    while result.prev_state:
        #insert flips except for the final state
        if goal(result.state):
            state = result.state
        else:
            state = insert_flip(result.state, diff)
        list_path.append(state + "\tg=" + str(result.g_cost) + "\th=" + str(result.h_cost))
        diff = result.g_cost - result.prev_state.g_cost
        result = result.prev_state
    
    #add the initial state
    #insert flips except for the final state
    if goal(result.state):
        state = result.state
    else:
        state = insert_flip(result.state, diff)    
    list_path.append(state + "\tg=" + str(result.g_cost) + "\th=" + str(result.h_cost))
    
    while list_path:
        #pop (LIFO) to print paths from start to goal
        print(list_path.pop())

'''
Main function
'''
def main():
    print("Solve the Pancake Problem!")
    print("Enter your Pancake ordering and algorithm choice.")
    print("Input format: ####X.\nUse 'd' for DFS 'u' for UCS 'g' for Greedy and 'a' for A*")
    print("Example: 3412g means bottom pancake of size 3 and greedy algorithm") 
    my_input = input("=>")
    
    if ('1' not in my_input) or ('2' not in my_input) or ('3' not in my_input) or ('4' not in my_input):
        print("Not a valid state!\nRestart")
        exit(1)
    
    if ('a' not in my_input) and ('d' not in my_input) and ('g' not in my_input) and ('u' not in my_input):
        print("Not a valid algorithm!\nRestart")
        exit(1)    
    
    #get the algorithm and pancake ordering
    start_state = my_input[:4] #first 4 items
    algorithm = my_input[-1] #last item i.e. algorithm
    #print(start_state)
    
    
    if algorithm == 'a':
        results = a_star_next(start_state)
        print("\nAlgorithm: A*")
    elif algorithm == 'u':
        results = ucs_next(start_state)
        print("\nAlgorithm: UCS")
    elif algorithm == 'g':
        print("\nAlgorithm: Greedy")
        results = greedy_next(start_state)
    else:
        print("\nAlgorithm: DFS")
        results = dfs_next(start_state)
    
    print("PATH:")
    #last item in the results list is the solution path
    display_path(results[-1])


'''
Running the main function
'''
if __name__== "__main__":
    main()