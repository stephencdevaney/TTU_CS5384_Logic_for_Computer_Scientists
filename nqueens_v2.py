# AUTHORS: Stephen Devaney, Amir Faiyaz, and Ucchwas Talukder
# FILENAME: nqueens_v2.py
# SPECIFICATION: Generate the DIMACS CNF for the n-queens problem based on user input and if able runs SATSOLVER over solution
# FOR: CS5384 Logic for Computer Scientists



# Import needed libraries 
import os
import sys
import argparse



##################### Functions
def at_least_one(propositional_list):
    # Name: at_least_one
    # Input: propositional_list: List of propositional letters 
    # Output: return_clause: clause that define at least one of the propositional letters are true
    # Purpose: takes in a list of propositional letters and out puts a clause that represent at least one of the propositional letters are true (ie. $P0 \vee P1 \vee ... \vee Pn$) in DIMACs CNF
    return_clause = ""
    for propositional_letter in propositional_list:
        return_clause += str(propositional_letter) + " "
    return return_clause + "0\n"

def at_most_one(propositional_list):
    # Name: at_most_one
    # Input: propositional_list: List of propositional letters 
    # Output: return_clause: clause that define at most one of the propositional letters are true
    # Purpose: takes in a list of propositional letters and out puts a clause that represent at most one of the propositional letters are true (ie. $P0 \rightarrow \neg P1$ or $\neg P0 \vee \neg P1$) in DIMACs CNF
    return_clause = ""
    return_count = 0
    for i in range(0, len(propositional_list)):
        for j in range(i+1, len(propositional_list)):
            return_clause += "-" + str(propositional_list[i]) + " -" + str(propositional_list[j]) + " 0\n"
            return_count += 1
    return return_clause, return_count

def flip_solution(solution):
    # Name: flip_solution
    # Input: solution: DIMACs CNF solution string
    # Output: solution_string: new solution string that is the inverse of solution
    # Purpose: takes in a list of propositional letters and out puts a clause that represent at most one of the propositional letters are true (ie. $P0 \rightarrow \neg P1$ or $\neg P0 \vee \neg P1$) in DIMACs CNF
    solution_string = ""
    solution_list = solution.strip().split(" ")
    for letter in solution_list:
        if letter[0].isdigit() and letter[0] != '0':
            solution_string += "-" + letter + " "
        elif letter[0] == '0':
            solution_string += letter
        else:
            solution_string += letter[1:] + " "
    return solution_string + "\n"

def convert_index_to_letter(row_index, column_index, spaces_per_row):
    # Name: convert_index_to_letter
    # Input: row: current row, column: current column, spaces_per_row: number of spaces one each row
    # Output: the propositional letter based off the index
    # Purpose: takes in a row and column index and converts it to a propositional letter based off the index and number of values per row ie n
    return row_index*spaces_per_row + column_index + 1



##################### MAIN PROGRAM
# Setup default variables
ALL_SOLUTIONS = False
clause_count = 0
SATSOLVER = "./minisat.exe"

# Recieve User Input (ggiving the user to pass arguments from console or from command line)
# Setup arg parser
parser = argparse.ArgumentParser(description = "Generate CNF file based on MINISAT for the n-queens problem. If 'minisat' is in the directory or path to 'minisat' is specified then CNF file will be ran through minisat and find first solution. If user indicates all solutions then all solutions will be generated using a temp.cnf file that will be removed upon finishing the run.")
parser.add_argument("-n", "--nqueens", type=int, help = "Sets the number of Queens to be ran through SAT Solver.")
parser.add_argument("-a", "--all", choices = ["y", "n"], help = "Finds all solutions for the specified n-queens problem.")
parser.add_argument("-s", "--satsolver", help = "Change the location of the SAT solver. (Needed if .py script is not in same folder as SAT SOLVER) NOTE: This program was built based on MINISAT. NOTE: to change the location must use command line arguments")
args = parser.parse_args()

#Check if args were pass from the command line if they were not ask for input from the user on the console
if args.nqueens:
    n = args.nqueens
else:
    while True:
        n = input("Enter number of queens: ")
        if n.lower() == "exit":
            sys.exit()
        if n.isdigit():
            n = int(n)
            break
        else:
            print("\nInvalid arguement for number of queens, arguement requires an integer! Type 'exit' to end the program.")
