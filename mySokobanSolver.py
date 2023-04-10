
'''

    Sokoban assignment


The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.

No partial marks will be awarded for functions that do not meet the specifications
of the interfaces.

You are NOT allowed to change the defined interfaces.
In other words, you must fully adhere to the specifications of the 
functions, their arguments and returned values.
Changing the interfacce of a function will likely result in a fail 
for the test of your code. This is not negotiable! 

You have to make sure that your code works with the files provided 
(search.py and sokoban.py) as your code will be tested 
with the original copies of these files. 

Last modified by 2022-03-27  by f.maire@qut.edu.au
- clarifiy some comments, rename some functions
  (and hopefully didn't introduce any bug!)

'''

# You have to make sure that your code works with 
# the files provided (search.py and sokoban.py) as your code will be tested 
# with these files
import search 
import sokoban


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
#    return [ (1234567, 'Ada', 'Lovelace'), (1234568, 'Grace', 'Hopper'), (1234569, 'Eva', 'Tardos') ]
    #raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A "taboo cell" is by definition
    a cell inside a warehouse such that whenever a box get pushed on such 
    a cell then the puzzle becomes unsolvable. 
    
    Cells outside the warehouse are not taboo. It is a fail to tag an 
    outside cell as taboo.
    
    When determining the taboo cells, you must ignore all the existing boxes, 
    only consider the walls and the target  cells.  
    Use only the following rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of 
             these cells is a target.
    
    @param warehouse: 
        a Warehouse object with the worker inside the warehouse

    @return
       A string representing the warehouse with only the wall cells marked with 
       a '#' and the taboo cells marked with a 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''
    taboo_cell =""
    #List to store cell for rule 1
    taboo_corner_cell =[]
    #list to store cells for rule 2
    other_taboo =[]
    #list to store targert cells
    target_list =[]
    
    cells = str(warehouse).split('\n')
    x_1 = 0
    for x in cells:
        cells[x_1] = list(x)
        x_1 +=1
    # Codes for rule rule 1 
    # Copy cells into temp by splitting everything    
    temp = cells[:]
    for indx, row in enumerate(cells):
        inside_cell = False
        for cent_indx, char in enumerate(row):
            # turn the goal into a legit spot
            if char == "." or char == '$' or char == '*':
                cells[indx][cent_indx] = " " 
                inside_cell = True
                
            if char == "." or char == "*":
                target_list.append((indx, cent_indx))
            #If a wall is encountered, check if it is within the playing area    
            elif char == '#':
                inside_cell = True
                for index in range(cent_indx):
                    if cells[indx][index] == '#':
                        inside_cell = False
                cells[indx][cent_indx] = char
                
            else:
                # Check if the space is within the cell and if it's in the corner of the warehouse
                if inside_cell == False or indx == 0 or indx == len(cells) - 1 or cent_indx == 0 or cent_indx == len(cells[indx]) - 1:
                    cells[indx][cent_indx] = char
                else:
                    
                    taboo1 = temp[indx][cent_indx - 1] == '#' and temp[indx - 1][cent_indx] == '#' # Checks left top
                    taboo2 = temp[indx][cent_indx + 1] == '#' and temp[indx - 1][cent_indx] == '#' # Checks right top
                    taboo3 = temp[indx][cent_indx - 1] == '#' and temp[indx + 1][cent_indx] == '#' # Checks left bottom
                    taboo4 = temp[indx][cent_indx + 1] == '#' and temp[indx + 1][cent_indx] == '#' # Checks right bottom
                    
                    if taboo1 or taboo2 or taboo3 or taboo4:
                        cells[indx][cent_indx] = 'X'
                        taboo_corner_cell.append((indx, cent_indx))
                    else:
                        cells[indx][cent_indx] = ' '
    
    # Codes to get cells for Rule 2
    taboo_x_y = []
    is_taboo = False
    
    for x in taboo_corner_cell:
        # if a corner taboo cell is in a Top Left Corner
        if cells[x[0]][x[1] - 1] == '#' and cells[x[0] - 1][x[1]] == '#':
            
            y = x[0] + 1
            # get the all the cells below the corner taboo cell untill a wall is encountered
            while cells[y][x[1]] != '#':
                taboo_x_y.append((y, x[1]))
                y = y + 1
            
            if len(taboo_x_y) > 0:
                # Check all the cells are in between two corners
                if taboo_x_y[-1] in taboo_corner_cell:
                    is_taboo = True
                    for z in taboo_x_y:
                        # Check the left side of all the cells, if one is not a wall,
                        # then all cells are not taboo cells
                        if cells[z[0]][z[1]- 1 ] != '#':
                            is_taboo = False
                        
                        # Check if any of the cells is a target, if it is a target.
                        # then all cells are not taboo cells
                        if z in target_list:
                            is_taboo = False
            if is_taboo:
                other_taboo.extend(taboo_x_y)
                is_taboo=False
                
            taboo_x_y =[]
            
            # Check and get the all the cells to the right the corner taboo cell untill a wall is encountered# Check and get the all the cells to the right the corner taboo cell untill a wall is encountered
            count = x[1] +1
            while cells[x[0]][count] != '#':
                taboo_x_y.append((x[0], count))
                count = count+1
                
            if len(taboo_x_y)>0:
                # Check all the cells are in between two corners
                if (taboo_x_y[-1]) in taboo_corner_cell:
                    is_taboo = True
                    for z in taboo_x_y:
        # Check the top side of all the cells, if one of is not a wall,
                     # then all cells are not taboo cells
                        if cells[x[0]-1][z[1]] != '#':
                            is_taboo = False
                        if z in target_list:
                            is_taboo
                        
            if is_taboo:
                other_taboo.extend(taboo_x_y)
                is_taboo=False
                
            taboo_x_y =[]
            
        #the code is similar to the section above expect looking in the Top Right Corner  
        if cells[x[0]][x[1] + 1] == '#' and cells[x[0] - 1][x[1]] == '#':
            
            y = x[0] + 1
            
            while cells[y][x[1]] != '#':
                taboo_x_y.append((y, x[1]))
                y = y + 1
            
            if len(taboo_x_y) > 0:
                if taboo_x_y[-1] in taboo_corner_cell:
                    is_taboo = True
                    for y in taboo_x_y:
                        if cells[z[0]][y[1]+ 1 ] != '#':
                            is_taboo = False
                        
                        if y in target_list:
                            is_taboo = False
            if is_taboo:
                other_taboo.extend(taboo_x_y)
                is_taboo=False
                
            taboo_x_y =[]
            
            count = x[1] -1
            while cells[x[0]][count] != '#':
                taboo_x_y.append((x[0], count))
                count = count-1
                
            if len(taboo_x_y) >0:
                if len(taboo_x_y[-1]) in taboo_corner_cell:
                    is_taboo = True
                    for y in taboo_x_y:
                        if cells[x[0]-1][y[1]] != '#':
                            is_taboo = False
                        if y in target_list:
                            is_taboo = False
                        
            if is_taboo:
                other_taboo.extend(taboo_x_y)
                is_taboo=False
                
            taboo_x_y =[]
        
        #the code is similar to the section above expect looking in the Bottom Left Corner
        if cells[x[0]][x[1] -1] == '#' and cells[x[0] +1][x[1]] == '#':
            
            y = x[0] - 1
            
            while cells[y][x[1]] != '#':
                taboo_x_y.append((y, x[1]))
                y = y - 1
            
            if len(taboo_x_y) > 0:
                
                if taboo_x_y[-1] in taboo_corner_cell:
                    is_taboo = True
                    for z in taboo_x_y:
                        
                        if cells[z[0]][z[1]- 1 ] != '#':
                            is_taboo = False
                        
                        if z in target_list:
                            is_taboo = False
            if is_taboo:
                other_taboo.extend(taboo_x_y)
                is_taboo=False
                
            taboo_x_y =[]
            
            count = x[1] +1
            while cells[x[0]][count] != '#':
                taboo_x_y.append((x[0], count))
                count = count+1
                
            if len(taboo_x_y) >0:
                if len(taboo_x_y[-1]) in taboo_corner_cell:
                    is_taboo = True
                    for y in taboo_x_y:
                        if cells[x[0]+1][y[1]] != '#':
                            is_taboo = False
                        if z in target_list:
                            is_taboo = False
                        
            if is_taboo:
                other_taboo.extend(taboo_x_y)
                is_taboo=False
                
            taboo_x_y =[]
        #the code is similar to the section above expect looking in the Bottom Right Corner
        if cells[x[0]][x[1] +1] == '#' and cells[x[0] +1][x[1]] == '#':
            
            y = x[0] - 1
            
            while cells[y][x[1]] != '#':
                taboo_x_y.append((y, x[1]))
                y = y - 1
            
            if len(taboo_x_y) > 0:
                
                if taboo_x_y[-1] in taboo_corner_cell:
                    is_taboo = True
                    for z in taboo_x_y:
                        
                        if cells[z[0]][z[1]+ 1 ] != '#':
                            is_taboo = False
                        
                        if z in target_list:
                            is_taboo = False
            if is_taboo:
                other_taboo.extend(taboo_x_y)
                is_taboo=False
                
            taboo_x_y =[]
            
            count = x[1] -1
            while cells[x[0]][count] != '#':
                taboo_x_y.append((x[0], count))
                count = count-1
                
            if len(taboo_x_y) >0:
                if len(taboo_x_y[-1]) in taboo_corner_cell:
                    is_taboo = True
                    for y in taboo_x_y:
                        if cells[x[0]+1][y[1]] != '#':
                            is_taboo = False
                        if y in target_list:
                            is_taboo = False
                        
            if is_taboo:
                other_taboo.extend(taboo_x_y)
                is_taboo=False
            taboo_x_y =[]
            
    for x in other_taboo:
        cells[x[0]][x[1]] = "X"
        
    cells = cells[:]
    
    counter = 0
    for row in cells:
        taboo_cell += ''.join(row)
        
        if counter <len(cells) -1: 
            taboo_cell += "\n"
           
        counter = counter+ 1
    
    return taboo_cell  
    #raise NotImplementedError()
