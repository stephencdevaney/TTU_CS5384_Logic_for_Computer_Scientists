Generates CNF file based on MINISAT for the n-queens problem. If 'minisat' is in the directory or path to SATSOLVER is
specified then CNF file will be ran through SATSOLVER and find first solution. If user indicates all solutions then all
solutions will be generated using a temp.cnf file that will be removed upon finishing the run.

usage:
usage: nqueens_v2.py <options>

options:
  -h, --help            show this help message and exit
  -n NQUEENS, --nqueens NQUEENS
                        Sets the number of Queens to be ran through SAT Solver.
  -a {y,n}, --all {y,n}
                        Finds all solutions for the specified n-queens problem.
  -s SATSOLVER, --satsolver SATSOLVER
                        Change the location of the SAT solver. (Needed if .py script is not in same folder as SAT
                        SOLVER) NOTE: This program was built based on MINISAT. NOTE: to change the location must use
                        command line arguments