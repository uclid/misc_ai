'''
Write a program that uses Q-learning algorithm to determine the best path to a goal state.

Similar to the format described in the class, you will work with a 3*4 board. Each of the 12
squares has a unique index. There are four special squares on the board. These four squares 
are: start, donut, forbidden, and wall squares. The remaining eight square are empty ordinary 
squares. The starting square (S) is fixed and always at index 1. The locations of the donut, 
forbidden, and wall squares are determined from the input. An agent has four possible actions 
of going to the north, east, south and west.

Input
The input to your program consists of three numbers, one character, and possibly an additional
number [# # # X (#)]. The first three numbers show the location of the donut, forbidden and
wall squares respectively. Figure 1 shows two possible inputs and the corresponding board
configuration based on each of those inputs. The remaining items in the input, determine the
output format. The fourth item is either character "p" or "q", and if it's "q", there will be an
additional number at the end. Item "p" refers to printing the optimal policy, and "q" refers
to the optimal Q-values.

Strategy
In this problem, the living reward for every action (each step) is r=-0.1. The discount rate is 
"gamma" = 0.5, and learning rate "alpha" = 0.1. The reward for performing the exit action (the only 
availableaction) in the donut square is +100, and for the forbidden square, it's equal to -100. The 
agent cannot enter or pass through the wall square. For the purpose of exploring the board, use an 
epsilon-greedy method with 0.1. This means that with the probability "epsilon", the agent acts 
randomly, and with the probability "1-epsilon", it acts on current policy.

Output
If the input contains "p", your program has to print the best action that should be chosen for
each square or in other words print optimal policy. To do this, in separate lines print: each 
state's index and the action. Here is an example:
Input:
12 8 6 p
Output (possible):
1 '\N{UPWARDS ARROW}'
2 '\N{RIGHTWARDS ARROW}'
3 '\N{UPWARDS ARROW}'
4 '\N{LEFTWARDS ARROW}'
5 '\N{UPWARDS ARROW}'
7 '\N{UPWARDS ARROW}'
9 '\N{RIGHTWARDS ARROW}'
10 '\N{RIGHTWARDS ARROW}'
11 '\N{RIGHTWARDS ARROW}'
If the input contains "q" following a number n, the program has to print the four Q-values
associated with each of the four possible actions in the state that has index n. Here is an
example:
Input:
12 8 6 q 11
Output (possible):
'\N{UPWARDS ARROW}' 0
'\N{RIGHTWARDS ARROW}' 99.23
'\N{LEFTWARDS ARROW}' 90.45
'\N{DOWNWARDS ARROW}' 78.39

'''

import sys, pprint
import random
import time

'''GLOBALS DEFINED BELOW'''

#special states
donut = 0
forbidden = 0
wall = 0

#output parameters
output_type = ''
q_square = 0

#initial grid
grid = [
    #N   E   S   W
    [5,  2,  1,  1],  #1
    [6,  3,  2,  1],  #2
    [7,  4,  3,  2],  #3
    [8,  4,  4,  3],  #4
    [9,  6,  1,  5],  #5
    [10, 7,  2,  5],  #6
    [11, 8,  3,  6],  #7
    [12, 8,  4,  7],  #8
    [9,  10, 5,  9],  #9
    [10, 11, 6,  9],  #10
    [11, 12, 7,  10], #11
    [12, 12, 8,  11]  #12
]

#initial q-values for each state
q_values = [
    #N   E   S   W
    [0,  0,  0,  0], #1
    [0,  0,  0,  0], #2
    [0,  0,  0,  0], #3
    [0,  0,  0,  0], #4
    [0,  0,  0,  0], #5
    [0,  0,  0,  0], #6
    [0,  0,  0,  0], #7
    [0,  0,  0,  0], #8
    [0,  0,  0,  0], #9
    [0,  0,  0,  0], #10
    [0,  0,  0,  0], #11
    [0,  0,  0,  0]  #12
]

'''END OF GLOBALS'''

