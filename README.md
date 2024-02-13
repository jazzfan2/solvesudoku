# Name: solvesudoku.py
solvesudoku.py - A solver for 9 x 9 type Sudoku problems.

# Description:
solvesudoku.py solves 9 x 9 type Sudoku problems by processing a text file with a 9-by-9 matrix of digits corresponding with the given and empty fields of the problem, and finds the missing digits by applying a recursive backtracking algorithm.

# How to use solvesudoku.py:
Fill the text file 'matrix.txt' by the given digits for fields in corresponding positions, and by zeroes 
if fields are empty, and place this file into the same directory as the program.

Then supply the simple command:

	./solvesudoku.py

In order to solve a 9 x 9 type Suduku problem with four additional 3 x 3 "grey square" zones, supply any extra argument to above command. 

# Author:
Written by Rob Toscani (rob_toscani@yahoo.com).
