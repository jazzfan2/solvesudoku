#!/usr/bin/env python2
# Name  : solvesudoku.py
# Author: Rob Toscani
# Date  : 15-01-2017
# Description: Solver for 9 x 9 type Sudoku problems.
# Fill the text file 'matrix.txt' by the given digits for fields in corresponding 
# positions, and by zeroes if fields are empty.
# To solve a Suduku type with four 3 x 3 "grey square" zones, supply any extra argument. 
# 
###############################################################################
#
# Copyright (C) 2024 Rob Toscani <rob_toscani@yahoo.com>
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
#
import sys
import os
import time
#
alldigits = set([1,2,3,4,5,6,7,8,9])
solutions = set()
#
def view(grid):
    for q in xrange(9):
        print grid[q]
    time.sleep(0.02)
    os.system('clear')
#
def solve(grid,depth,option,i_min_options,j_min_options):
    grid = [list(x) for x in grid]					# Diep kopieren!
    if depth > 0:
        grid[i_min_options][j_min_options] = option
    zerocount_prev = 100
    min_options = alldigits
    while True:
#        view(grid)
        zerocount = 0
        string = ""
        for i in xrange(9):
            for j in xrange(9):
                string += str(grid[i][j])
                if grid[i][j] == 0:
                    zerocount += 1
                    vset = set()
                    hset = set()
                    sqset = set()
                    gsqset = set()
                    for x in xrange(9):
                        vset.add(grid[x][j])
                        hset.add(grid[i][x])
                    for p in xrange(i/3*3,i/3*3+3):
                        for q in xrange(j/3*3,j/3*3+3):
                            sqset.add(grid[p][q])
                    if len(sys.argv) > 1:
                        if i not in (0,4,8) and j not in (0,4,8):
                            for p in xrange(i/4*4+1,i/4*4+4):
                                for q in xrange(j/4*4+1,j/4*4+4):
                                    gsqset.add(grid[p][q])
                    options = alldigits - (vset | hset | sqset | gsqset)
                    if len(options) == 1:
                        grid[i][j] = int(list(options)[0])
                    elif len(options) == 0:
                        return
                    else:
                         if len(options) < len(min_options):
                            min_options = set(options)
                            i_min_options = i
                            j_min_options = j
        if zerocount == 0:
            solutions.add(string) 
            for i in xrange(9):
                print grid[i]
            print; return			# Voor alle oplossingen (dit kunnen er > 100000 zijn !).
#            sys.exit()				# Voor alleen de eerste oplossing.
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
# print solutions
print len(solutions)				# Aantal oplossingen

