def print_debug(str):
    print("\033[93m{}\033[00m" .format(str))


class Maze(object):

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.size = height*width # Inner dimensions only?

        # Initialise the inner grid only with all walls "on", i.e. blocked
        self.h_walls = [[1 for h in range(height)] for v in range(width-1)]
        self.v_walls = [[1 for v in range(width)] for h in range(height-1)]

        print_debug("h_walls: " + str(self.h_walls[0]))
        print_debug("v_walls: " + str(self.v_walls[0]))

    def reset(self):
        """
        Return the maze to it's initial state (with all walls set to 1)
        """
        self.h_walls = [[1 for h in range(self.height)] for v in range(self.width-1)]
        self.v_walls = [[1 for v in range(self.width)] for h in range(self.height-1)]


    def __str__(self):
        str = ""
        for i in range(self.height-1):
            for j in range(self.width-1):
                str += "_" if self.h_walls[j][i] else " "
                str += "|" if self.v_walls[i][j] else " "
            str += "_\n" if self.h_walls[j][i+1] else " \n" # Last Colunm
        for j in range(self.width-1):
            str += " |" if self.v_walls[i][j] else "  " # Last Row
        return str


    def get_neighbours(self, cell):
        """
        Helper function for maze generation. Return all neighbouring
        cells for a given set of input cooordinates.
        """

        # Check legality against height/width?

        neighbours = []

        if cell[1] > 0:              # North
            neighbours.append((cell[0], cell[1]-1))

        if cell[0] < self.width-1:   # East
            neighbours.append((cell[0]+1, cell[1]))

        if cell[1] < self.height-1:  # South
            neighbours.append((cell[0], cell[1]+1))

        if cell[0] > 0:              # West
            neighbours.append((cell[0]-1, cell[1]))

        return neighbours

    def join_cells(self, existing, new):
        """
        Helper function for maze generation. Creates a path through the
        maze by removing the walls between two cells.
        """

        if existing[0] == new[0]:
           self.v_walls[existing[0]][min(existing[1], new[1])] = 0

        elif existing[1] == new[1]:
           self.h_walls[existing[1]][min(existing[0], new[0])] = 0
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
        # Start at the top left corner for now
        path_list = [(0,0)]
        while len(path_list) < self.size:
            existing = random.choice(path_list)
            print_debug(f"In cell: {existing}")
            N = self.get_neighbours(existing)
            print_debug(f"Neighbours: {N}")
            new = random.choice(self.get_neighbours(existing))
            path_list.append(new)
            self.join_cells(existing, new)
            print_debug(f"Connecting cells {existing} and {new}")


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
m = Maze(5,10)
print("Initial:")
print(m)
print()

for i in range(5):
    m.reset()
    m.generate(i*50)
    print(f"Randomized (seed : {i*50})")
    print(m)
    print()


# From: http://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm
# --------------------------------------------------------------------
# An implementation of Prim's algorithm for generating mazes.
# This is a pretty fast algorithm, when implemented well, since it
# only needs random access to the list of frontier cells. It does
# require space proportional to the size of the maze, but even worse-
# case, it won't be but a fraction of the size of the maze itself.
# As with Kruskal's, this algorithm tends to generate mazes with many
# short cul-de-sacs.


# srand(seed)
#
# # 2. Set up constants to aid with describing the passage directions
# N, S, E, W = 1, 2, 4, 8
# IN         = 0x10
# FRONTIER   = 0x20
# OPPOSITE   = { E => W, W =>  E, N =>  S, S => N }
#
# # 3. Data structures and methods to assist the algorithm
# grid = Array.new(height) { Array.new(width, 0) }
# frontier = []
#
# def add_frontier(x, y, grid, frontier)
#   if x >= 0 && y >= 0 && y < grid.length && x < grid[y].length && grid[y][x] == 0
#     grid[y][x] |= FRONTIER
#     frontier << [x,y]
#   end
# end
#
# def mark(x, y, grid, frontier)
#   grid[y][x] |= IN
#   add_frontier(x-1, y, grid, frontier)
#   add_frontier(x+1, y, grid, frontier)
#   add_frontier(x, y-1, grid, frontier)
#   add_frontier(x, y+1, grid, frontier)
# end
#
# def neighbors(x, y, grid)
#   n = []
#
#   n << [x-1, y] if x > 0 && grid[y][x-1] & IN != 0
#   n << [x+1, y] if x+1 < grid[y].length && grid[y][x+1] & IN != 0
#   n << [x, y-1] if y > 0 && grid[y-1][x] & IN != 0
#   n << [x, y+1] if y+1 < grid.length && grid[y+1][x] & IN != 0
#
#   n
# end
#
# def direction(fx, fy, tx, ty)
#   return E if fx < tx
#   return W if fx > tx
#   return S if fy < ty
#   return N if fy > ty
# end
#
# # 4. Routines for displaying the maze
# def empty?(cell)
#   cell == 0 || cell == FRONTIER
# end
#
# def display_maze(grid)
#   print "\e[H" # move to upper-left
#   puts " " + "_" * (grid[0].length * 2 - 1)
#   grid.each_with_index do |row, y|
#     print "|"
#     row.each_with_index do |cell, x|
#       print "\e[41m" if cell == FRONTIER
#       if empty?(cell) && y+1 < grid.length && empty?(grid[y+1][x])
#         print " "
#       else
#         print((cell & S != 0) ? " " : "_")
#       end
#       print "\e[m" if cell == FRONTIER
#
#       if empty?(cell) && x+1 < row.length && empty?(row[x+1])
#         print((y+1 < grid.length && (empty?(grid[y+1][x]) || empty?(grid[y+1][x+1]))) ? " " : "_")
#       elsif cell & E != 0
#         print(((cell | row[x+1]) & S != 0) ? " " : "_")
#       else
#         print "|"
#       end
#     end
#     puts
#   end
# end
#
# # 5. Prim's algorithm
# mark(rand(width), rand(height), grid, frontier)
# until frontier.empty?
#   x, y = frontier.delete_at(rand(frontier.length))
#   n = neighbors(x, y, grid)
#   nx, ny = n[rand(n.length)]
#
#   dir = direction(x, y, nx, ny)
#   grid[y][x] |= dir
#   grid[ny][nx] |= OPPOSITE[dir]
#
#   mark(x, y, grid, frontier)
#
#   display_maze(grid)
#   sleep 0.01
# end
#
# display_maze(grid)
