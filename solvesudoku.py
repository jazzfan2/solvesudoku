#!/usr/bin/env python3
# Name  : solvesudoku.py
# Author: Rob Toscani
# Date  : 13-11-2026
# Description: Solver for 9 x 9 type Sudoku problems.
# Fill the text file 'matrix.txt' by the given digits for fields in corresponding 
# positions, and by zeroes if fields are empty.
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
 
alldigits = set([1,2,3,4,5,6,7,8,9])
solutions = 0
 
def duplicates(list_of_lists):
    for lis in list_of_lists:
        lis = [x for x in lis if x != 0]
        if len(lis) != len(set(lis)):
            return True
    return False
 
def solve(grid,depth,option,i_min_options,j_min_options):
    global solutions
    grid = [list(x) for x in grid]  # Deep copying!
    if depth > 0:
        grid[i_min_options][j_min_options] = option
    zerocount_prev = 100
    min_options = alldigits
    while True:
        zerocount = 0
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    zerocount += 1
                    vlist   = []
                    hlist   = []
                    sqlist  = []
                    gsqlist = []
                    for x in range(9):
                        vlist.append(grid[x][j])
                        hlist.append(grid[i][x])
                    for p in range(i//3*3,i//3*3+3):
                        for q in range(j//3*3,j//3*3+3):
                            sqlist.append(grid[p][q])
                    if len(sys.argv) > 1:
                        if i not in (0,4,8) and j not in (0,4,8):
                            for p in range(i//4*4+1,i//4*4+4):
                                for q in range(j//4*4+1,j//4*4+4):
                                    gsqlist.append(grid[p][q])
                    if duplicates([vlist, hlist, sqlist, gsqlist]):
                        return
                    options = alldigits - set(vlist + hlist + sqlist + gsqlist)
                    if len(options) == 1:
                        (grid[i][j],) = options
                    elif len(options) == 0:
                        return
                    else:
                        if len(options) < len(min_options):
                            min_options = set(options)
                            i_min_options = i
                            j_min_options = j
        if zerocount == 0:
            solutions += 1 
            for i in range(9):
                print(grid[i])
            print(); return         # For all solutions (total number could exceed 100000 !)
#           sys.exit()              # Only for the first solution
        elif zerocount == zerocount_prev:
            depth_plus1 = depth + 1
            for option in min_options:
                solve(grid,depth_plus1,option,i_min_options,j_min_options)
            return
        else:
            zerocount_prev = zerocount
count = 0
grid = []
f = open('matrix.txt')
for line in f.readlines():
    if not line:
        break
    count += 1
    grid.append([int(i) for i in str(line)[0:9]])
    if count == 9:
        solve(grid,0,0,0,0)
f.close()
# Print number of solutions:
print(solutions)

