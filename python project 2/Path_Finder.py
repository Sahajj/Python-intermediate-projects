import curses
from curses import wrapper
import queue
import time

maze = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]


def print_maze(maze, stdscr, path=[]):
    BLUE = curses.color_pair(1) #default maze as blue 
    RED = curses.color_pair(2) # and path as red

    for i, row in enumerate(maze): # enumerate will give me the index and the value of every one of these rows or nested arrays & i will be the current row i am on
        for j, value in enumerate(row): # row is my list, then i am enumerate the list that i have and grab the Column I'm currently on (j) & value == symbol in the column/maze
            if (i, j) in path:
                stdscr.addstr(i, j*2, "X", RED)
            else:
                stdscr.addstr(i, j*2, value, BLUE)


def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j

    return None


def find_path(maze, stdscr):
    start = "O"
    end = "X"
    start_pos = find_start(maze, start)

    q = queue.Queue()
    q.put((start_pos, [start_pos]))

    visited = set()

    while not q.empty():
        current_pos, path = q.get()
        row, col = current_pos
        
        stdscr.clear()
        print_maze(maze, stdscr, path)
        time.sleep(0.2)
        stdscr.refresh()

        if maze[row][col] == end:
            return path

        neighbors = find_neighbors(maze, row, col)
        for neighbor in neighbors:
            if neighbor in visited:
                continue

            r, c = neighbor
            if maze[r][c] == '#':
                continue

            new_path = path + [neighbor]
            q.put((neighbor, new_path))
            visited.add(neighbor)



def find_neighbors(maze, row, col):
    neighbors = []

    if row > 0: #UP
        neighbors.append((row - 1, col))
    if row + 1 < len(maze): #DOWN
        neighbors.append((row + 1, col))
    if col > 0: #LEFT
        neighbors.append((row, col - 1))
    if col + 1 < len(maze[0]): #RIGHT
        neighbors.append((row, col + 1))

    return neighbors



# Stdscr stands for standard output screen 
# and this is used to get o/p all the suff of our program
def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK) #we are creating a curse and then giving it an id 1 is the id of this curse and then we give color to the forground & the back ground.
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    find_path(maze, stdscr)
    stdscr.getch()  # Holds the screen till we exit it.
    # stdscr.clear() # Clear the whole screen 
    # # stdscr.addstr(5, 5, "Hello world", blue_and_black) # Addind a string at a position on the led/ terminal.
    # print_maze(maze, stdscr)
    # stdscr.refresh()  # Refreshsh the screen
    

# This intialize the curses module for us & then it calls the function
# passes this stdscr obejct and then we can use that in here to control our output.
wrapper(main)