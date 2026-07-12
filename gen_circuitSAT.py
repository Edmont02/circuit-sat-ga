import random

# this function randomly generates clauses for the genetic algorithm + WoC apporach hybrid algorithm to solve the CSAT problem
# it takes in a number of variables and the number of clauses and outputs a set of these generated clauses
def create_probs(num_vars, num_clauses):
    clauses = []
    
    for _ in range(num_clauses):
        clause = []
        # has 3 literals
        for _ in range(3):
            var = random.randint(1, num_vars)
            if random.random() < 0.5:
                # a positive literal
                literal = var
            else:
                # a negative literal
                literal = -var
                # appends the literal to the clause
            clause.append(literal)
        # appends the clause to the list of clauses
        clauses.append(clause)

    # prints out the number of variables and clauses in the first line of the text file
    print(f"{num_vars} {num_clauses}")
    
    # this for loop prints out the clauses which will be copied and put into a text file to be used in the hybrid algorithm
    for clause in clauses:
        print(" ".join(map(str, clause)))

    return clauses

if __name__ == '__main__':
    # function call to create_probs to generate clauses for algorithm
    # create_probs(10, 20)
    # create_probs(20, 40)
    # create_probs(40, 60)
    # create_probs(60, 80)
    # create_probs(80, 100)
    create_probs(100,200)
