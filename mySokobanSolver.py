
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
    ## check if in bounds 
    ## make list of all walls on row and column
    ## max & min of x in walls when y = y
    ## max & min of y in walls when x = x
    ## do this in first part 
    
    ##nested loop
    ##
    ## make list of targets on wall 
    cells = []  
    for (x,y) in warehouse.walls:
        ymax = max(list(j for (i,j) in warehouse.walls if i==x))
        xmax = max(list(i for (i,j) in warehouse.walls if j==y))
        ymin = min(list(j for (i,j) in warehouse.walls if i==x))
        xmin = min(list(i for (i,j) in warehouse.walls if j==y))
        ##corner_test = [(x+1, y+1), (x-1, y-1), (x-1, y+1), (x+1, y-1)]
        ##if x not in [x[0] for x in warehouse.walls]:
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
                    
    X,Y = zip(*warehouse.walls) # pythonic version of the above
    x_size, y_size = 1+max(X), 1+max(Y)
    
    vis = [[" "] * x_size for y in range(y_size)]
    for (x,y) in warehouse.walls:
        vis[y][x] = "#"
    for (x,y) in cells:
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
        ## note taht this works with 1 goal, might need more robust testing for multiple goals
        ##return tuple(state.boxes) == self.goal
        return tuple(state.boxes) == self.goal




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
    
    ##         "INSERT YOUR CODE HERE"
    # use astar search function 
    # heuristic is sum of manahattan distancea from boxs to closest goals
    # heuristic of distance from player to closest goal 
    # while not travelling through taboocells
    
    # heuristic number of goals without a box on them 
    # loop through boxes 
    
    # h is previously defined heuristic 
    
    ## check if boxes can go to a goal 
    ## read node and check if any boxes are in a goal 
    ## each box not in a goal increases heuristic value 
    ## check if moving box to a specific goal is legal
    ## if legal path cost (edge) is distance from box to goal 
    ## have to find the assignment of boxes to goals that minimises sumation of this distance
    
    def h(node):
        heur = 0
        ## check if any value of boxes is in targets 
        ## check if doing an illegal action if illegal make heuristic really large
#        if check_action_seq(node.state,node.path()) == 'Failure':
#            return 10000 ## illegal action impossible so infinity
        
        assigned_boxes = []
        assigned_targets = []
        distance = 0
        
        ## this loop checks if a box is on a wall if on a wall assign to a target also on that wall 
        for (x,y) in node.state.boxes:
            L = []
            if (x+1,y) or (x-1,y) in node.state.walls:
                ## assign this box to a target thats on a wall 
                for (i,j) in node.state.targets:
                    if i==x:
                        if (i,j) not in L:
                            L.append((i,j))
                            ## these are the possible boxes
#            if (x-1,y) in node.state.walls:
#                ## assign this box to a target thats on a wall 
#                for (i,j) in node.state.targets:
#                    if i==x:
#                        if (i,j) not in L:
#                            L.append((i,j))
#                            ## these are the possible boxes
            if (x,y+1) or (x,y-1) in node.state.walls:
                ## assign this box to a target thats on a wall 
                for (i,j) in node.state.targets:
                    if i==y:
                        if (i,j) not in L:    
                            L.append((i,j))
#            if (x,y-1) in node.state.walls:
#                ## assign this box to a target thats on a wall 
#                for (i,j) in node.state.targets:
#                    if i==y:
#                        if (i,j) not in L:    
#                            L.append((i,j))
            ##if there are targets in list assign box to closest one
            
            if len(L) > 0 :
                dis = 1000
                target = []
                for (i,j) in L:              
                    if (abs(x-i)+abs(y-j)) < dis:
                        dis = abs(x-i)+abs(y-j)
                        target = (i,j)
                assigned_boxes.append((x,y))
                assigned_targets.append(target)
                distance = distance + dis    
        
        print("distance 1: ")
        print(distance)
        ## each node has a bunch of stored actions
        ## check if any boxes already on a target 
        for (x,y) in node.state.boxes:
            if (x,y) in node.state.targets:
                if (x,y) not in assigned_boxes:
                    assigned_boxes.append((x,y))
                    assigned_targets.append((x,y))