#--------------------------------------------------------------------------------------------------------------------------   
 
def box_or_wall(position,state):
    """
    Returns a tuple that contains wether the position is a box or a wall
    """
    is_box = False
    is_wall = False
    for wall in state.walls:
        if position == list(wall):
            is_wall = True
    
    for box in state.boxes:
        if position == list(box):
            is_box = True
    tup = [is_box,is_wall]
    return tup
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    '''
    
    #
    #         "INSERT YOUR CODE HERE"
    #
    #     Revisit the sliding puzzle and the pancake puzzle for inspiration!
    #
    #     Note that you will need to add several functions to 
    #     complete this class. For example, a 'result' method is needed
    #     to satisfy the interface of 'search.Problem'.
    #
    #     You are allowed (and encouraged) to use auxiliary functions and classes

    
    def __init__(self, warehouse):

        self.initial = warehouse.copy()

        #raise NotImplementedError()

#--------------------------------------------------------------------------------------------------------------------------   

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        """

        #Defines the actions of the state as true at the beginning
        up = True
        left = True
        right = True
        down = True

        #Defines the position of the worker
        worker = list(state.worker)

        #Defines the positions next to the worker
        worker_up = [worker[0],worker[1] - 1]
        worker_left = [worker[0] - 1,worker[1]]
        worker_right = [worker[0] + 1,worker[1]]
        worker_down = [worker[0],worker[1] + 1]

        #Defines the positions two steps away from the worker
        worker_up2 = [worker[0],worker[1] - 2]
        worker_left2 = [worker[0] - 2,worker[1]]
        worker_right2 = [worker[0] + 2,worker[1]]
        worker_down2 = [worker[0],worker[1] + 2]


        #Checks the position next to the worker is a wall if the position is a wall that direction is false
        #Checks whether a box next to the worker can be pushed by checking the position next to the box is either a wall or a box
        if box_or_wall(worker_up,state)[1] or (box_or_wall(worker_up,state)[0] and (box_or_wall(worker_up2,state)[0] or box_or_wall(worker_up2,state)[1])):
            up = False
        if box_or_wall(worker_left,state)[1] or (box_or_wall(worker_left,state)[0] and (box_or_wall(worker_left2,state)[0] or box_or_wall(worker_left2,state)[1])):
            left = False
        if box_or_wall(worker_right,state)[1] or (box_or_wall(worker_right,state)[0] and (box_or_wall(worker_right2,state)[0] or box_or_wall(worker_right2,state)[1])):
            right = False
        if box_or_wall(worker_down,state)[1] or (box_or_wall(worker_down,state)[0] and (box_or_wall(worker_down2,state)[0] or box_or_wall(worker_down2,state)[1])):
            down = False

        #returns a boolean for each position in a list representing whether that direction is a valid input
        return[up,down,left,right]
        raise NotImplementedError
    

def check_elem_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Impossible', if one of the action was not valid.
           For example, if the agent tries to push two boxes at the same time,
                        or push a box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    #return string if move is impossible
    impossible_seq = 'Impossible'

    worker_x, worker_y = warehouse.worker

    for action in action_seq:
        if action == 'Up':
            ###print('up')
            #next move after up
            next_x = worker_x
            next_y = worker_y - 1
            if (next_x, next_y) in warehouse.walls:
                return impossible_seq
            elif (next_x, next_y) in warehouse.boxes:
                if (next_x, next_y - 1) not in warehouse.walls and (next_x, next_y) in warehouse.boxes:
                    warehouse.boxes.remove((next_x, next_y))
                    warehouse.boxes.append((next_x, next_y - 1))
                    worker_y = next_y
            else:
                return impossible_seq 
        else:
            worker_y = next_y 
    ###elif action == "Down":



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban(warehouse):
    '''
    This function analyses the given warehouse.
    It returns the two items. The first item is an action sequence solution. 
    The second item is the total cost of this action sequence.
    
    @param 
     warehouse: a valid Warehouse object

    @return
    
        If puzzle cannot be solved 
            return 'Impossible', None
        
        If a solution was found, 
            return S, C 
            where S is a list of actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
            C is the total cost of the action sequence C

    '''
    
    #raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def move_worker(state,action):
    """
    Moves worker and box in a certain direction        
    """

    worker = list(state.worker)

    #Defines the positions next to the worker
    worker_up = [worker[0],worker[1] - 1]
    worker_left = [worker[0] - 1,worker[1]]
    worker_right = [worker[0] + 1,worker[1]]
    worker_down = [worker[0],worker[1] + 1]

    #Defines the positions two steps away from the worker
    worker_up2 = [worker[0],worker[1] - 2]
    worker_left2 = [worker[0] - 2,worker[1]]
    worker_right2 = [worker[0] + 2,worker[1]]
    worker_down2 = [worker[0],worker[1] + 2]



    if action == "Left":
        #Moves Box along with player if box is in the way
        if box_or_wall(worker_left,state)[0]:
            index = state.boxes.index((worker_left[0],worker_left[1]))
            state.boxes[index] = worker_left2

        state.worker = worker_left

    if action == "Right":
        #Moves Box along with player if box is in the way
        if box_or_wall(worker_right,state)[0]:
            index = state.boxes.index((worker_right[0],worker_right[1]))
            state.boxes[index] = worker_right2

        state.worker = worker_right

    if action == "Up":
        #Moves Box along with player if box is in the way
        if box_or_wall(worker_up,state)[0]:
            index = state.boxes.index((worker_up[0],worker_up[1]))
            state.boxes[index] = worker_up2

        state.worker = worker_up
    
    if action == "Down":
        #Moves Box along with player if box is in the way
        if box_or_wall(worker_down,state)[0]:
            index = state.boxes.index((worker_down[0],worker_down[1]))
            state.boxes[index] = worker_down2

        state.worker = worker_down
        

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def remove_taboo_state(state):
    """
    Removes the states where a box is in a taboo_cell
        
    """
    return None

def remove_duplicate_state(duplicate_1,duplicate_2):
    """
    Compares multiple states with the same layout and removes the state that has a longer path
        
    """
    return None

