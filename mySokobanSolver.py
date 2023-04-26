
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
# stores list of x,y values for taboo locations in warehouse
taboo_location=[]

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
    cell_to_remove = ['$', '@']
    target_cell = ['.', '!', '*']
    wall_cell = '#'
    taboo_cell = 'X'
    
    
    cells = str(warehouse)
    for char in cell_to_remove:
        cells = cells.replace(char, ' ')
    cells = cells.split('\n')
    cells = list(zip(*cells))  

    
    #List to store cell for rule 1
    
    x_1 = 0
    for x in cells:
        cells[x_1] = list(x)
        
        x_1 +=1
    
    

    def corner_cell(warehouse, x, y, wall=0):
        """
    Check whether cell has one wall above or below it and if wall is left or right of it
    Returns 
    @param
    warehouse: a warehouse object representing the current state of the warehouse
    x: x position of wall in warehouse
    y: y position of wall in warehouse
    wall: to decide what should be returned
    @return
    Returns boolean of walls above and below, left and right, or both.
        
        """
        up_down = 0
        left_right = 0
        # check for walls above and below
        for (dx, dy) in [(0, 1), (0, -1)]:
            if warehouse[y + dy][x + dx] == wall_cell:
                up_down += 1
        # check for walls left and right
        for (dx, dy) in [(1, 0), (-1, 0)]:
            if warehouse[y + dy][x + dx] == wall_cell:
                left_right += 1
        if wall:
            return (up_down >= 1) or (left_right >= 1)
        else:
            return (up_down >= 1) and (left_right >= 1)
   

    
    # rule 1
    for y in range(len(cells) - 1):
        inside_cell = False
        for x in range(len(cells[0]) - 1):
            if cells[y][x] == '$':
                print(y,x)
            # iretate through row in warehouse until wthe first wall is discovered
            if not inside_cell:
                if cells[y][x] == wall_cell:
                    inside_cell = True
            else:
                #see if all the walls to to the right of current is empty
                
                if all([char == ' ' for char in cells[y][x:]]):
                    break
                if cells[y][x] not in target_cell:
                    
                    if cells[y][x] != wall_cell:
                        if corner_cell(cells, x, y):
                            cells[y][x] = taboo_cell
                            taboo_location.append((y, x))

    # apply rule 2
    for y in range(1, len(cells) - 1):
        for x in range(1, len(cells[0]) - 1):
            if cells[y][x] == taboo_cell and corner_cell(cells, x, y):
                row = cells[y][x + 1:]
                col = [row[x] for row in cells[y + 1:][:]]
                # fill in taboo_cells in row to the right of cell where taboo is 
                for x2 in range(len(row)):
                    if row[x2] in target_cell or row[x2] == wall_cell:
                        break
                    if row[x2] == taboo_cell and corner_cell(cells, x2 + x + 1, y):
                        if all([corner_cell(cells, x3, y, 1)
                                for x3 in range(x + 1, x2 + x + 1)]):
                            for x4 in range(x + 1, x2 + x + 1):
                                cells[y][x4] = 'X'
                                taboo_location.append((y, x4))
                # fill in taboo_cells in column going down from where taboo is 
               
                for y2 in range(len(col)):
                    if col[y2] in target_cell or col[y2] == wall_cell:
                        break
                    if col[y2] == taboo_cell and corner_cell(cells, x, y2 + y + 1):
                        if all([corner_cell(cells, x, y3, 1)
                                for y3 in range(y + 1, y2 + y + 1)]):
                            for y4 in range(y + 1, y2 + y + 1):
                                cells[y4][x] = 'X'
                                taboo_location.append((y4, x))

    # change the array back into a string
    cells_copy = ""
    cells = cells[:]
    
    cells = list(zip(*cells))  

    
    
    counter = 0
    for row in cells:
        cells_copy += ''.join(row)
        
        if counter <len(cells) -1: 
            cells_copy += "\n"
           
        counter = counter+ 1
    
    

    # remove the remaining target_squares
    for char in target_cell:
        cells_copy = cells_copy.replace(char, ' ')
    return cells_copy
    #raise NotImplementedError()