#function to intialize the grid with special states
def create_grid():
    global donut
    global forbidden
    global wall
    global grid
    
    #all '0' i.e. winning exit actions if donut state
    grid.pop(donut-1)
    grid.insert(donut-1, [0, 0, 0, 0])
    
    #all '-1' i.e. losing exit actions if forbidden state
    grid.pop(forbidden-1)
    grid.insert(forbidden-1, [-1, -1, -1, -1])
    
    #change neighboring states if wall state
    #grid[wall]
    try:
        #change west action for the state right of the wall, except donut and forbidden
        if(wall !=4 and wall !=8 and wall !=12 and (grid[wall][3] !=0 and grid[wall][3] !=-1)):
            grid[wall][3] = (wall+1)
        #change east action for the state left of the wall, except donut and forbidden
        if(wall !=1 and wall !=5 and wall !=9 and (grid[wall-2][1] !=0 and grid[wall-2][1] !=-1)):
            grid[wall-2][1] = (wall-1)
        #change south action for the state above of the wall, except donut and forbidden
        if(wall !=9 and wall !=10 and wall !=11 and wall !=12 and (grid[wall+3][2] !=0 and grid[wall+3][2] !=-1)):
            grid[wall+3][2] = (wall+4) 
        #change north action for the state above of the wall, except donut and forbidden
        if(wall !=1 and wall !=2 and wall !=3 and wall !=4 and (grid[wall-5][0] !=0 and grid[wall-5][0] !=-1)):
            grid[wall-5][0] = (wall-4)
        #pprint.pprint(grid)
    except:
        print("Wall cannot be placed in the specified location!")

def grid_state(i):
        if(i == donut):
            return(str(i) + '(D)\t')
        elif(i == forbidden):
            return(str(i) + '(F)\t')
        elif(i == wall):
            return(str(i) + '(W)\t')
        elif(i == 1):
            return(str(i) + '(S)\t')        
        else:
            return(str(i) + '\t')   

#prints the grid in presentable format
def print_grid():
    print('-------------------------------')
    #row 1
    for i in range(9,13):
        sys.stdout.write(grid_state(i))
    print()
    #row 2
    for i in range(5,9):
        sys.stdout.write(grid_state(i))
    print()
    #row 3
    for i in range(1,5):
        sys.stdout.write(grid_state(i))
    print('\n-------------------------------')

#return the arrow symbol based on direction number
def arrow(next_direction):
    if(next_direction == 2):
        return '\N{DOWNWARDS ARROW}'
    elif(next_direction == 0):
        return '\N{UPWARDS ARROW}'
    elif(next_direction == 1):
        return '\N{RIGHTWARDS ARROW}'
    else:
        return '\N{LEFTWARDS ARROW}'

#check convergence using exit states
def converged():
    #using only exit states since the policy would be optimal when we have
    #reached correct values of reward for exit states upto two decimal places
    if((q_values[donut -1][3] >= 99.995) and (q_values[forbidden -1][3] <= -99.995)):
        return True
    return False

#returns he max q-value of a state
def max_q(q_list):
    #print(q_list)
    return max(q_list)

#returns next state based on epsilon greedy method
def next_move(current_state):
    epsilon = 0.1
    global q_values
    next_state = 0
    next_direction = 0
    
    #gives a random number basde on value of epsilon
    #in this case, it should give am integer between
    #1 and 10. we will assume 1 as the random choice
    #and 2-9 as choice according to policy
    choice = random.randint(1,1/epsilon)
    
    if(choice == 1): #0.1 probability of random choices
        #get next state randomly towards any 4 directions
        random_next = random.randint(0,3)
        next_state = grid[current_state -1][random_next]
        next_direction = random_next
    else: #0.9 probability of acting based on current policy
        #get index of max q_value and map to grid
        max_val = max_q(q_values[current_state -1])
        arg_max = q_values[current_state -1].index(max_val)
        
        next_state = grid[current_state-1][arg_max]
        next_direction = arg_max
    
    return next_state, next_direction

