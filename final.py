"""
@author: Danny Kim
"""

import math
import copy

class Node:
    def __init__(self, grid, parent, action, depth, fn):
        self.grid = grid
        self.parent = parent
        self.action = action
        self.depth = depth
        self.children = []
        self.fn = fn

#get position of blank(0) 
def position(state):
    position = [0,0]
    for i in range(len(state)):
        for j in range(len(state)):
            if state[i][j] == 0:
                position[0]= [i, j]
    return position

#find position of num
def find_index(state, num):
    for i in range(len(state)):
       for j in range(len(state)):
            if state[i][j] == num:
               return i, j

#calculate h(n) value
def calc_hn(curr_state, goal_state, depth):
    hn = 0
    for i in range(len(curr_state)):
        for j in range(len(curr_state)):
            goal_index = find_index(goal_state, curr_state[i][j])
            if curr_state[i][j] != 0:
                distance = abs(i - goal_index[0]) + abs(j - goal_index[1]) 
                hn += distance
    return hn + depth

#return new_state according to action
def move(action, node, blank_pos, new_state, blank):
    if action == 'U': #up
        if blank_pos[0] - 1 >= 0:
            num = new_state[blank_pos[0] - 1][blank_pos[1]]
            new_state[blank_pos[0]-1][blank_pos[1]] = blank
            new_state[blank_pos[0]][blank_pos[1]] = num
            
    elif action == 'D': #down
        if blank_pos[0] + 1 <= 3:
            num = new_state[blank_pos[0] + 1][blank_pos[1]]
            new_state[blank_pos[0]+1][blank_pos[1]] = blank
            new_state[blank_pos[0]][blank_pos[1]] = num
            
    elif action == 'L': #left
        if blank_pos[1] - 1 >= 0:
            num = new_state[blank_pos[0]][blank_pos[1] - 1]
            new_state[blank_pos[0]][blank_pos[1]-1] = blank
            new_state[blank_pos[0]][blank_pos[1]] = num
            
    elif action == 'R': #right
        if blank_pos[1] + 1 <= 3:
           
            num = new_state[blank_pos[0]][blank_pos[1] + 1]
            new_state[blank_pos[0]][blank_pos[1]+1] = blank
            new_state[blank_pos[0]][blank_pos[1]] = num   
            
    return new_state


#update states of children
def find_states(blank, node):
    actions = ['U','D','L','R']
    state = []
    node_state = node.grid
    blank_x = blank[0][0]
    blank_y = blank[0][1]

    #copy
    for action in actions:
        new_state = []
        for row in node_state:
            new_state.append(row[:])
        new_state = move(action, node, (blank_x, blank_y), new_state, 0) 
        state.append([new_state, action])
        
    return state

#check if goal function
def goal(node_state, goal_state):
    curr_state = []
    for row in node_state:
        curr_state.append(row[:])
    for i in range(len(node_state)):
        for j in range(len(node_state[i])):
            if (node_state[i][j] == 0): 
                curr_state[i][j] = 0
    return curr_state == goal_state


def main():
    #enter input filename
    print("Please enter the name of the input file:")
    file_name = input()

    #enter output filename
    print("Please enter the name of the output file:")
    outputFileName = input()
    outFile = open(outputFileName, "w")
    
    with open(file_name) as f:
        puzzle = f.readlines()

    #get rid of \n spaces
    for i in range(len(puzzle)):
        puzzle[i] = puzzle[i].strip() 

    #create puzzles of initial and goal states
    div = 0
    initial_state = []
    goal_state = []
    for line in puzzle:
        row = line.split(' ')

        if line == '': 
            div = 1
            continue
        
        if div:
            for i in range(len(row)):
                row[i] = int(row[i])
            goal_state.append(row)
            
        else:
            for i in range(len(row)):
                row[i] = int(row[i])
            initial_state.append(row)

    manhattan = calc_hn(initial_state, goal_state, 0)
    initial = Node(initial_state, 0, 0, 0, manhattan)
    

    #create explored and unexplored nodes
    explored = []
    unexplored = []
    depth = 0
    counter= 0
    unexplored.append(initial)

    while len(unexplored) != 0:

        #find node with lowest fn
        index = 0
        node = unexplored[0]
        counter += 1
        count = 0
        explored.append(node.grid)
        
        for i in unexplored:
            if i.fn < node.fn:
                index = count
                node = i 
            count += 1


        #swap fn values
        unexplored[index], unexplored[-1] = unexplored[-1], unexplored[index]
        
        #pop node
        node = unexplored.pop()
        
        # get index of blank states
        blank_pos = position(node.grid)
        blank = blank_pos[0]
        children = find_states(blank_pos, node)
       
        #map each node
        for i in children:
            if i[0] not in explored:
                num = 0
                for j in unexplored:
                    if j.grid == i[0]:
                        num = 1
                        break
                if not num:
                    fn = calc_hn(i[0], goal_state, node.depth+1)
                    unexplored.append(Node(i[0], node, i[1], node.depth+1, fn))


        #check if curr_state = goal_state
        final = goal(node.grid, goal_state)
        if final:
            nodes = node
            action = []
            manhattan = []
            
            while nodes.parent != 0:
                action.append(nodes.action)
                manhattan.append(nodes.fn)
                nodes = nodes.parent
            manhattan.append(nodes.fn)

            #print initial and goal states
            for i in initial_state:
                row = ''
                for j in i:
                    row += str(j) + ' '
                print(row)
                outFile.writelines(row+'\n')

            outFile.writelines('\n')
            print('\n')
    
            for i in goal_state:
                row = ''
                for j in i:
                    row += str(j) + ' '
                print(row)
                outFile.writelines(row+'\n')
    
            outFile.writelines('\n')
            print('\n')

    
            #depth of tree
            print(node.depth)
            outFile.writelines(str(node.depth)+'\n')
            
            #total number of nodes in tree
            print(counter)
            outFile.writelines(str(counter)+'\n')

            #actions
            row = ''
            for i in action[::-1]:
                row += str(i) + ' '
            print(row)
            outFile.writelines(row+'\n')

            #f(n) values
            row = ''
            for i in manhattan[::-1]:
                row += str(i) + ' '
            print(row)
            outFile.writelines(row)

            break
        

if __name__ == "__main__":
    main()
