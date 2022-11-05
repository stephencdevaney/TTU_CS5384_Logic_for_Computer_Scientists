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

def convert_index_to_letter(row_index, column_index, values_per_row):
    return row_index*values_per_row + column_index + 1



##################### MAIN PROGRAM
# Recieve User Input (thinking of using both from console and from command line)
clause_count = 0
n = 4
total_spaces = n*n

# Open clause output file
with open("nqueens_clauses.txt", "w") as clause_temp_file:

    # GENERATE ROWS
    for row in range(0, n):
        p_list = []
        for column in range(0, n):
            p_list.append(convert_index_to_letter(row, column, n))
        clause_temp_file.write(at_least_one(p_list))
        clause, temp_count = at_most_one(p_list)
        clause_count += 1 + temp_count
        clause_temp_file.write(clause)

    # GENERATE COLUMNS
    for column in range(0, n):
        p_list = []
        for row in range(0, n):
            p_list.append(convert_index_to_letter(row, column, n))
        clause_temp_file.write(at_least_one(p_list))
        clause, temp_count = at_most_one(p_list)
        clause_count += 1 + temp_count
        clause_temp_file.write(clause)

    # GENERATE DIAGONALES
    for column in range(0, n):
        p_list = []
        clause = ""
        for row in range(0, column+1):
            p_list.append(convert_index_to_letter(row, column-row, n))
        temp_clause, temp_count = at_most_one(p_list)
        clause += temp_clause
        clause_count += temp_count
        p_list = []
        for row in range(0, n-column):
            p_list.append(convert_index_to_letter(row, column+row, n))
        temp_clause, temp_count = at_most_one(p_list)
        clause += temp_clause
        clause_count += temp_count
        clause_temp_file.write(clause)

    for column in range(n-1, -1, -1):
        clause = ""
        if(column != 0):
            p_list = []
            for row in range(n-1, column-1, -1):
                p_list.append(convert_index_to_letter(row, column+n-1-row, n))
            temp_clause, temp_count = at_most_one(p_list)
            clause += temp_clause
            clause_count += temp_count
        if(column != n-1):
            p_list = []
            for row in range(n-1, n-column-2, -1):
                p_list.append(convert_index_to_letter(row, column-n+1+row, n))
            temp_clause, temp_count = at_most_one(p_list)
            clause += temp_clause
            clause_count += temp_count 
        clause_temp_file.write(clause)

# GENERATE FINAL OUTPUT FILE
# open output file and reopen clause file
with open("nqueens_v2.txt", "w") as outfile:
    with open("nqueens_clauses.txt", "r") as clause_temp_file:
        # Generate Starting Information for SatSolver
        outfile.write("c AUTHORS: Generated by nqueens.py that was developed by Stephen Devaney, Amir Faiyaz, and Ucchwas Talukder\n")
        outfile.write("c FILENAME: nqueens.cnf\n")
        outfile.write("c SPECIFICATION: SAT formula generated for " + str(n) + "-queens.\n")
        outfile.write("c FOR: CS5384 Logic for Computer Scientists\n")
        outfile.write("c Uses each position as a proposition letter on a " + str(n) + "x" + str(n) + " board.\n")
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
