#!/usr/bin/env python3
# Name  : solvesudoku_.py
# Author: Rob Toscani
# Date  : 17-11-2026
# Description: Solver for 9 x 9 type Sudoku problems.
# Fill the text file 'matrix.txt' by the given digits for fields in corresponding
# positions, and by zeros if fields are empty.
# To solve a 9 x 9 type Suduku problem with additional four 3 x 3 "grey square" zones,
# supply any extra argument.
#
###############################################################################
#
# Copyright (C) 2026 Rob Toscani <rob_toscani@yahoo.com>
#
# solvesudoku.py is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# solvesudoku.py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


import sys
import os
import time

alldigits = set([1,2,3,4,5,6,7,8,9])
solutions = 0

# Determine all possible digits for cell, given digits in its row, column, square(s):
def get_options(i, j, grid):
    column   = []
    row      = []
    square   = []
    graysquare = []
    for x in range(9):
        # Fill the list of (non-zero) digits found in cell row and column:
        column.append(grid[x][j])
        row.append(grid[i][x])
    # Determine index boundaries of square that cell belongs to:
    for p in range(((i>2)+(i>5))*3, ((i>2)+(i>5))*3+3):
        for q in range(((j>2)+(j>5))*3, ((j>2)+(j>5))*3+3):
            # Fill the list of (non-zero) digits found in square:
            square.append(grid[p][q])
    if len(sys.argv) > 1:
        # If gray squares are involved and cell belongs to any of them:
        if i not in (0,4,8) and j not in (0,4,8):
            # Determine index boundaries of gray square that cell belongs to:
            for p in range((i>4)*4+1, (i>4)*4+4):
                for q in range((j>4)*4+1, (j>4)*4+4):
                    # Fill the list of (non-zero) digits found in gray square:
                    graysquare.append(grid[p][q])
    # Return set of digits left as possible options for given cell:
    return alldigits - set(column + row + square + graysquare)


# Test if none of the columns, rows, squares & graysquares contain duplicates:
def end_test(grid):
    columns     = [ [] for x in range(9) ]
    rows        = [ [] for x in range(9) ]
    squares     = [ [] for x in range(9) ]
    graysquares = [ [] for x in range(4) ]
    for i in range(9):
        for j in range(9):
            columns[j].append(grid[i][j])
            rows[i].append(grid[i][j])
            squares[((i>2)+(i>5))*3+(j>2)+(j>5)].append(grid[i][j])
            if i not in (0,4,8) and j not in (0,4,8):
                graysquares[(i>4)*2+(j>4)].append(grid[i][j])
    for lis in columns + rows + squares + graysquares:
        if len(lis) != len(set(lis)):
            return False
    return True


# Solve current grid, given zero count, digit option & indices of cell in question:
def solve(grid, option, i_option, j_option, zerocount):
    global solutions
    grid = [list(x) for x in grid]  # Deep copying!
    # Fill given digit option in cell with given indices:
    if option > 0:
        grid[i_option][j_option] = option
    zerocount_prev = zerocount
    while True:
        # Initialize least options set to all 9 digits:
        least_options = alldigits
        # Initialize number of zeros:
        zerocount = 0
        # Loop though all remaining zero cells:
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    # Increment zero count:
                    zerocount += 1
                    # Determine all non-zero digit options possible for cell:
                    options = get_options(i, j, grid)
                    if len(options) == 1:
                        # Only one digit option found so cell must adopt this value:
                        (grid[i][j],) = options
                        zerocount -= 1
                    elif len(options) == 0:
                         # No possible solution w/ current digits so stop recursion:
                        return
                    else:
                        # >1 digit options, store (only) smallest set & associated cell:
                        if len(options) < len(least_options):
                            least_options = set(options)
                            i_least_options = i
                            j_least_options = j

#       Uncomment to see process steps:
#       for i in range(9):
#           print(grid[i])
#       time.sleep(0.1)
#       os.system('clear')

        if zerocount == 0:
            # No zeros present anymore, so if end test passes we have a (new) solution!
            if end_test(grid):
                solutions += 1
                for i in range(9):
                    # Print solved grid solution:
                    print(grid[i])
                print()
#               time.sleep(2)
#               os.system('clear')
#               Uncomment if only the first solution is desired:
#               sys.exit()
#           To next solution (total number could exceed 100000 !):
            return
        elif zerocount == zerocount_prev:
            # If there is no progression within the iteration ...
#           # Rebuild least_options *after* nested loop (takes duplicates case to test):
#           least_options = get_options(i_least_options, j_least_options, grid)
            for option in least_options:
                # Fork to recursions with all options of cell w/ least number of options:
                solve(grid, option, i_least_options, j_least_options, zerocount_prev)
            return
        else:
            zerocount_prev = zerocount

grid = []
with open('matrix.txt') as f:
    for line in f.readlines():
        if line == '\n':
            continue
        # Fill grid with digit pattern found in text matrix:
        grid.append([int(i) for i in str(line)[0:9]])
    # Count initial number of zeros in grid:
    zerocount = f.read().count('0')

# Send grid to solver:
solve(grid, 0, 0, 0, zerocount)

# Print number of solutions:
print(solutions)