def find_taboo(warehouse):
    cell_to_remove = ['$', '@']
    target_cell = ['.', '!', '*']
    wall_cell = '#'
    taboo_cell = 'X'
    taboo_locations = []
    
    cells = str(warehouse)
    for char in cell_to_remove:
        cells = cells.replace(char, ' ')
    cells = cells.split('\n')
    cells = list(zip(*cells))  

    
    #List to store cell for rule 1
    
    x_1 = 0
    for x in cells:
        cells[x_1] = list(x)
        
        x_1 +=1
    
    

    def corner_cell(warehouse, x, y, wall=0):
        """
    Check whether cell has one wall above or below it and if wall is left or right of it
    Returns 
    @param
    warehouse: a warehouse object representing the current state of the warehouse
    x: x position of wall in warehouse
    y: y position of wall in warehouse
    wall: to decide what should be returned
    @return
    Returns boolean of walls above and below, left and right, or both.
        
        """
        up_down = 0
        left_right = 0
        # check for walls above and below
        for (dx, dy) in [(0, 1), (0, -1)]:
            if warehouse[y + dy][x + dx] == wall_cell:
                up_down += 1
        # check for walls left and right
        for (dx, dy) in [(1, 0), (-1, 0)]:
            if warehouse[y + dy][x + dx] == wall_cell:
                left_right += 1
        if wall:
            return (up_down >= 1) or (left_right >= 1)
        else:
            return (up_down >= 1) and (left_right >= 1)
   

    
    # rule 1
    for y in range(len(cells) - 1):
        inside_cell = False
        for x in range(len(cells[0]) - 1):
            if cells[y][x] == '$':
                print(y,x)
            # iretate through row in warehouse until wthe first wall is discovered
            if not inside_cell:
                if cells[y][x] == wall_cell:
                    inside_cell = True
            else:
                #see if all the walls to to the right of current is empty
                
                if all([char == ' ' for char in cells[y][x:]]):
                    break
                if cells[y][x] not in target_cell:
                    
                    if cells[y][x] != wall_cell:
                        if corner_cell(cells, x, y):
                            cells[y][x] = taboo_cell
                            taboo_locations.append((y, x))

    # apply rule 2
    for y in range(1, len(cells) - 1):
        for x in range(1, len(cells[0]) - 1):
            if cells[y][x] == taboo_cell and corner_cell(cells, x, y):
                row = cells[y][x + 1:]
                col = [row[x] for row in cells[y + 1:][:]]
                # fill in taboo_cells in row to the right of cell where taboo is 
                for x2 in range(len(row)):
                    if row[x2] in target_cell or row[x2] == wall_cell:
                        break
                    if row[x2] == taboo_cell and corner_cell(cells, x2 + x + 1, y):
                        if all([corner_cell(cells, x3, y, 1)
                                for x3 in range(x + 1, x2 + x + 1)]):
                            for x4 in range(x + 1, x2 + x + 1):
                                cells[y][x4] = 'X'
                                taboo_locations.append((y, x4))
                # fill in taboo_cells in column going down from where taboo is 
               
                for y2 in range(len(col)):
                    if col[y2] in target_cell or col[y2] == wall_cell:
                        break
                    if col[y2] == taboo_cell and corner_cell(cells, x, y2 + y + 1):
                        if all([corner_cell(cells, x, y3, 1)
                                for y3 in range(y + 1, y2 + y + 1)]):
                            for y4 in range(y + 1, y2 + y + 1):
                                cells[y4][x] = 'X'
                                taboo_locations.append((y4, x))
    return taboo_locations
#--------------------------------------------------------------------------------------------------------------------------   
 
