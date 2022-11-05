# AUTHORS: Stephen Devaney, Amir Faiyaz, and Ucchwas Talukder
# FILENAME: nqueens.py
# SPECIFICATION: Generate the DIMACS CNF for the n-queens problem based on user input
# FOR: CS CS5384 Logic for Computer Scientists



import os



##################### Functions
def at_least_one(propositional_list):
    return_clause = ""
    for propositional_letter in propositional_list:
        return_clause += str(propositional_letter) + " "
    return return_clause + "0\n"

def at_most_one(propositional_list):
    return_clause = ""
    return_count = 0
    for i in range(0, len(propositional_list)):
        for j in range(i+1, len(propositional_list)):
            return_clause += "-" + str(propositional_list[i]) + " -" + str(propositional_list[j]) + " 0\n"
            return_count += 1
    return return_clause, return_count



##################### MAIN PROGRAM
# Recieve User Input (thinking of using both from console and from command line)
clause_count = 0
n = 4
total_spaces = n * n

# Open clause output file
with open("nqueens_clauses.txt", "w") as clause_temp_file:

    # GENERATE ROWS
    for i in range(1, total_spaces+1, n):
        p_list = []
        for j in range(i, n+i):
            p_list.append(j)
        clause_temp_file.write(at_least_one(p_list))
        clause, temp_count = at_most_one(p_list)
        clause_count += 1 + temp_count
        clause_temp_file.write(clause)

    # GENERATE COLUMNS
    for i in range(1,  n+1):
        p_list = []
        temp_clause = ""
        for j in range(i, total_spaces+i, n):
            p_list.append(j)
        clause_temp_file.write(at_least_one(p_list))
        clause, temp_count = at_most_one(p_list)
        clause_count += 1 + temp_count
        clause_temp_file.write(clause)

    # GENERATE DIAGONALES
    for i in range(1, n+1):
        p_list = []
        clause = ""
        for j in range(i, total_spaces+1, n-1):
            if(j == i*n):
                break
            p_list.append(j)
        temp_clause, temp_count = at_most_one(p_list)
        clause += temp_clause
        clause_count += temp_count
        p_list = []
        for j in range(i, total_spaces+1, n+1):
            if(j == i +(n+1)*(n+1-i)):
                break
            p_list.append(j)
        temp_clause, temp_count = at_most_one(p_list)
        clause += temp_clause
        clause_count += temp_count
        clause_temp_file.write(clause)

    for i in range(total_spaces, total_spaces-n, -1):
        clause = ""
        if i != total_spaces - n + 1:
            p_list = []
            for j in range(i, 0, -n+1):
                if(j == (i-(n*(n-1))-1) * n + 1 ):
                    break
                p_list.append(j)
            temp_clause, temp_count = at_most_one(p_list)
            clause += temp_clause
            clause_count += temp_count
        if i != total_spaces:
            p_list = []
            for j in range(i, 0, -n-1):
                if(j == i - (n+1) * (i-(n*(n-1))) ):
                    break
                p_list.append(j)
            temp_clause, temp_count = at_most_one(p_list)
            clause += temp_clause
            clause_count += temp_count
            clause_temp_file.write(clause)
    clause_temp_file.close()

# GENERATE CNF OUTPUT FILE
# open output file and reopen clause file
with open("nqueens_v1.cnf", "w") as outfile:
    with open("nqueens_clauses.txt", "r") as clause_temp_file:
        # Generate Starting Information for SatSolver
        outfile.write("c AUTHORS: Generated by nqueens.py that was developed by Stephen Devaney, Amir Faiyaz, and Ucchwas Talukder\n")
        outfile.write("c FILENAME: nqueens.cnf\n")
        outfile.write("c SPECIFICATION: SAT formula generated for " + str(n) + "-queens.\n")
        outfile.write("c FOR: CS5384 Logic for Computer Scientists\n")
        outfile.write("c Uses each position as a proposition letter on a " + str(n) + "x" + str(n) + " board.\n")
        outfile.write("c This gives us a total of " + str(total_spaces) + " total spaces.\n")
        outfile.write("p cnf " + str(total_spaces) + " " + str(clause_count) + "\n")

        #copy clause file to output file
        while True:
            line = clause_temp_file.readline()
            if not line:
                break
            outfile.write(line)
        clause_temp_file.close()
outfile.close()
os.remove("nqueens_clauses.txt")

# RUN MINISAT
os.system("./minisat nqueens_v1.cnf output.txt")
