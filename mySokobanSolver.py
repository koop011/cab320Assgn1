
'''

The partially defined functions and classes of this module 
will be called by a marker script. 

You should complete the functions and classes according to their specified interfaces.
 

'''

import search

import sokoban

import itertools


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [ (8843325, 'Sam', 'Rogan'), (8806781, 'Seok', 'Yoon'), (7007035, 'Tom', 'Burke') ]


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
    ## if a corner make taboo
    ## if no goal or gap is on this wall make taboo
    ## if the distance between 2 corners is not entirely filled by walls then there must be a gap 

    cells = []  #list for taboo cells
    #loop through all positions in puzzle
    for (x,y) in warehouse.walls:
        #find the inner and outer walls for this particular position
        ymax = max(list(j for (i,j) in warehouse.walls if i==x))
        xmax = max(list(i for (i,j) in warehouse.walls if j==y))
        ymin = min(list(j for (i,j) in warehouse.walls if i==x))
        xmin = min(list(i for (i,j) in warehouse.walls if j==y))
        count = 0
        if (x+1, y) not in warehouse.walls and x+1 <= xmax:
            if (x+1, y) not in cells: ##check for doubles
                ##check if corner
                if (x+1, y+1) in warehouse.walls or (x+1, y-1) in warehouse.walls:
                    if (x+1, y) not in warehouse.targets:
                        cells.append((x+1,y))
                ##check for a target on this wall
                elif x+1 not in [x[0] for x in warehouse.targets]:
                    ##check for a blank space or hole on this wall
                    for j in range(ymin,ymax):
                        if (x, j) in warehouse.walls:
                            count += 1
                    if count == (ymax-ymin):
                        ##if all criteria are met append taboocell
                        cells.append((x+1,y))
                    count = 0 ##clear counter
                    ## this is repeated for a wall on each side of player
        if (x-1, y) not in warehouse.walls and x-1 > xmin:
            if (x-1, y) not in cells:
                if (x-1, y+1) in warehouse.walls or (x-1, y-1) in warehouse.walls:
                    if (x-1, y) not in warehouse.targets:
                        cells.append((x-1,y))
                elif x-1 not in [x[0] for x in warehouse.targets]:
                    for j in range(ymin,ymax):
                        if (x, j) in warehouse.walls:
                            count += 1
                    if count == (ymax-ymin):
                        cells.append((x-1,y))
                    count = 0
        if (x, y+1) not in warehouse.walls and y+1 <= ymax:
            if (x, y+1) not in cells:
                if (x+1, y+1) in warehouse.walls or (x-1, y+1) in warehouse.walls:
                    if (x, y+1) not in warehouse.targets:
                        cells.append((x, y+1))
                elif y+1 not in [x[1] for x in warehouse.targets]:
                    for i in range(xmin,xmax):
                        if (i, y) in warehouse.walls:
                            count += 1
                    if count == (xmax-xmin):
                        cells.append((x,y+1))
                    count = 0
        if (x, y-1) not in warehouse.walls and y-1 > ymin:
            if (x, y-1) not in cells:
                if (x+1, y-1) in warehouse.walls or (x-1, y-1) in warehouse.walls:
                    if (x, y-1) not in warehouse.targets:
                        cells.append((x,y-1)) 
                elif y-1 not in [x[1] for x in warehouse.targets]:
                    for i in range(xmin,xmax):
                        if (i, y) in warehouse.walls:
                            count += 1
                    if count == (xmax-xmin):
                        cells.append((x,y-1))
                    count = 0 
    # code addapted from __str__ in warehouse class                
    X,Y = zip(*warehouse.walls) 
    x_size, y_size = 1+max(X), 1+max(Y)
    
    vis = [[" "] * x_size for y in range(y_size)]
    for (x,y) in warehouse.walls:
        vis[y][x] = "#"
    for (x,y) in cells:
        vis[y][x] = "X"

    return "\n".join(["".join(line) for line in vis])

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class SokobanPuzzle(search.Problem):
    '''
    Class to represent a Sokoban puzzle.
    Your implementation should be compatible with the
    search wfunctions of the provided module 'search.py'.
    
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
        self.initial = warehouse.copy()
        
        ## need to create list of strings
        ##taboo_cells(warehouse).split(sep='\n')

        self.taboo_cells = list(sokoban.find_2D_iterator(taboo_cells(warehouse).split(sep='\n'), "X"))


        self.goal = tuple(warehouse.targets)

        
        

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
            if (x_pos, y_pos+1) in state.boxes:
                if (x_pos, y_pos+2) not in self.taboo_cells and (x_pos, y_pos+2) not in state.walls:
                    L.append('Down')
            else:
                L.append('Down')  
        # test if moving down pushes into a wall, or box into a taboo cell
        if (x_pos, y_pos-1) not in state.walls:
            if (x_pos, y_pos-1) in state.boxes:
                if (x_pos, y_pos-2) not in self.taboo_cells and (x_pos, y_pos-2) not in state.walls:
                    L.append('Up')
            else:
                L.append('Up')
        # test if moving left pushes into a wall, or box into a taboo cell
        if (x_pos-1, y_pos) not in state.walls:
            if (x_pos-1, y_pos) in state.boxes:
                if (x_pos-2, y_pos) not in self.taboo_cells and (x_pos-2, y_pos) not in state.walls:
                    L.append('Left')
            else:
                L.append('Left')
        # test if moving right pushes into a wall, or box into a taboo cell
        if (x_pos+1, y_pos) not in state.walls:
            if (x_pos+1, y_pos) in state.boxes:
                if (x_pos+2, y_pos) not in self.taboo_cells and (x_pos+2, y_pos) not in state.walls:
                    L.append('Right')
            else:
                L.append('Right')
        return L
        #raise NotImplementedError
        
    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        # need to make a copy of state wich should be a warehouse object
        x_pos = state.worker[0]
        y_pos = state.worker[1]
        assert action in self.actions(state)
        #asserts error if action not possible
        #next_state = Warehouse()

        if action == 'Down':
            if (x_pos, y_pos+1) in state.boxes:
                next_boxes = [(x_pos, y_pos+2) if (x,y)==(x_pos, y_pos+1) else (x,y) for (x,y) in state.boxes]
                next_state = state.copy(worker = (x_pos, y_pos+1), boxes = next_boxes)
            else:
                next_state = state.copy(worker = (x_pos, y_pos+1))
        elif action == 'Up':
            if (x_pos, y_pos-1) in state.boxes:
                next_boxes = [(x_pos, y_pos-2) if (x,y)==(x_pos, y_pos-1) else (x,y) for (x,y) in state.boxes]
                next_state = state.copy(worker = (x_pos, y_pos-1), boxes = next_boxes)
            else:
                next_state = state.copy(worker = (x_pos, y_pos-1))
        elif action == 'Left':
            if (x_pos-1, y_pos) in state.boxes:
                next_boxes = [(x_pos-2, y_pos) if (x,y)==(x_pos-1, y_pos) else (x,y) for (x,y) in state.boxes]
                next_state = state.copy(worker = (x_pos-1, y_pos), boxes = next_boxes)
            else:
                next_state = state.copy(worker = (x_pos-1, y_pos))
        elif action == 'Right':
            if (x_pos+1, y_pos) in state.boxes:
                next_boxes = [(x_pos+2, y_pos) if (x,y)==(x_pos+1, y_pos) else (x,y) for (x,y) in state.boxes]
                next_state = state.copy(worker = (x_pos+1, y_pos), boxes = next_boxes)
            else:
                next_state = state.copy(worker = (x_pos+1, y_pos))
        return next_state

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough."""
        ## create all permutations of boxes and check if boxe are same as goal
        permu_boxes = list(itertools.permutations(state.boxes))
        for i in range(len(permu_boxes)):
            if tuple(permu_boxes[i])==self.goal:
                return True
        return False
        



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

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
    puzzle= SokobanPuzzle(warehouse)
    for action in action_seq:
        
        ## Get result of action
        warehouse=puzzle.result(warehouse,action)
        
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

    
    def h(node):
        '''
        This function finds the heuristics of the current node.
        
        @parm node: a valid Node object 
        
        @return 
            The heuristic of the current node, heuristic if defined as infinity
            if action is illegal, otherwise it takes the minimum manhattan 
            distance of boxes to goals when each box is assigned to only 1 goal.
            With this the manhattan distance from the target to the closest box 
            is also added to the heuristic.
        '''
        # check if doing an illegal action if illegal make heuristic really large
        if check_action_seq(node.state,node.solution()) == 'Failure':
            return 10000 # illegal action impossible so heuristic is infinity
        
        # create every possible permutation of targets
        permu_targets = list(itertools.permutations(node.state.targets))
        heuristic_list = []
        # loop through every permutation
        for i in range(len(permu_targets)):
             # zip permutation and boxes for comparison
             zipped = list(zip(node.state.boxes, permu_targets[i]))
             total_abs_value = 0
             # loop through lists and find total absolute distance from targets to boxes
             for j in range(len(zipped)):
                 abs_value = abs(zipped[j][0][0]-zipped[j][1][0]) + abs(zipped[j][0][1]-zipped[j][1][1])
                 total_abs_value = total_abs_value + abs_value
             heuristic_list.append(total_abs_value)   
        
        # take the minimum absolute distance of boxes to targets
        boxtotarget_distance = min(heuristic_list)
        
        heuristic_list = []
        # store the absolute distance between the worker and the closest goal in a list
        for (x,y) in node.state.boxes:
            abs_distance = abs(x-node.state.worker[0])+abs(y-node.state.worker[1])
            heuristic_list.append(abs_distance)
        #get the minimum distance between worker and closest goal    
        workertobox_distance = min(heuristic_list)

        return boxtotarget_distance + workertobox_distance
    #A* graph search on puzzle using the heuristic function definied 
    ans = search.astar_graph_search(SokobanPuzzle(warehouse), h)
    if ans == []:
        return 'Impossible'
    else:
        return ans.solution()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def can_go_there(warehouse, dst):
    def f(node):
         h=abs(warehouse.worker[0]-dst[1])+ abs(warehouse.worker[1]-dst[0])
         return h

    ans = search.best_first_graph_search(SokobanPuzzleCanGoThere(warehouse,(dst[1],dst[0])),f)
    if ans == None:
        return False
    else:
        return True
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -       
class SokobanPuzzleCanGoThere(search.Problem):
    
     def __init__(self, warehouse,goal):
        self.initial = warehouse.copy()
        self.goal=goal
    #gives possible actions depending on state
     def actions(self, state):
        L = []
        workerX=state.worker[0]
        workerY=state.worker[1]
        if (workerX,workerY-1) not in state.walls and (workerX,workerY-1) not in state.boxes:
            L.append('Up')
        if (workerX,workerY+1) not in state.walls and (workerX,workerY+1) not in state.boxes:
            L.append('Down')
        if (workerX-1,workerY) not in state.walls and (workerX-1,workerY) not in state.boxes:
            L.append('Left')
        if (workerX+1,workerY) not in state.walls and (workerX+1,workerY) not in state.boxes:
            L.append('Right')
        return L
    #outputs result of action on state
     def result(self, state, action):
        if action == "Up":
            return state.copy(worker = (state.worker[0],state.worker[1]-1))
        elif action == "Down":
            return state.copy(worker = (state.worker[0],state.worker[1]+1))
        elif action == "Left":
            return state.copy(worker = (state.worker[0]-1,state.worker[1]))
        elif action == "Right":
            return state.copy(worker = (state.worker[0]+1,state.worker[1]))

     def goal_test(self, state):
        return state.worker==self.goal
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_macro(warehouse):

    def f(node):
        h=0
        #for each target adds distance of closest box to h
        for target in node.state.targets:
            closest_box_dist=1000000
            for box in node.state.boxes:
                dist_to_target = (abs(target[0]-box[0])+abs(target[1]-box[1]))
                if dist_to_target < closest_box_dist:
                    closest_box_dist=dist_to_target
            h=h+closest_box_dist
        #for each box adds distance of closest target to h
        for box in node.state.boxes:
            closest_target_dist=1000000
            for target in node.state.targets:
                dist_to_box = (abs(target[0]-box[0])+abs(target[1]-box[1]))
                if dist_to_box < closest_target_dist:
                    closest_target_dist=dist_to_box
            h=h+closest_target_dist
        return h
    
    ans = search.best_first_graph_search(SokobanPuzzleMacro(warehouse), f)
    if ans ==None:
        return ['Impossible']
    else:
        return ans.solution()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class SokobanPuzzleMacro(search.Problem):

    
    def __init__(self, warehouse):
        self.initial = warehouse.copy()        
        self.taboo_cells = list(sokoban.find_2D_iterator(taboo_cells(warehouse).split(sep='\n'), "X"))
        self.goal = tuple(warehouse.targets)      

    def actions(self, state):
        L = []
        #check if each box can be pushed
        for box in state.boxes:
            boxcolumn=box[0]
            boxrow=box[1]
            ## up
            if (boxcolumn,boxrow-1) not in self.taboo_cells and (boxcolumn,boxrow-1) not in state.walls and (boxcolumn,boxrow-1) not in state.boxes and can_go_there(state,(boxrow+1,boxcolumn)):
                            L.append(((boxrow,boxcolumn),'Up'))
            ## down
            if (boxcolumn,boxrow+1) not in self.taboo_cells and (boxcolumn,boxrow+1) not in state.walls and (boxcolumn,boxrow+1) not in state.boxes and can_go_there(state,(boxrow-1,boxcolumn)):
                            L.append(((boxrow,boxcolumn),'Down'))                           
            ## left
            if (boxcolumn-1,boxrow) not in self.taboo_cells and (boxcolumn-1,boxrow) not in state.walls and (boxcolumn-1,boxrow) not in state.boxes and can_go_there(state,(boxrow,boxcolumn+1)):
                            L.append(((boxrow,boxcolumn),'Left'))
            ## right
            if (boxcolumn+1,boxrow) not in self.taboo_cells and (boxcolumn+1,boxrow) not in state.walls and (boxcolumn+1,boxrow) not in state.boxes and can_go_there(state,(boxrow,boxcolumn-1)):
                            L.append(((boxrow,boxcolumn),'Right'))
        return L
        
    def result(self, state, action):
        #turns the row column of action into x,y for manipulation
        boxX=action[0][1]
        boxY=action[0][0]
        # determines result based on direction and box to be pushed
        if action[1]=='Up':
                      next_boxes=[(boxX,boxY-1) if (x,y)==(boxX,boxY) else (x,y) for (x,y) in state.boxes]
        elif action[1]=='Down':
                      next_boxes=[(boxX,boxY+1) if (x,y)==(boxX,boxY) else (x,y) for (x,y) in state.boxes]
        elif action[1]=='Left':
                      next_boxes=[(boxX-1,boxY) if (x,y)==(boxX,boxY) else (x,y) for (x,y) in state.boxes]
        elif action[1]=='Right':
                      next_boxes=[(boxX+1,boxY) if (x,y)==(boxX,boxY) else (x,y) for (x,y) in state.boxes]                      
        return state.copy(worker=(boxX,boxY), boxes = next_boxes)
        
    def goal_test(self, state):
        #checks each order of boxes with the targets
        permu_boxes = list(itertools.permutations(state.boxes))
        for i in range(len(permu_boxes)):
            if tuple(permu_boxes[i])==self.goal:
                return True
        return False
    
