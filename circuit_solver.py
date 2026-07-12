import time
import random
import matplotlib.pyplot as plt

# reads a text file that contains the data for the clauses and returns them as a tuple
def read_file(file):
    # read in the data from the file
    with open(file, 'r') as f:
        # the first line in text file contains the number of variables and the number of clauses
        num_vars, num_clauses = map(int, f.readline().split())
        clauses = []
        for line in f:
            clause = list(map(int, line.split()))
            clauses.append(clause)
    return num_vars, clauses
    
# creates an initial population with random binary values for each variable
def initial_pop(pop_size, num_vars):
    # initialize a set for the initial population of potential solutions
    population = []
    # creates clauses and adds them to chromosome set to which the potential solutions are added to the population set
    for _ in range(pop_size):
        chromosome = []
        for _ in range(num_vars):
            # randomly assigns True or False
            gene = random.choice([0, 1])
            chromosome.append(gene)
        population.append(chromosome)
    return population 

# evalutes the fitness of a potential solution and reports back a sorted list of clauses from fittest to least fit
def fitness(chromosomes, clauses, logic_type):
    fitness_scores = []
    # for loop looks at each clause within the chromosomes set
    for chromosome in chromosomes:
        # initializing the number of satisfied clauses to zero
        satisfied_clauses = 0

        # for loop looks over each clause in the problem
        for clause in clauses:
            # for 'OR' -- any literal being satisfied makes the clause satisfied
            if logic_type == "OR":
                clause_satisfied = any(
                    # literal is positive and the corresponding variable is True (1)
                    (lit > 0 and chromosome[abs(lit) - 1] == 1) or
                    # literal is negative and the corresponding variable is False (0)
                    (lit < 0 and chromosome[abs(lit) - 1] == 0)
                    # this iterates over all literals in the current clause
                    for lit in clause
                    )
            # for 'AND' -- all literals must be satisfied for the clause to be satisfied
            elif logic_type == "AND":
                clause_satisfied = all(
                    # literal is positive and the corresponding variable is True (1)
                    (lit > 0 and chromosome[abs(lit) - 1] == 1) or
                    # literal is negative and the corresponding variable is False (0)
                    (lit < 0 and chromosome[abs(lit) - 1] == 0)
                    # this iterates over all literals in the current clause
                    for lit in clause
                    )
            # for 'NOT' -- checks that the negatiion of the literal is satisfied
            elif logic_type == "NOT":
                clause_satisfied = any(
                    # negative literal should be True
                    (lit < 0 and chromosome[abs(lit) - 1] == 1) or
                    # positive literal should be False
                    (lit > 0 and chromosome[abs(lit) - 1] == 0)
                    # this iterates over all literals in the current clause
                    for lit in clause
                    )

            # increments the satisfied_clauses by 1 any time a clause is satisfied
            if clause_satisfied:
                satisfied_clauses += 1

        # appends the current chromosome and the number of satisfied clauses to the fitness_scores list
        fitness_scores.append((chromosome, satisfied_clauses))
    # sorts the fitness_score list from the fittest in the front (greater number of satisfied clauses) to the least fit in the back
    fitness_scores.sort(key=lambda x: x[1], reverse=True)

    return fitness_scores    

# takes in two parents and returns two children
def crossover(parent1, parent2):
    # both of the parents should be of the same length so only one parent length is needed
    length = len(parent1)
    # chooses a random crossover point
    crossover_point = random.randint(1, length - 1)
    # combines the parents at their crossover points to create two new solutions/children
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    
    return child1, child2

# appplies mutations to the given chromosome based on the mutation rate provided by the genetic algorithm
def mutation(chromosome, mutation_rate):
    # initializes a list to store the mutated chromosome
    mutated_chromosome = []
    # loops through each variable in the possible solution
    for gene in chromosome:
        # randomly decides if the gene should mutate
        if random.random() <= mutation_rate:
            # flips the bit value (changes 0 to 1, or 1 to 0)
            mutated_chromosome.append(1 - gene)
        else:
            # if no mutation occurs, keeps the original variable
            mutated_chromosome.append(gene)

    return mutated_chromosome

# a genetic algorithm with a WoC approach to solve CSAT problems
def genetic_algorithm(num_vars, clauses, logic_type, pop_size=15, generations=50, mutation_rate=0.05):
    
    # generates an initial random population of possible solutions
    chromosomes = initial_pop(pop_size, num_vars)
    # this list keeps track of the best fitness values from each generation to later be used for plotting
    best_fitness_per_gen = []

    # starts the evolution process over the specified number of generations
    for generation in range(generations):

        # function call to the fitness funciton to evaluate the fitness of the current population
        fitness_scores = fitness(chromosomes, clauses, logic_type)

        # keeps track the best fitness score of the current generation
        best_fitness_per_gen.append(fitness_scores[0][1])

        # selects the front half of the possible solutions based on their fitness
        selected_chromosomes = [fitness_scores[i][0] for i in range(len(fitness_scores) // 2)]
        # ensure the number of selected possible solutions is even for pairing (for crossover)
        if len(selected_chromosomes) % 2 != 0:
            selected_chromosomes.append(selected_chromosomes[0])

        # creates two new solutions/children through crossover and mutation
        # the list that will store the new solutions/children
        offspring = []
        for i in range(0, len(selected_chromosomes), 2):
            # the parent chromosomes to be combined in crossover
            parent1, parent2 = selected_chromosomes[i], selected_chromosomes[i+1]
            # function call to the crossover function to output two new solutions/children
            child1, child2 = crossover(parent1, parent2)
            # list appendage and function call to the mutation function to randomly apply mutations to the new solutions/children
            offspring.append(mutation(child1, mutation_rate))
            offspring.append(mutation(child2, mutation_rate))
        # creates the next generations population by combining selected parents and their offspring
        chromosomes = selected_chromosomes + offspring

    # after all generations are complete, this evaluates the fitness of the final population and gets the final fitness scores
    final_fitness = fitness(chromosomes, clauses, logic_type)
    # selects the chromosome with the highest fitness score
    best_chromosome, best_score = final_fitness[0]

    return best_chromosome, best_score, best_fitness_per_gen

# this function plots the results of the fitness over all the generations
def plotting_results(best_fitness_per_gen):
    # plots the fitness vlaues over the generations
    plt.plot(best_fitness_per_gen, c='blue')
    # labels the axes and gives a title to the plot
    plt.xlabel("Generation")
    plt.ylabel("Fitness (Number of Clauses Satisfied)")
    plt.title("Fitness Over Generations")
    # display gridlines on the plot
    plt.grid(True)
    # displays the plot
    plt.show()

# main function - elapsed time calculation, function calls, and printing statements of results
if __name__ == '__main__':
    
    # path to the file
    file_path = "80_100_circuitSAT.txt"
    # a function call to get the city coordinates from the file
    num_vars, clauses = read_file(file_path)
    
    # starts counting for run time
    start_timer = time.time()

    # can change to 'OR', 'AND', or 'NOT'
    logic_type = "NOT"
    # add function calls here
    best_chromosome, best_score, best_fitness_per_gen = genetic_algorithm(num_vars, clauses, logic_type)
    
    # stops counting for run time
    end_timer = time.time()
    
    # calculates the elapsed time
    elapsed_time = round((end_timer - start_timer), 4)
    
    # print results here with elapsed time
    print(f"Final best solution found: {best_chromosome}")
    print(f"Number of clauses satisfied: {best_score}")
    print(f"Elapsed time: {elapsed_time} seconds.")

    # plotting fitness over generations
    plotting_results(best_fitness_per_gen)
