# AUTHORS: Stephen Devaney
# FILENAME: nqueens.py
# SPECIFICATION: Generate the DIMACS CNF for the n-queens problem based on user input
# FOR: CS CS5384 Logic for Computer Scientists

import os
    

##################### MAIN PROGRAM
# Recieve User Input (thinking of using both from console and from command line)
clause_count = 0
n = 4
total_spaces = n * n

# Open clause output file
with open("nqueens_clauses.txt", "w") as clause_temp_file:


    # GENERATE ROWS
    for i in range(1, total_spaces+1, n):
        temp_clause = ""
        for j in range(i, n+i):
            temp_clause += str(j) + " "
        clause_temp_file.write(temp_clause + "0\n")
        clause_count += 1
        for j in range(i, n+i):
            for k in range(j, n+i):
                if(j != k):
                    clause_temp_file.write("-" + str(j) + " -" + str(k) + " 0\n")
                    clause_count += 1

    # GENERATE COLUMNS
    for i in range(1,  n+1):
        temp_clause = ""
        for j in range(i, total_spaces+i, n):
            temp_clause += str(j) + " "
        clause_temp_file.write(temp_clause + "0\n")
        clause_count += 1
        for j in range(i, total_spaces+i, n):
            for k in range(j, total_spaces+i, n):
                if(j != k):
                    clause_temp_file.write("-" + str(j) + " -" + str(k) + " 0\n")
                    clause_count += 1

    # GENERATE DIAGONALES

    clause_temp_file.close()


# GENERATE FINAL OUTPUT FILE
# open output file and reopen clause file
with open("nqueens.txt", "w") as outfile:
    with open("nqueens_clauses.txt", "r") as clause_temp_file:
        # Generate Starting Information for SatSolver
        outfile.write("c SAT formula for " + str(n) + "-queens.\n")
        outfile.write("c Use each position as a proposition letter on a " + str(n) + "x" + str(n) + " board.\n")
        outfile.write("c This gives us a total of " + str(total_spaces) + " total spaces.\n")
        outfile.write("p CNF " + str(total_spaces) + ", " + str(clause_count) + "\n")

        #copy clause file to output file
        while True:
            line = clause_temp_file.readline()
            if not line:
                break
            outfile.write(line)
        clause_temp_file.close()
outfile.close()
os.remove("nqueens_clauses.txt")