if args.all:
    if args.all == 'y':
        ALL_SOLUTIONS = True
else:
    while True:
        all_query = input("Would you like the SAT solver to find all solutions (y/n): ")
        if all_query.lower() == "exit":
            sys.exit()
        if all_query.lower() == "yes" or all_query.lower() == "y":
            ALL_SOLUTIONS = True
            break
        elif all_query.lower() == "no" or all_query.lower() == "n":
            break 
        else:
            print("\nInvalid arguement for query, arguement requires yes or y for 'yes' and no or n for 'no'! Type 'exit' to end the program.")    
if args.satsolver:
    SATSOLVER = args.satsolver

# Setup total spaces for cnf file output
total_spaces = n * n

# Open clause output file
with open("nqueens_clauses.txt", "w") as clause_temp_file:
    print("Generating nqueens_v1.cnf!")

    # GENERATE ROWS
    for row in range(0, n):  # generate rows based off of indexes
        p_list = []
        for column in range(0, n):
            p_list.append(convert_index_to_letter(row, column, n))  # convert index to propositonal letter and append to list
        clause_temp_file.write(at_least_one(p_list))  # call at least one and write output to file
        clause, temp_count = at_most_one(p_list)  # call at most one 
        clause_count += 1 + temp_count
        clause_temp_file.write(clause)  # write at most one to a file

    # GENERATE COLUMNS
    for column in range(0, n):  # generate columns based off of indexes
        p_list = []
        for row in range(0, n):
            p_list.append(convert_index_to_letter(row, column, n))  # convert index to propositonal letter and append to list
        clause_temp_file.write(at_least_one(p_list))  # call at least one and write output to file
        clause, temp_count = at_most_one(p_list)  # call at most one 
        clause_count += 1 + temp_count
        clause_temp_file.write(clause)  # write at most one to a file

    # GENERATE DIAGONALES
    for column in range(0, n):  # generate first set of diagonals from the bottem row
        p_list = []
        clause = ""
        for row in range(0, column+1):  # generate left diagonals and append them to list
            p_list.append(convert_index_to_letter(row, column-row, n))
        temp_clause, temp_count = at_most_one(p_list)  # call at most one 
        clause += temp_clause
        clause_count += temp_count
        p_list = []
        for row in range(0, n-column):  # generate right diagonals and append them to list
            p_list.append(convert_index_to_letter(row, column+row, n))
        temp_clause, temp_count = at_most_one(p_list)  # call at most one 
        clause += temp_clause
        clause_count += temp_count
        clause_temp_file.write(clause)  # write both at most one clauses to a file

    for column in range(n-1, -1, -1):  # generate first set of diagonals from the top row
        clause = ""
        if(column != 0):  # since far left diagonal has already been generated skip this diagonal
            p_list = []
            for row in range(n-1, column-1, -1):  # generate right diagonals and append them to list
                p_list.append(convert_index_to_letter(row, column+n-1-row, n))
            temp_clause, temp_count = at_most_one(p_list)  # call at most one 
            clause += temp_clause
            clause_count += temp_count
        if(column != n-1):  # since far right diagonal has already been generated skip this diagonal
            p_list = []
            for row in range(n-1, n-column-2, -1):  # generate left diagonals and append them to list
                p_list.append(convert_index_to_letter(row, column-n+1+row, n))
            temp_clause, temp_count = at_most_one(p_list)  # call at most one 
            clause += temp_clause
            clause_count += temp_count 
        clause_temp_file.write(clause)  # write both at most one clauses to a file

# GENERATE FINAL CNF OUTPUT FILE
# open output file and reopen clause file
with open("nqueens_v1.cnf", "w") as outfile:  # open final outputfile
    with open("nqueens_clauses.txt", "r") as clause_temp_file:  # open file clauses were written in
        # Generate Starting Information for SatSolver and place in final output file
        outfile.write("c AUTHORS: Generated by nqueens.py that was developed by Stephen Devaney, Amir Faiyaz, and Ucchwas Talukder\n")
        outfile.write("c FILENAME: nqueens.cnf\n")
        outfile.write("c SPECIFICATION: SAT formula generated for " + str(n) + "-queens.\n")
        outfile.write("c FOR: CS5384 Logic for Computer Scientists\n")
        outfile.write("c Uses each position as a proposition letter on a " + str(n) + "x" + str(n) + " board.\n")
        outfile.write("c This gives us a total of " + str(total_spaces) + " total spaces.\n")
        outfile.write("p cnf " + str(total_spaces) + " " + str(clause_count) + "\n")

        #copy contents from the file clauses were written in to final output file
        while True:
            line = clause_temp_file.readline()
            if not line:
                break
            outfile.write(line)
        clause_temp_file.close()
    outfile.close()