#q learning iterations
def q_learn():
    #q-learning constants
    discount = 0.5
    alpha = 0.1
    global q_values
    
    living_reward = -0.1
    reward_donut = 100
    reward_forbidden = -100
    
    current_state = 1 #start state is 1
    max_iterations = 210000 #run iterations up to 210000 steps max
    reward = 0
    
    print('**Agent Moves. Start => 1**')
    while (max_iterations > 0):
        next_state, next_direction = next_move(current_state)
        #print("Next:" + str(next_state))
        
        #for holding initial part and sample part in the running average
        #of q-values
        part_1 = 0
        part_2 = 0
        
        #REWARD IS +100 AND -100 ONLY WHEN IN EXIT STATES, OTHERWISE LIVING REWWARD
        if(next_state == 0):
            reward = reward_donut
            #calculating q-values for the states based on the formula
            part_1 = float(q_values[current_state -1][next_direction])
            part_2 = reward #there is no next state for exit action
        elif(next_state ==  -1):
            reward = reward_forbidden
            #calculating q-values for the states based on the formula
            part_1 = float(q_values[current_state -1][next_direction])
            part_2 = reward #there is no next state for exit action
        else:
            reward = living_reward
            #calculating q-values for the states based on the formula
            part_1 = float(q_values[current_state -1][next_direction])
            part_2 = reward + (discount * float(max_q(q_values[next_state-1])))            
        
        #printing the move made by the agent
        print('Current:' + str(current_state) + '\tMove Direction:' + str(arrow(next_direction)) + '\tReward:' + str(reward))
        
        #updating the q-value for the relevant state
        q_values[current_state -1][next_direction] = ((1-alpha) * part_1) + (alpha * part_2)
        
        #check convergence to stop learning
        if(converged()):
            print('\nCONVERGED. Values learned in ' + str(210000 - max_iterations) + ' steps!')
            break
        
        #begin from start state after exit action
        if(next_state == 0 or next_state == -1):
            next_state = 1
        
        #next_state now becomes the current state for next iteration
        current_state = next_state
        
        max_iterations -= 1
    
    if(max_iterations <= 0):
        print("\nLEARNING COMPLETE. Max iterations limit surpassed!")    


#the main method
def main():
    global donut
    global forbidden
    global wall
    global output_type
    global q_square
    global q_values
    
    try:
        donut = int(sys.argv[1])
        forbidden = int(sys.argv[2])
        wall = int(sys.argv[3])
        
        #avoid the states to be at zero index
        if(wall <= 0 or forbidden <= 0 or donut <= 0):
            print("Special states cannot be at zero or negative index. Indexes start at 1!")
            exit(1)
            
        #avoid the states to be beyond maximum index
        if(wall > 12 or forbidden >12 or donut >12 ):
            print("Some states beyond grid size. They should be with 1-12!")
            exit(1)        
        
        #avoid special states to be at the same place
        if(wall == forbidden or donut == forbidden or wall == donut):
            print("Special states cannot be at the same index!")
            exit(1)            
    
        output_type = sys.argv[4]
    except:
        print('Not enough input parameters or invalid parameters. Exiting!')
        exit(1)
    
    #create the grid based on user input about special states
    create_grid()
    
    #prints the grid with proper formatting
    print('The agent navigates in the grid shown below')
    print_grid()
    
    #delay to allow user to see the grid
    print('Starts Learning in 3s...')
    time.sleep(3)
    print()

    #learn the q-values
    q_learn()
    
    #pprint.pprint(q_values)
    print('The agent navigated in the grid shown below')
    print_grid()
    
    if output_type == 'p':
        print('Optimal Policy:')
        for index, item in enumerate(q_values):
            max_val = max_q(item)
            arg_max = item.index(max_val)    
            if((index + 1) == wall):
                print(str(index + 1) + " (wall)")
            elif((index + 1) == donut or (index + 1) == forbidden):
                print(str(index + 1) + " (exit)")                
            else:
                print(str(index + 1) + " " + arrow(arg_max))
    elif output_type == 'q':
        try:
            q_square = int(sys.argv[5])
            print('Q-values for the state ' + str(q_square))
            if(q_square == wall):
                print("It's a wall state.")
                print(arrow(0) + " " + ("{0:.2f}".format(q_values[q_square-1][0])))
                print(arrow(1) + " " + ("{0:.2f}".format(q_values[q_square-1][1])))
                print(arrow(2) + " " + ("{0:.2f}".format(q_values[q_square-1][2])))
                print(arrow(3) + " " + ("{0:.2f}".format(q_values[q_square-1][3])))
            elif(q_square == donut or q_square == forbidden):
                print("It's an exit state.")
                print('Q-Value = ' + ("{0:.2f}".format(q_values[q_square-1][0])))         
            else:
                print("It's a regular state.")
                print(arrow(0) + " " + ("{0:.2f}".format(q_values[q_square-1][0])))
                print(arrow(1) + " " + ("{0:.2f}".format(q_values[q_square-1][1])))
                print(arrow(2) + " " + ("{0:.2f}".format(q_values[q_square-1][2])))
                print(arrow(3) + " " + ("{0:.2f}".format(q_values[q_square-1][3])))               
        except:
            print('Missing state index for Q-value. Exiting')
            exit(1)
    else:
        print('Invalid input arguments. Exiting!')
        exit(1)

#runs the main function
if __name__== "__main__":
    main()