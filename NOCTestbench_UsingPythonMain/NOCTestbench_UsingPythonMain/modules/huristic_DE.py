import random
import numpy as np

def generate_source_destination_DE(rows, columns, gen=4032, popsize=10, crossover_rate=0.7, mutation_rate=0.9):
    # Initialize NoC parameters
    n_bits = rows * columns
    lst_s = list(range(0, n_bits))
    print("\033[93m"+f"n_bits={n_bits}  lst_s={lst_s}"+"\033[0m")

    # Store array of all possible paths between two nodes of the NoC
    combos = np.zeros((n_bits * (n_bits - 1), 2))
    iter = n_bits * (n_bits - 1) - 1
    for i in lst_s:
        for j in lst_s:
            if i != j:
                combos[iter] = [i, j]
                iter = iter - 1

    # Generate the initial population
    pop = np.zeros((popsize, 2))
    for k in range(popsize):
        i = random.choice(lst_s)
        j = random.choice(lst_s)
        pop[k] = [i, j]

    def objective_function(individual):
        return int(np.any(np.all(combos == individual, axis=1)))

    def crossover(pop, mutant_pop):
        crossover_pop = np.zeros((len(pop), 2))
        for x in range(len(pop)):
            if random.random() < crossover_rate:
                crossover_pop[x] = mutant_pop[x]
            else:
                crossover_pop[x] = pop[x]
        return crossover_pop

    def mutant(pop):
        mutant_pop = np.zeros((len(pop), 2))
        for x in range(len(pop)):
            idxs = [idx for idx in range(len(pop))]
            a, b, c = pop[random.choice(idxs)], pop[random.choice(idxs)], pop[random.choice(idxs)]
            mutant = np.add(a, mutation_rate * np.subtract(b, c))
            mutant = np.clip(mutant, 0, n_bits - 1)
            mutant = np.round(mutant)
            mutant_pop[x] = mutant
        return mutant_pop

    def differential_evolution(pop):
        for x in range(gen):
            print(f"iteration is done x={x}")
            mutant_pop = mutant(pop)
            crossover_pop = crossover(pop, mutant_pop)
            pop_arr = np.array(pop)
            next_pop = np.concatenate((pop_arr, crossover_pop))
            next_pop = np.unique(next_pop, axis=0)
            next_pop_fitness = np.array([objective_function(individual) for individual in next_pop])
            next_pop = np.multiply(next_pop, next_pop_fitness[:, np.newaxis])
            np.random.shuffle(next_pop)
            next_pop = next_pop.tolist()
            next_pop = [t for t in next_pop if t != [0, 0]]
            pop = next_pop
        return pop

    sol = differential_evolution(pop)
    result=[]
    for x in sol:
        i = x[0]
        j = x[1]
        lbs = i // columns
        source_l = bin(int(lbs)).replace('0b', '')
        x = source_l[::-1]
        while len(x) < 4:
            x += '0'
        source_l = x[::-1]
        ubs = i % columns
        source_u = bin(int(ubs)).replace('0b', '')
        x = source_u[::-1]
        while len(x) < 4:
            x += '0'
        source_u = x[::-1]
        source = str(source_l) + str(source_u)
        ######################
        lbd = j // columns
        dest_l = bin(int(lbd)).replace('0b', '')
        x = dest_l[::-1]
        while len(x) < 4:
            x += '0'
        dest_l = x[::-1]
        ubd = j % columns
        dest_u = bin(int(ubd)).replace('0b', '')
        x = dest_u[::-1]
        while len(x) < 4:
            x += '0'
        dest_u = x[::-1]
        dest = str(dest_l) + str(dest_u)
        
        result.append([source, dest])
    return result



