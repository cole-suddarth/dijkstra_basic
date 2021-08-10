'''
File: dijkstra_on_grid.py
Author: Cole Suddarth
Purpose: To solver a maze using djikstras algorithim, given
   that the first time the point is reached is the fastest route
'''
# from os import read
from typing import Text
from dijkstra_node import *

def read_file():
    '''
    This function asks the user for a file to read and opens said file,
    reading it and determining if there is a # or space to create a dijkstra
    node or append None. It then returns a 2d list of nones and nodes
    Arguments: None
    Return: total_grid is a 2d array representing the maze grid, and is
       filled with Nones and nodes
    Assumptions: the file name is valid and openable, filled with '#' or ' '
    '''
    print('Please give the grid file: ')
    file_name = input()
    file_name = file_name.lstrip().rstrip()
    file = open(file_name)

    total_grid = []
    line_length = 0
    for line in file:
        line = line.strip('\n')
        line_length = max(len(line), line_length)
        row = []
        # creates a row of spaces and dijkstra nodes
        for char in line:
            # dijkstranode if there is a #, else None
            if char == '#':
                row.append(DijkstraNode())
            else:
                row.append(None)
        # create 2d-array
        total_grid.append(row)

        # if a row does not have anough entries append None to end
        # so all rows are the same length in total_grid
        for i in range(len(total_grid)):
            while len(total_grid[i]) <= line_length:
                total_grid[i].append(None)

    return total_grid

def print_map(total_grid):
    '''
    This funcion prints the maps, or grid of the file. It works given the
        animate and fill statuses.
    Arguments: total_grid is a 2d array filled with either none or dijkstra
        nodes
    Returns: None
    Assumptions: total_grid is either filled with None or dijkstra nodes
    '''
    for row in total_grid:
        for elem in row:
            # if elem is node and been confirmed print number
            if elem and elem.is_done():
                if elem.get_dist() < 10:
                    print(' ' + str(elem.get_dist()) + ' ', end='')
                else:
                    print(str(elem.get_dist()) + ' ', end='')
            # if elem is node and been reached not confirmed print num + ?
            elif elem and elem.is_reached():
                if elem.get_dist() < 10:
                    print(' ' + str(elem.get_dist()) + '?', end='')
                else:
                    print(str(elem.get_dist()) + '?', end ='')
            # if node but never reached print #
            elif elem:
                print(' # ', end = '')
            # if no node, empty space print 3 empty spaces
            else:
                print('   ', end = '')
        print('\n', end='')

def queue_adjustment(total_grid, x, y, todo):
    '''
    This function adjusts the queue and each dijkstra node when reached
    It uses the first point in the queue and checks for adjacent nodes,
    and then removes that point from the queue.
    Arguments: total_grid is 2d-array representing the grid of None and nodes
        x and y are integers
    Return: todo is a list which containts tuples structred such as
        (distance, x, y) which points have yet to be confirmed
    '''
    # if the first element: todo is None, initalize todo list
    if todo is None:
        cur_node = total_grid[y][x]
        cur_node.update_dist(0)
        todo = [ (cur_node.get_dist(),  x, y) ]
        # once distance is updated, it says that it has been reached

    # todo list exists and needs to be manipulated
    else:
        cur_x = todo[0][1]
        cur_y = todo[0][2]
        cur_node = total_grid[cur_y][cur_x]

        # check left for new node
        if cur_x != 0 and total_grid[cur_y][cur_x-1]:
            left = total_grid[cur_y][cur_x-1]
            if not left.is_reached():
                # update distance
                left.update_dist(cur_node.get_dist() + 1)
                # add to todo list
                todo.append( (left.get_dist(), cur_x-1, cur_y) )

        # check right for new node
        if cur_x != (len(total_grid[0])-1) and total_grid[cur_y][cur_x+1]:
            right = total_grid[cur_y][cur_x+1]
            if not right.is_reached():
                # update distance
                right.update_dist(cur_node.get_dist() + 1)
                # add to todo list
                todo.append( (right.get_dist(), cur_x+1, cur_y) )

        # check above for new node
        if cur_y != 0 and total_grid[cur_y-1][cur_x]:
            above = total_grid[cur_y-1][cur_x]
            if not above.is_reached():
                # update distance
                above.update_dist(cur_node.get_dist() + 1)
                # add to todo list
                todo.append( (above.get_dist(), cur_x, cur_y-1) )

        # check below for new node
        if cur_y != (len(total_grid)-1) and total_grid[cur_y+1][cur_x]:
            below = total_grid[cur_y+1][cur_x]
            if not below.is_reached():
                # update distance
                below.update_dist(cur_node.get_dist() + 1)
                # add to todo list
                todo.append( (below.get_dist(), cur_x, cur_y+1) )

        cur_node.set_done()
        todo.pop(0)  # pop the first element in queue

    return sorted(todo)

def main():
    '''
    This function asks the user for operation and staritng coordinates.
    It then runs the program and depending on whether animate or fill is
    chosen it prints every step of the solving or only the final solution.
    Arguments: None
    Return: None
    Assumptions: all inputs are valid, and command is either animate or fill
    '''
    total_grid = read_file()

    print('Where to start?')
    coord = input()
    coord = coord.lstrip().rstrip().split(' ')
    x, y = int(coord[0]), int(coord[1])
    print('What type of operation?')
    command = input()
    command = command.lstrip().rstrip()

    # if animating print the starting grid
    if command == 'animate':
        print('Searching from (' + str(x) + ',' + str(y) + ') outward.\n')
        print('STARTING GRID:')
        print_map(total_grid)
        print()

    # initalize the todo queue, such that queue starts at None
    todo = queue_adjustment(total_grid, x, y, None)

    # while the todo queue is not empty
    while todo != []:
        # if animating print the grid and todo list at each step
        if command == 'animate':
            print('CURRENT GRID:')
            print_map(total_grid)
            print('\nTODO list:', todo)
            print()

        # perform actual algorithim
        todo = queue_adjustment(total_grid, x, y, todo)

    # if animating print that all spaces are filled
    if command == 'animate':
        print('-------- All reachable spaces filled.  This is \
the final map --------')

    print_map(total_grid)

main()