#import random

def print_debug(str, end="\n"):
    print("\033[93m{}\033[00m".format(str), end=end)

def sort_set(input_set):
    l = list(input_set.copy())
    l.sort()
    return l

class Maze(object):

    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.size = height*width # Inner dimensions only?


        self.h_walls = [[1 for h in range(width)] for v in range(height-1)]
        self.v_walls = [[1 for v in range(height)] for h in range(width-1)]

        # Initalise a set of all cooordinates.
        self.all_cells = set()
        for i in range(self.width):
            for j in range(self.height):
                self.all_cells.add((i,j))


        #print_debug("h_walls: " + str(self.h_walls))
        #print_debug("v_walls[ " + str(self.v_walls))

    def reset(self):
        """
        Return the maze to it's initial state (with all walls set to 1)
        """
        self.h_walls = [[1 for h in range(self.width)] for v in range(self.height-1)]
        self.v_walls = [[1 for v in range(self.height)] for h in range(self.width-1)]



    def __str__(self):
        str = ""
        for i in range(self.height-1):
            for j in range(self.width-1):
                #print_debug("{},{}".format(i, j))
                str += "_" if self.h_walls[i][j] else " "
                str += "|" if self.v_walls[j][i] else " "
            str += "_\n" if self.h_walls[i][j+1] else " \n" # Last Colunm
        for j in range(self.width-1):
            str += " |" if self.v_walls[j][i+1] else "  " # Last Row
        return str


    def get_neighbours(self, cell):
        """
        Helper function for maze generation. Return all neighbouring
        cells for a given set of input cooordinates.
        """

        # Check legality against height/width?


        neighbours = set()

        if cell[1] > 0:              # North
            neighbours.add((cell[0], cell[1]-1))

        if cell[0] < self.width-1:   # East
            neighbours.add((cell[0]+1, cell[1]))

        if cell[1] < self.height-1:  # South
            neighbours.add((cell[0], cell[1]+1))

        if cell[0] > 0:              # West
            neighbours.add((cell[0]-1, cell[1]))

        return neighbours

    def join_cells(self, existing, new):
        """
        Helper function for maze generation. Creates a path through the
        maze by removing the walls between two cells.
        """
        #print_debug(f"join_cells: existing: {existing}, new: {new}")
        if existing[0] == new[0]:
           self.h_walls [min(existing[1], new[1])] [existing[0]] = 0

        elif existing[1] == new[1]:
           self.v_walls [min(existing[0], new[0])] [existing[1]] = 0
        else:
            print("Error: join_cells should only be called on neighbouring cells.")

    def generate(self, seed):
        """
        Implementation of Prim's algorithm. This will ovewrite the current maze setup.

        See: http://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm

        1) Choose an arbitrary vertex from G (the graph), and add it to some (initially empty) set V.
        2) Choose a random edge that connects a vertex in V with another vertex not in V.
        3) Add that edge to the minimal spanning tree, and the edge’s other vertex to V.
        4) Repeat steps 2 and 3 until V includes every vertex in G.
        """
        import random
        random.seed(seed)

        # Crate a pair of sets to mark progress
        unexplored_cells = self.all_cells.copy()
        traversed_cells = set()

        # Start at the top left corner for now
        #initial_cell = (0,0)
        initial_cell = ( int(self.width/2), int(self.height/2) )
        print(f"Initial Cell: {initial_cell}")


        # As each new cell is covered shuffle between the two sets
        traversed_cells.add(initial_cell)
        # print_debug(f"[1] Number of unexplored cells: {len(unexplored_cells)}")
        # print(unexplored_cells)
        unexplored_cells.discard(initial_cell)
        # print(unexplored_cells)
        # print_debug(f"[2] Number of unexplored cells: {len(unexplored_cells)}")
        frontier_cells = self.get_neighbours(initial_cell) # & unexplored_cells

        #while len(unexplored_cells) > 0:
        while len(traversed_cells) < self.size:
            # print_debug(f"traversed_cells list: {sort_set(traversed_cells)}")
            # print_debug(f"Number of traversed cells: {len(traversed_cells)}, ", end='')
            # print_debug(f"Number of unexplored cells: {len(unexplored_cells)}")
            # print_debug(f"frontier_cells list: {sort_set(frontier_cells)}")

            # Debug
            #print(self)
            #input()

            #print_debug(f"frontier_cells list: {sort_set(frontier_cells)}")
            new = random.sample(frontier_cells, 1)[0]
            #print_debug(f"selected cell: {new}")
            neighbours = self.get_neighbours(new)
            existing = random.sample(neighbours & traversed_cells, 1)[0]
            traversed_cells.add(new)
            unexplored_cells.discard(new)
            frontier_cells.discard(new)
            #print_debug(f"Connecting cells {existing} and {new}")
            self.join_cells(existing, new)

            for cell in neighbours - traversed_cells:
                frontier_cells.add(cell)

            #print_debug("---")


    def randomize(self, seed):
        """
        True Randomization of the maze walls. Not in any way
        gaurenteed to produce any thing remotely usesable.
        """
        import random
        random.seed(seed)
        for i in range(self.height-1):
            for j in range(self.width-1):
                self.h_walls[j][i] = random.choice([1, 0])
                self.v_walls[i][j] = random.choice([1, 0])
            self.h_walls[j][i+1] = random.choice([1, 0])
        for j in range(self.width-1):
            self.v_walls[i][j] = random.choice([1, 0])





# Testing
print("Testing Maze class")
m = Maze(42,28)
print(f"Initial: (size: {m.size})")
print(m)
#print(f"Cell List: {sort_set(m.all_cells)}")

for i in range(1,10):
    input()
    m.reset()
    print(f"Generated (seed : {i*7})")
    m.generate(i)
    print(m)

    print()