os.remove("nqueens_clauses.txt")
print("nqueens_v1.cnf file generated!")


# RUN MINISAT
if(os.path.exists(SATSOLVER)):  # if path to the SATSOLVER is correct run SATSOLVER
    os.system(SATSOLVER + " nqueens_v1.cnf output.txt")
    # if all solutions are requested then recursively run minisat solver with updated cnf file
    if ALL_SOLUTIONS:
        # check if first solution is satisifable if so write to all solutions file and generate temp.cnf file
        sat = False
        solution_count = 0
        with open("output.txt", "r") as satfile:
            with open("all_solutions.txt", "w") as solfile:
                if satfile.readline().strip() == "SAT": # if the first solution is satisifable
                    line = satfile.readline()
                    satfile.close()
                    sat = True
                    # generate all solutions file
                    solfile.write("All Satisifable Solutions:\n")
                    #generate tempfile
                    os.system("cp nqueens_v1.cnf temp.cnf")
                    with open("temp.cnf", "r") as tempfile1:
                        with open("temp2.cnf", "w") as tempfile2:
                            # copy contents without the old header
                            templine = tempfile1.readline()
                            flag = False
                            while True:
                                if not templine: # skip old header
                                    break
                                if templine[0].isdigit() or templine[0] == "-":
                                    if not flag: # first line in the temp2 file add new header otherwise copy clauses
                                        flag = True
                                        solution_count += 1
                                        tempfile2.write("p cnf " + str(total_spaces) + " " + str(clause_count + solution_count) + "\n")
                                    tempfile2.write(templine)
                                templine = tempfile1.readline()
                            tempfile2.write(flip_solution(line))
                            tempfile2.close()
                        tempfile1.close()
                        os.system("mv temp2.cnf temp.cnf")  # overwrite old temp file with tempfile2 and rename tempfile 2
                    solfile.write(line)
                else:  # if first solution is not satisifable write in all solutions file
                    solfile.write("NO SATISIFABLE SOLUTIONS!")
                solfile.close()

        # if first solution is satisfactory write recursivly run SATSOLVER to generate all solotions and write to all solutions file. Regenerate temp.cnf file
        while sat:
            os.system(SATSOLVER + " temp.cnf output.txt")
            with open("output.txt", "r") as satfile:
                with open("all_solutions.txt", "a") as solfile:
                    if satfile.readline().strip() == "SAT":  # if the current solution is satisifable
                        # update all solutions file
                        line = satfile.readline()
                        solfile.write(line)
                        satfile.close()
                        solfile.close()
                        # Regenerate tempfile
                        with open("temp.cnf", "r") as tempfile1:
                            with open("temp2.cnf", "w") as tempfile2:
                                # copy contents without the old header
                                templine = tempfile1.readline()
                                flag = False
                                while True:  
                                    if not templine:  # skip old header
                                        break
                                    if templine[0].isdigit() or templine[0] == "-":
                                        if not flag:  # first line in the temp2 file add new header otherwise copy clauses
                                            flag = True
                                            solution_count += 1
                                            tempfile2.write("p cnf " + str(total_spaces) + " " + str(clause_count + solution_count) + "\n")
                                        tempfile2.write(templine)
                                    templine = tempfile1.readline()
                                tempfile2.write(flip_solution(line))
                                tempfile2.close()
                            tempfile1.close()
                            os.system("mv temp2.cnf temp.cnf")  # overwrite old temp file with tempfile2 and rename tempfile 2
                    else:  # after reaching last solution output count and break loop
                        sat = False
                        solfile.write("\nTotal number of solutions: " + str(solution_count))
                        solfile.close()
        os.system("rm temp.cnf")  # remove temp file
        os.system("rm output.txt")  # if we are generating all solutions remove final output file
else:  # if sat solver path is incorrect inform user
    print("Sat solver does not exist at " + SATSOLVER + " nqueens_v1.cnf was not ran through the SAT solver.")
