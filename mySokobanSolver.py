
'''

The partially defined functions and classes of this module 
will be called by a marker script. 

You should complete the functions and classes according to their specified interfaces.
 

'''

import search

import sokoban



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [ (8843325, 'Sam', 'Rogan'), (8806781, 'Leo', 'Yoon'), (1234569, 'Eva', 'Tardos') ]


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A cell is called 'taboo' 
    if whenever a box get pushed on such a cell then the puzzle becomes unsolvable.  
    When determining the taboo cells, you must ignore all the existing boxes, 
    simply consider the walls and the target  cells.  
    Use only the following two rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of 
             these cells is a target.
    
    @param warehouse: a Warehouse object

    @return
       A string representing the puzzle with only the wall cells marked with 
       an '#' and the taboo cells marked with an 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''
    ## find cells adjacent to walls and within boundaries 
    ## check if in bounds 
    ## make list of all walls on row and column
    ## max & min of x in walls when y = y
    ## max & min of y in walls when x = x
    ## do this in first part 
    cells = []  
    for (x,y) in warehouse.walls:
        ymax = max(list(j for (i,j) in warehouse.walls if i==x))
        xmax = max(list(i for (i,j) in warehouse.walls if j==y))
        if (x+1, y) not in warehouse.walls and x+1 <= xmax:
            cells.append((x+1,y))
        if (x-1, y) not in warehouse.walls and x-1 > 0:
            cells.append((x-1,y))
        if (x, y+1) not in warehouse.walls and y+1 <= ymax:
            cells.append((x, y+1))
        if (x, y-1) not in warehouse.walls and y-1 > 0:      
            cells.append((x,y-1)) 
            
    ## if taboocells  has a double then its a corner
    ## check for doubles in taboocells and store in a list for corners
    ## need to check if corners are in bounds so after 1st wall and before 
    ## last wall 
    print(cells)
    corners = []
    seen = set()
    for (x,y) in cells:
        if (x,y) in seen and (x,y) not in warehouse.targets: 
            corners.append((x,y))
        seen.add((x,y))
        
    ## check if there are 2 corners on any row or column
    ## if more then 2 corners on row or column add to enclosed row or column 

    enclosed_row = []
    enclosed_column = []
    measured_row = []
    measured_column = []
    seen_x = set()
    seen_y = set()
    index_x = 0
    index_y = 0
    for (x, y) in corners:
        if x in seen_x and x not in measured_column:
            enclosed_column.append([x])
            for (i,j) in corners:
                if i == x : enclosed_column[index_x].append(j) 
            ## mark column as measured
            measured_column.append(x)
            index_x += 1
        if y in seen_y and y not in measured_row: 
            enclosed_row.append([y])
            for (i,j) in corners:
                if j == y: enclosed_row[index_y].append(i) ## also need other x value
            ## mark row as measured
            measured_row.append(y)
            index_y += 1
        seen_x.add(x)
        seen_y.add(y)
    
    ## check length of columns and rows, if even remove an element 

    ## loop through every second starting at the second
    ## need to consider U shape with flat tops
    for i in reversed(range(len(enclosed_column))):
        x = enclosed_column[i][0]
        for j in range(1,len(enclosed_column[i]),2):##enclosed_column[i][1::2]:
            for y in range(enclosed_column[i][j],enclosed_column[i][j+1]):
                if (x,y)  not in warehouse.targets or (x,y) in cells:
                    del enclosed_column[i]  
                    break
                
    for i in reversed(range(len(enclosed_row))):
        y = enclosed_row[i][0]
        for j in range(1,len(enclosed_row[i]),2):##enclosed_column[i][1::2]:
            for x in range(enclosed_row[i][j],enclosed_row[i][j+1]):
                if (x,y) in warehouse.targets or (x,y) not in cells:
                    del enclosed_row[i]  
                    break
    ## add these tabboo cells to corners
    ## improve logic so this can be done in earlier loop 
    for i in range(len(enclosed_column)):
        x = enclosed_column[i][0]
        for j in range(1,len(enclosed_column[i]),2):##enclosed_column[i][1::2]:
            for y in range(enclosed_column[i][j]+1,enclosed_column[i][j+1]):
                corners.append((x,y))
                
    for i in reversed(range(len(enclosed_row))):
        y = enclosed_row[i][0]
        for j in range(1,len(enclosed_row[i]),2):##enclosed_column[i][1::2]:
            for x in range(enclosed_row[i][j]+1,enclosed_row[i][j+1]):
                corners.append((x,y))
                
    X,Y = zip(*warehouse.walls) # pythonic version of the above
    x_size, y_size = 1+max(X), 1+max(Y)
    
    vis = [[" "] * x_size for y in range(y_size)]
    for (x,y) in warehouse.walls:
        vis[y][x] = "#"
    for (x,y) in corners:
        vis[y][x] = "X"

    return "\n".join(["".join(line) for line in vis])

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#        list_x = []
#        list_y = []
#        for (i,j) in warehouse.walls:
#            if i == x:
#                list_y.append((i,j))
#            if j == y:
#                list_x.append((i,j))