#            else:    
#                heur = heur + 100 # if not in targets add large heuristic
#                boxes.append(x,y)
#                targets.append(x,y)

            ## maybe pop this value out of boxes and targets
            
        
        ## for check action sequence 
        # check_action_seq(node.state.sololution())
        available_targets = []
        available_boxes = []
        ## check what targets are available
        for (x,y) in node.state.targets:
            if (x,y) not in assigned_targets:
                available_targets.append((x,y))
        for (x,y) in node.state.boxes:
            if (x,y) not in assigned_boxes:
                available_boxes.append((x,y))
        
        permu_targets = list(itertools.permutations(available_targets))
        heuristic_list =[]
        for i in range(len(permu_targets)):
             zipped = list(zip(available_boxes, permu_targets[i]))
             total_abs_value = 0
             for j in range(len(zipped)):
                 abs_value = abs(zipped[j][0][0]-zipped[j][1][0]) + abs(zipped[j][0][1]-zipped[j][1][1])
                 total_abs_value = total_abs_value + abs_value
             heuristic_list.append(total_abs_value)   

        print(heuristic_list)
        
#        for (x,y) in availible_boxes:
#            min_dis_heur = 1000
#            current_dis_heur = 0
#            if (x,y) not in assigned_boxes:
#                for (i,j) in node.state.targets:
#                    if (i,j) not in assigned_targets:
#                        current_dis_heur = current_dis_heur + abs(x-i) + abs(y-j)
#                if current_dis_heur < min_dis_heur:
#                    min_dis_heur = current_dis_heur
        
            
        distance = distance + min(heuristic_list)
        print("distance 2: ")
        print(distance)
        print(node.state)

        return distance
        
#    heur = 0
#    for (x,y) in warehouse.boxes:
#        man_dis = []
#        for (i, j) in warehouse.targets:
#            man_dis.append(abs(x-i)+abs(y-j))
#        heur = heur + min(man_dis)
#        del man_dis
        
    ## check is action sequence is legal 
    #print(heur)
    ans = search.astar_graph_search(SokobanPuzzle(warehouse), h)
    return ans.solution()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def can_go_there(warehouse, dst):
    def f(node):
         h=abs(warehouse.worker[0]-dst[1])+ abs(warehouse.worker[1]-dst[0])
         return h
    
        
    '''    
    Determine whether the worker can walk to the cell dst=(row,col) 
    without pushing any box.
    
    @param warehouse: a valid Warehouse object

    @return
      True if the worker can walk to cell dst=(row,col) without pushing any box
      False otherwise
    ''' 
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
        for target in node.state.targets:
            closest_box_dist=1000000
            for box in node.state.boxes:
                dist_to_target = (abs(target[0]-box[0])+abs(target[1]-box[1]))
                if dist_to_target < closest_box_dist:
                    closest_box_dist=dist_to_target
            h=h+closest_box_dist
        for box in node.state.boxes:
            closest_target_dist=1000000
            for target in node.state.targets:
                dist_to_box = (abs(target[0]-box[0])+abs(target[1]-box[1]))
                if dist_to_box < closest_target_dist:
                    closest_target_dist=dist_to_box
            h=h+closest_target_dist
        #print (h)
        return h


        
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

    
    ans = search.best_first_graph_search(SokobanPuzzleMacro(warehouse), f)
    
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
        #print (L)
        return L
        
    def result(self, state, action):
        boxX=action[0][1]
        boxY=action[0][0]                      
        if action[1]=='Up':
                      next_boxes=[(boxX,boxY-1) if (x,y)==(boxX,boxY) else (x,y) for (x,y) in state.boxes]
        elif action[1]=='Down':
                      next_boxes=[(boxX,boxY+1) if (x,y)==(boxX,boxY) else (x,y) for (x,y) in state.boxes]
        elif action[1]=='Left':
                      next_boxes=[(boxX-1,boxY) if (x,y)==(boxX,boxY) else (x,y) for (x,y) in state.boxes]
        elif action[1]=='Right':
                      next_boxes=[(boxX+1,boxY) if (x,y)==(boxX,boxY) else (x,y) for (x,y) in state.boxes]                      
        #print (state.copy(worker=(boxX,boxY), boxes = next_boxes))
        return state.copy(worker=(boxX,boxY), boxes = next_boxes)
        
    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough."""
        return tuple(state.boxes) == self.goal
    
