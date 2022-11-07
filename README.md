# CS5384 N-Queens SATSOLVER
[GitHub Repository](https://github.com/stephencdevaney/TTU_CS5384_Logic_for_Computer_Scientists)

## Project Overview
This project generates a CNF file based on MINISAT for the n-queens problem. If 'minisat' is in the directory or path to SATSOLVER is
specified then CNF file will be ran through SATSOLVER and find first solution. If user indicates all solutions then all
solutions will be generated using a temp.cnf file that will be removed upon finishing the run.

## Project Development Environment
The project was developed using python IDLE and was interpreted using Python 3.6.8 and MINISAT 2.2.0. 
You can download python from https://www.python.org/ and MINISAT from http://minisat.se/MiniSat.html .

## Usage:
usage: nqueens_v2.py <options>

## Options:
  -h, --help            show this help message and exit
  -n NQUEENS, --nqueens NQUEENS
                        Sets the number of Queens to be ran through SAT Solver.
  -a {y,n}, --all {y,n}
                        Finds all solutions for the specified n-queens problem.
  -s SATSOLVER, --satsolver SATSOLVER
                        Change the location of the SAT solver. (Needed if .py script is not in same folder as SAT
                        SOLVER) NOTE: This program was built based on MINISAT. NOTE: to change the location must use
                        command line arguments