def box_or_wall(position,state):
    """
    Returns a tuple that contains wether the position is a box or a wall

    @param
    position: a tuple representing the position on the grid
    state: a State object representing the current state of the warehouse

    @return
    Returns a tuple of two Boolean values. The first value is True if the given position is a box, False otherwise.
    The second value is True if the given position is a wall, False otherwise.
    
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

        # represents the initial state of the warehouse
        self.initial = warehouse
        # represents the states that have not been expanded
        self.unexpanded_states = []
        self.unexpanded_actionSequences = []
        self.unexpanded_weights = []
        # represents the states that have been expanded
        self.expanded_actionSequences = []
        self.expanded_actionSequences.append([])
        self.expanded_weights = []
        self.expanded_weights.append(0)
        self.expanded_states = []
        self.expanded_states.append(self.initial)
        self.goal = warehouse.targets
        # represents the current state being expanded
        self.current = warehouse
        actions = self.actions(self.initial)

        # represents the heuristic values of the unexpanded states
        self.hueristic = []

        worker = warehouse.worker
        #Defines the positions next to the worker
        worker_up = [worker[0],worker[1] - 1]
        worker_left = [worker[0] - 1,worker[1]]
        worker_right = [worker[0] + 1,worker[1]]
        worker_down = [worker[0],worker[1] + 1]

        self.taboo = find_taboo(warehouse)

        #expand initial nodes and add nodes to the unexpanded states list
        for action in actions:
            weight = 1
            if action == "Left":
                try:
                    index = self.initial.boxes.index((worker_left[0],worker_left[1]))
                    weight = self.initial.weights[index] + 1
                    self.unexpanded_weights.append(weight)
                except:
                    self.unexpanded_weights.append(weight)
            
            if action == "Right":
                try:
                    index = self.initial.boxes.index((worker_right[0],worker_right[1]))
                    weight = self.initial.weights[index] + 1
                    self.unexpanded_weights.append(weight)
                except:
                    self.unexpanded_weights.append(weight)
            
            if action == "Up":
                try:
                    index = self.initial.boxes.index((worker_up[0],worker_up[1]))
                    weight = self.initial.weights[index] + 1
                    self.unexpanded_weights.append(weight)
                except:
                    self.unexpanded_weights.append(weight)

            if action == "Down":
                try:
                    index = self.initial.boxes.index((worker_down[0],worker_down[1]))
                    weight = self.initial.weights[index] + 1
                    self.unexpanded_weights.append(weight)
                except:
                    self.unexpanded_weights.append(weight)


            # Creates a copy of the warehouse and then moves the worker and adds that to the unexpanded states list
            warehouse_copy = deep_copy(self.initial)
            move_worker(warehouse_copy,action)
            self.unexpanded_states.append(warehouse_copy)

            # adds the initial sequence as blank
            sequence = []
            sequence.append(action)
            self.unexpanded_actionSequences.append(sequence)

            # adds the initial heuristic value
            h = hueristic_distance(warehouse_copy.boxes,self.goal,self.initial.weights) + weight
            self.hueristic.append(h)
            
            
            





        #raise NotImplementedError()

#--------------------------------------------------------------------------------------------------------------------------   

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        """


        actions = ["Up","Left","Right","Down"]
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
            actions.remove("Up")
        if box_or_wall(worker_left,state)[1] or (box_or_wall(worker_left,state)[0] and (box_or_wall(worker_left2,state)[0] or box_or_wall(worker_left2,state)[1])):
            actions.remove("Left")
        if box_or_wall(worker_right,state)[1] or (box_or_wall(worker_right,state)[0] and (box_or_wall(worker_right2,state)[0] or box_or_wall(worker_right2,state)[1])):
            actions.remove("Right")
        if box_or_wall(worker_down,state)[1] or (box_or_wall(worker_down,state)[0] and (box_or_wall(worker_down2,state)[0] or box_or_wall(worker_down2,state)[1])):
            actions.remove("Down")

        #returns a boolean for each position in a list representing whether that direction is a valid input
        return actions
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

    #check if each move in the action sequence is valid 
    for action in action_seq:
        if action == 'Up':
            #next move after up
            next_x = worker_x
            next_y = worker_y - 1
            if (next_x, next_y) in warehouse.walls:
                return impossible_seq
            elif (next_x, next_y) in warehouse.boxes:
                if (next_x, next_y - 1) not in warehouse.walls and (next_x, next_y) in warehouse.boxes:
                    #the move is possible
                    warehouse.boxes.remove((next_x, next_y))
                    warehouse.boxes.append((next_x, next_y - 1))
                    move_worker(warehouse, "Up")
                else:
                    #if move is impossible
                    return impossible_seq 
            else:
                move_worker(warehouse, "Up") 
        elif action == 'Down':
            next_x = worker_x
            next_y = worker_y + 1
            if (next_x, next_y) in warehouse.walls:
                return impossible_seq
            elif (next_x, next_y) in warehouse.boxes: 
                if (next_x, next_y + 1) not in warehouse.walls and (next_x, next_y) in warehouse.boxes:
                    warehouse.boxes.remove((next_x, next_y))
                    warehouse.boxes.append((next_x, next_y + 1))
                    move_worker(warehouse, "Down")
                else:
                    return impossible_seq
            else:
                move_worker(warehouse, "Down")
        elif action == 'Left':
            next_x = worker_x - 1
            next_y = worker_y
            if(next_x, next_y) in warehouse.walls:
                return impossible_seq
            elif (next_x, next_y) in warehouse.boxes:
                if(next_x - 1, next_y) not in warehouse.walls and (next_x, next_y) in warehouse.boxes:
                    warehouse.boxes.remove((next_x, next_y))
                    warehouse.boxes.append((next_x - 1, next_y))
                    move_worker(warehouse, "Left")
                else:
                    return impossible_seq
            else:
                move_worker(warehouse, "Left")
        elif action == 'Right':
            next_x = worker_x + 1
            next_y = worker_y
            if(next_x, next_y) in warehouse.walls:
                return impossible_seq
            elif (next_x, next_y) in warehouse.boxes:
                if(next_x + 1, next_y) not in warehouse.walls and (next_x, next_y) in warehouse.boxes:
                    warehouse.boxes.remove((next_x, next_y))
                    warehouse.boxes.append((next_x + 1, next_y))
                    move_worker(warehouse, "Right")
                else:
                    return impossible_seq
            else:
                move_worker(warehouse, "Right")

    #return a string representing the state of the puzzle
    return warehouse.__str__()



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
    solver = SokobanPuzzle(warehouse)
    while set(solver.current.boxes) != set(solver.goal) and solver.unexpanded_states:
        # Find lowest heuristic value
        min_h = min(solver.hueristic)
        index = solver.hueristic.index(min_h)
        # Checks if that state is either a duplicate state or a state that has a box in a taboo state
        if(not Is_duplicate_state(solver.expanded_states,solver.unexpanded_states[index]) and remove_taboo_state(solver.unexpanded_states[index],solver.taboo)):
            solver.current = solver.unexpanded_states[index]
        
        # removes that state from the unexpanded list
        else:
            del solver.unexpanded_states[index]
            del solver.unexpanded_actionSequences[index]
            del solver.unexpanded_weights[index]
            del solver.hueristic[index]
            continue

        worker = solver.current.worker
        #Defines the positions next to the worker
        worker_up = [worker[0],worker[1] - 1]
        worker_left = [worker[0] - 1,worker[1]]
        worker_right = [worker[0] + 1,worker[1]]
        worker_down = [worker[0],worker[1] + 1]

        actions = solver.actions(solver.current)

        #expand initial nodes and add nodes to the unexpanded states list
        for action in actions:
            if action == "Left":
                # tries to index the box if position is box then sets weight
                try:
                    box_index = solver.current.boxes.index((worker_left[0],worker_left[1]))
                    weight = solver.current.weights[box_index] + 1 + solver.unexpanded_weights[index]
                    solver.unexpanded_weights.append(weight)

                # sets weight when the position does not have a box
                except:
                    weight = 1 + solver.unexpanded_weights[index] 
                    solver.unexpanded_weights.append(weight)
            
            if action == "Right":
                # tries to index the box if position is box then sets weight
                try:
                    box_index = solver.current.boxes.index((worker_right[0],worker_right[1]))
                    weight = solver.current.weights[box_index] + 1 + solver.unexpanded_weights[index]
                    solver.unexpanded_weights.append(weight)

                # sets weight when the position does not have a box
                except:
                    weight = 1 + solver.unexpanded_weights[index] 
                    solver.unexpanded_weights.append(weight)

            if action == "Up":
                # tries to index the box if position is box then sets weight
                try:
                    box_index = solver.current.boxes.index((worker_up[0],worker_up[1]))
                    weight = solver.current.weights[box_index] + 1 + solver.unexpanded_weights[index]
                    solver.unexpanded_weights.append(weight)
                
                # sets weight when the position does not have a box
                except:
                    weight = 1 + solver.unexpanded_weights[index] 
                    solver.unexpanded_weights.append(weight)

            if action == "Down":
                # tries to index the box if position is box then sets weight
                try:
                    box_index = solver.current.boxes.index((worker_down[0],worker_down[1]))
                    weight = solver.current.weights[box_index] + 1 + solver.unexpanded_weights[index]
                    solver.unexpanded_weights.append(weight)
                
                # sets weight when the position does not have a box
                except:
                    weight = 1 + solver.unexpanded_weights[index] 
                    solver.unexpanded_weights.append(weight)

            # Creates a copy of the warehouse and then moves the worker and adds that to the unexpanded states list
            warehouse_copy = deep_copy(solver.current)
            move_worker(warehouse_copy,action)
            solver.unexpanded_states.append(warehouse_copy)

            sequence = []

            # Adds the sequence of actions of the state
            for action_2 in solver.unexpanded_actionSequences[index]:
                sequence.append(action_2)
            sequence.append(action)
            solver.unexpanded_actionSequences.append(sequence)

            # Finds the heuristic value of the state and adds it to the list
            h = hueristic_distance(warehouse_copy.boxes,solver.goal,solver.initial.weights) + weight
            solver.hueristic.append(h)

        # Adds current state to expanded states
        solver.expanded_states.append(solver.current)
        solver.expanded_actionSequences.append(solver.unexpanded_actionSequences[index])
        solver.expanded_weights.append(solver.unexpanded_weights[index])
        # deletes current state from unexpanded list
        del solver.hueristic[index]
        del solver.unexpanded_states[index]
        del solver.unexpanded_actionSequences[index]
        del solver.unexpanded_weights[index]

    if(set(solver.current.boxes) == set(solver.goal)):
        return [[solver.expanded_actionSequences[len(solver.expanded_actionSequences)-1]],solver.expanded_weights[len(solver.expanded_weights)-1]]
    else:
        return "Impossible",None

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def move_worker(state,action):
    """
    Moves worker and box in a certain direction.
    
    @param 
        state: a valid State object representing the current state
        action: a string representing the action to take
        
    @return
        None
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
        #Moves Box along with worker if box is in the way
        if box_or_wall(worker_left,state)[0]:
            index = state.boxes.index((worker_left[0],worker_left[1]))
            state.boxes[index] = (worker_left2[0],worker_left2[1])

        state.worker = (worker_left[0],worker_left[1])

    if action == "Right":
        #Moves Box along with worker if box is in the way
        if box_or_wall(worker_right,state)[0]:
            index = state.boxes.index((worker_right[0],worker_right[1]))
            state.boxes[index] = (worker_right2[0],worker_right2[1])

        state.worker = (worker_right[0],worker_right[1])

    if action == "Up":
        #Moves Box along with worker if box is in the way
        if box_or_wall(worker_up,state)[0]:
            index = state.boxes.index((worker_up[0],worker_up[1]))
            state.boxes[index] = (worker_up2[0],worker_up2[1])

        state.worker = (worker_up[0],worker_up[1])
    
    if action == "Down":
        #Moves Box along with worker if box is in the way
        if box_or_wall(worker_down,state)[0]:
            index = state.boxes.index((worker_down[0],worker_down[1]))
            state.boxes[index] = (worker_down2[0],worker_down2[1])

        state.worker = (worker_down[0],worker_down[1])

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
      
def hueristic_distance(boxes,targets,weights):
    """
    This function calculates an approximate cost of the movement required to move boxes from their current location to their target location in a warehouse. It returns a numerical value representing the estimated cost.

    @param
    boxes: a list of tuples containing the current location of each box
    targets: a list of tuples containing the target location of each box
    weights: a list of numerical values representing the weights of each box

    @return
    Returns a numerical value representing the estimated cost of moving the boxes 
    from their current location to their target location. 
    The cost is calculated as the sum of the Manhattan distances between the current location and target location of each box, multiplied by the weight of the box plus one. 
    The returned value is an estimate and may not represent the actual cost required to move the boxes to their target location.        
    """

    # represents the smallest distance between each box
    distance = 0
    i = 0
    for i in range(len(boxes)):
        newdistance = (abs(boxes[i][0] - targets[i][0]) + abs(boxes[i][1] - targets[i][1])) * (weights[i] + 1)
        distance = distance + newdistance  
        
    return distance
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def remove_taboo_state(state,taboo):
    """
    Check whether a given state has any boxes in taboo cells

    @param
    state: a warehouse object

    @return
    Returns a boolean value indicating whether the state has any boxes in taboo cells
    """
    is_not_taboo = True
    for tup in taboo:
        for box in state.boxes:
            if tup == box and box not in state.targets:
                is_not_taboo = False
                                      
    return is_not_taboo

def Is_duplicate_state(expanded,warehouse):
    """
    This function takes in a list of expanded states and a warehouse object and checks if the current state of the warehouse is a duplicate in the list of expanded states. It returns a boolean value indicating whether the current state is a duplicate or not.

    @param
    expanded: a list of valid State objects representing the states that have already been expanded
    warehouse: a valid Warehouse object representing the current state

    @return
    Returns a boolean value indicating whether the current state is a duplicate in the 
    list of expanded states. If the current state is a duplicate, returns True. Otherwise, returns False.
    """

    is_duplicate = False

    for state in expanded:
        if state.boxes == warehouse.boxes:
            if state.worker == warehouse.worker:
                is_duplicate = True
                
    return is_duplicate


def deep_copy(warehouse):
    """
    This function creates a deep copy of a given Warehouse object. It returns the deep copy of the given warehouse object.

    @param
    warehouse: a valid Warehouse object

    @return
    Returns a deep copy of the given warehouse object. 
    The copy is created by copying all attributes of the given warehouse object to a new instance of the Warehouse class. 
    The returned object is an independent copy and any changes made to it will not affect the original object.
    """

    # initialize copy as empty warehouse
    copy = sokoban.Warehouse()
    copy.worker =  warehouse.worker
    i = 0
    copy.boxes = [None] * len(warehouse.boxes)
    for box in warehouse.boxes:
        copy.boxes[i] = box
        i += 1
    copy.weights = warehouse.weights
    copy.targets = warehouse.targets
    copy.walls = warehouse.walls
    copy.ncols = warehouse.ncols
    copy.nrows = warehouse.nrows
    return copy