#        list_y = list((i,j) for (i,j) in warehouse.walls if i==x)
#        list_x = list((i,j) for (i,j) in warehouse.walls if j==y)
#        xmax = max(list_x,key=lambda item:item[0])[0]
#        ymax = max(list_y,key=lambda item:item[1])[1] 

#        ymax = max(list(j for (i,j) in warehouse.walls if i==x))
#        xmax = max(list(i for (i,j) in warehouse.walls if j==y))

class SokobanPuzzle(search.Problem):
    '''
    Class to represent a Sokoban puzzle.
    Your implementation should be compatible with the
    search functions of the provided module 'search.py'.
    
    	Use the sliding puzzle and the pancake puzzle for inspiration!
    
    '''
    ##         "INSERT YOUR CODE HERE"
    #state cares about player position and box position
    # taboo cells are setup in __init__
    
    def __init__(self, warehouse):
        #give initial state and goal state 
        #give this as initial warhouse object
        #give goal as warehouse object finished
        #dont car about where player is at end 

        self.taboo_cells = list(sokoban.find_2D_iterator(taboo_cells(warehouse), "X"))

        self.goal = warehouse.targets 
        
        raise NotImplementedError()

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state 
        if these actions do not push a box in a taboo cell.
        The actions must belong to the list ['Left', 'Down', 'Right', 'Up']        
        """
        # state would be a warehouse object 
        L = [] #List of legal actions
        
        
        #check if any action, "UP", "DOWN", "RIGHT", "LEFT" puts a box in
        #taboo cell or pushes worker into a wall \
        
        #check if move contains wall or box
        x_pos = state.worker[0]
        y_pos = state.worker[1]
        # test if moving up pushes into a wall, or box into a taboo cell
        if (x_pos, y_pos+1) not in state.walls:
            if (x_pos, y_pos+1) in state.boxes and (x_pos, y_pos+2) not in self.taboo_cells:
                L.append('Up')
        # test if moving down pushes into a wall, or box into a taboo cell
        if (x_pos, y_pos-1) not in state.walls:
            if (x_pos, y_pos-1) in state.boxes and (x_pos, y_pos-2) not in self.taboo_cells:
                L.append('Down')
        # test if moving left pushes into a wall, or box into a taboo cell
        if (x_pos-1, y_pos) not in state.walls:
            if (x_pos-1, y_pos) in state.boxes and (x_pos-2, y_pos) not in self.taboo_cells:
                L.append('Left')
        # test if moving right pushes into a wall, or box into a taboo cell
        if (x_pos+1, y_pos) not in state.walls:
            if (x_pos+1, y_pos) in state.boxes and (x_pos+2, y_pos) not in self.taboo_cells:
                L.append('Right')
        return L
        #raise NotImplementedError
        
    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        # need to make a copy of state wich should be a warehouse object
        x_pos = state.worker[0][0]
        y_pos = state.worker[0][1]
        assert action in self.actions(state)
        #asserts error if action not possible
        #next_state = Warehouse()
        if action == 'Up':
            if (x_pos, y_pos+1) in state.boxes:
                next_boxes = [(x_pos, y_pos+2) if (x,y)==(x_pos, y_pos+1) else (x,y) for (x,y) in state.boxes]
                next_state = state.copy(worker = (x_pos, y_pos+1), boxes = next_boxes)
            next_state = state.copy(worker = (x_pos, y_pos+1))
        if action == 'Down':
            if (x_pos, y_pos-1) in state.boxes:
                next_boxes = [(x_pos, y_pos-2) if (x,y)==(x_pos, y_pos-1) else (x,y) for (x,y) in state.boxes]
                next_state = state.copy(worker = (x_pos, y_pos-1), boxes = next_boxes)
            next_state = state.copy(worker = (x_pos, y_pos-1))
        if action == 'Left':
            if (x_pos-1, y_pos) in state.boxes:
                next_boxes = [(x_pos-2, y_pos) if (x,y)==(x_pos-1, y_pos) else (x,y) for (x,y) in state.boxes]
                next_state = state.copy(worker = (x_pos-1, y_pos), boxes = next_boxes)
            next_state = state.copy(worker = (x_pos-1, y_pos))
        if action == 'Right':
            if (x_pos+1, y_pos) in state.boxes:
                next_boxes = [(x_pos+2, y_pos) if (x,y)==(x_pos+1, y_pos) else (x,y) for (x,y) in state.boxes]
                next_state = state.copy(worker = (x_pos+1, y_pos), boxes = next_boxes)
            next_state = state.copy(worker = (x_pos+1, y_pos))
            
        return next_state

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough."""
        return state.boxes == self.goal
    
    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        
        #state is a warehouse
        
        
        return c + 1
    


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#        if (xpos, y_pos+1) not in state.boxes or (xpos, y_pos+1) not in state.walls:
#            L.append('Up')
#        else if (xpos, y_pos+1) in state.boxes and (xpos, y_pos+2) not in taboo_coordinates:
#            L.append('Up')
#        # test if moving down pushes into a wall, or box into a taboo cell
#        if (xpos, y_pos-1) not in state.boxes or (xpos, y_pos-1) not in state.walls:
#            L.append('Down')
#        else if (xpos, y_pos-1) in state.boxes and (xpos, y_pos-2) not in taboo_coordinates:
#            L.append('Down')
#        # test if moving left pushes into a wall, or box into a taboo cell
#        if (xpos-1, y_pos) not in state.boxes or (xpos-1, y_pos) not in state.walls:
#            L.append('Left')
#        else if (xpos-1, y_pos) in state.boxes and (xpos-2, y_pos) not in taboo_coordinates:
#            L.append('Left')
#        # test if moving right pushes into a wall, or box into a taboo cell
#        if (xpos+1, y_pos) not in state.boxes or (xpos+1, y_pos) not in state.walls:
#            L.append('Right')
#        else if (xpos+1, y_pos) in state.boxes and (xpos+2, y_pos) not in taboo_coordinates:
#            L.append('Right')
#        return L
def check_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Failure', if one of the action was not successul.
           For example, if the agent tries to push two boxes at the same time,
                        or push one box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    
    ##Do each action in action sequence
    for action in action_seq:
        
        ## Get result of action
        warehouse=result(warehouse,action)
        
        ##For each box
        for box in warehouse.boxes:
            
            ##Create empty set and test for box stacking 
            seen = set()
            if box in seen:
                return 'Failure'            
            else:
                seen.add(box)
                
            ##Test for boxes on walls    
            for wall in warehouse.walls:
                if wall==box:
                    return 'Failure'
                
        ##test for worker inside wall
        for wall in warehouse.walls:
            if wall==warehouse.worker:
                return 'Failure'
            
    ## return string as per documentation        
    return warehouse.__str__()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_elem(warehouse):
    '''    
    This function should solve using elementary actions 
    the puzzle defined in a file.
    
    @param warehouse: a valid Warehouse object

    @return
        A list of strings.
        If puzzle cannot be solved return ['Impossible']
        If a solution was found, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''
    
    ##         "INSERT YOUR CODE HERE"
    # use astar search function 
    # heuristic is sum of manahattan distancea from boxs to closest goals
    # heuristic of distance from player to closest goal 
    # while not travelling through taboocells
    
    # loop through boxes 
    
    # h is previously defined heuristic 
    h = 0
    for (x,y) in warehouse.boxes:
        man_dis = []
        for (i, j) in warehouse.targets:
            man_dis.append(abs(x-i)+abs(y-j))
        h = h + min(man_dis)
        del man_dis
        
    ## check is action sequence is legal 
    
    return astarsearch(warehouse, h)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def can_go_there(warehouse, dst):
    '''    
    Determine whether the worker can walk to the cell dst=(row,col) 
    without pushing any box.
    
    @param warehouse: a valid Warehouse object

    @return
      True if the worker can walk to cell dst=(row,col) without pushing any box
      False otherwise
    '''
    
    ##       
     '''
    for box in warehouse.boxes:
        
        
        
        
        x,y = zip(*warehouse.walls)
        
        if box[0] in range(warehouse.worker[0],dst[1]) and warehouse.worker[1] is box[1]:
            return False
        if box[1] in range(warehouse.worker[1],dst[0]) and warehouse.worker[0] is box[0]:
            return False
        if dst[0] > x+1 and dst[1] > y+1:
            return False
        
        if box[0] in range(warehouse.worker[0],dst[0]) or box[1] in range(warehouse.worker[1],dst[1]):
            return False
        elif box[0] is warehouse.worker[0] and box[1] is warehouse.worker[1]:
            return False
        else:
            return True
        
        if box[0] in range(warehouse.worker[0],dst[0]) or box[1] is warehouse.worker:
            return False
        elif box[1] in range(warehouse.worker[0],dst[0]) or box[0] is warehouse.worker:
            return False
        '''
        

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_macro(warehouse):
    '''    
    Solve using macro actions the puzzle defined in the warehouse passed as
    a parameter. A sequence of macro actions should be 
    represented by a list M of the form
            [ ((r1,c1), a1), ((r2,c2), a2), ..., ((rn,cn), an) ]
    For example M = [ ((3,4),'Left') , ((5,2),'Up'), ((12,4),'Down') ] 
    means that the worker first goes the box at row 3 and column 4 and pushes it left,
    then goes the box at row 5 and column 2 and pushes it up, and finally
    goes the box at row 12 and column 4 and pushes it down.
    
    @param warehouse: a valid Warehouse object

    @return
        If puzzle cannot be solved return ['Impossible']
        Otherwise return M a sequence of macro actions that solves the puzzle.
        If the puzzle is already in a goal state, simply return []
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

