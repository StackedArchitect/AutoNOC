from numpy.random import randint
from numpy.random import rand
from random import sample
import time
import numpy as np
import random
import logging

def source_destination_generator_GA(row,column):

    logging.info("\033[93m"+"GA huristic is selected"+"\033[0m")
    ########Parameters
    rows = row
    columns = column
    # define the total iterations
    n_iter =4000
    # bits
    n_bits = rows *columns
    # define the population size
    n_pop = 20
    # crossover rate
    r_cross = 0.9
    # mutation rate
    r_mut = 0.9#1.0 / float(n_bits)
    print("r_mut :", r_mut)
    ##########

    def fitness(sequence):
        #print("SeQQQQQQQQQQ")
        #print(sequence)
        covd = 0
        total_poss_comb = n_bits*n_bits-n_bits
        #compare test particle with soultion
        for i in range(n_bits):
            for j in range(n_bits-1):
            #if (solution[i]== 1):
            #   total_poss_comb = total_poss_comb + 1
                if (sequence[i][j]  == 1):
                    covd = covd + 1

        fitness_value = (covd/ total_poss_comb) * 100
        #print(fitness_value)
        return fitness_value


    # tournament selection
    def selection(pop, scores):
        #print(scores)
        selected = []
        for i in range(2):
            l = scores.index(max(scores))
            selected.append(pop[l])
            scores[l] = -1
        return selected


    # crossover two parents to create two children
    def crossover(p1, p2, r_cross):
        # children are copies of parents by default
        p1 = [item for sublist in p1 for item in sublist]
        p2 = [item for sublist in p2 for item in sublist]
        #p1 = list(p1)
        #p2 = list(p2)
        # check for recombination

        if rand() < r_cross:
            k = randint(0, len(p1))
            #print("Crossover point :", k)

            # interchanging the genes
            # for i in range(k, len(p1)):
            #    p1[i], p2[i] = p2[i], p1[i]
            # p1 = ''.join(p1)
            # p2 = ''.join(p2)
            c1 = np.append(p1[:k], p2[k:])
            c2 = np.append(p2[:k], p1[k:])
            #print(c1)
            #print(c2, "\n\n")
            ch1=c1
            #return [p1, p2]
        else:
            ch1 = p1
        return ch1

    def mutation(bitstring, r_mut):
            # check for a mutation
        for i in range(columns+1):
            if rand() < r_mut:
                a = random.randint(0,len(bitstring)-1)
                #print("Flip point :", a)
                if bitstring[a]:
                    bitstring[a] = 0
                else:
                    bitstring[a] = 1

        return bitstring
    #######(R+NR)
    ss = []

    for i in range(n_pop):
        particle = np.random.randint(2, size=(n_bits, n_bits-1))
        #print(particle)
        #particle.tolist()
        #print(particle)
        ss.append(particle.tolist())
    #print(ss)

    #####only NR
    def redundancy_check(n_bits,pop):#,pop_size,iter_size):
        cov = []
        valid = []
        #flat_pop = [item for sublist in pop for item in sublist]
        for i in range(len(pop)):
            t = 0
            for j in range(n_bits):
                for k in range(n_bits-1):
                    #print(type(pop[i][j][k]))
                    if pop[i][j][k] == 1:
                        t=t+1
            cov.append(t)
        for i in range(len(pop)):
            if cov[i] not in cov[:i]:
                valid.append(pop[i])
        return valid

    def check_valid(child,pop):
        t1 = fitness(child)
        #print("inside!!!!!!!!!!!!!!!!!11")
        #print(pop)
        for i in range(len(pop)):
            t2=fitness(pop[i])
            if (t1==t2):
                return []
        return child

    #new_pop=redundancy_check(n_bits,ss)
    new_pop=ss
    #print(len(new_pop))
    # genetic algorithm
    def genetic_algorithm(fitness, n_bits, n_iter, n_pop, r_cross, r_mut,new_pop):
        # initial population of random bitstring
        """pop = []
        for i in range(n_pop):
            a = np.random.random_integers(0, 1, size=(n_bits, n_bits))
            sequence = np.tril(a) + np.tril(a, -1).T
            np.fill_diagonal(sequence, 0)
            pop.append(list(sequence.flatten()))
        print("Initial Population: ")
        print(pop)"""
        # keep track of best solution
        pop=new_pop
        #print(pop)
        flag=False
        #print("Initial Population: ")
        #print(pop)
        best, best_eval = pop[0], fitness(pop[0])
        #print(best_eval)
        # print(objective(pop[0]))
        # enumerate generations
        for gen in range(n_iter):
            print("GEN= {}".format(gen))
            # evaluate all candidates in the population
            #print(pop)

            scores = [fitness(c) for c in pop]
            """
            count=0
            for c in pop:

                if check_valid(c,n_bits)== 0:
                    scores[count] = 0       #scores.append(fitness(c,solution))
                count+=1

            #
            """
            #print(pop)
            #print(scores)
            #print(scores)
            for i in range(len(scores)):
                if (scores[i] == 100):
                    flag = True

            # check for new best solution
            for i in range(len(pop)):
                if (scores[i] >best_eval):
                    best, best_eval = pop[i], scores[i]
                    #print(best, best_eval)
                    print("iteration {}, new best f({}) = {}".format(i, pop[i], scores[i]))
                    
                # select parents
            selected = selection(pop, scores)
            #print("SELECTED")
            #print(selected)
            # print(selected)
            # create the next generation
            children = []
            if (flag):
                break
            for i in range(0, len(pop)):
                # get selected parents in pairs
                #x = randint(len(selected))
                #y = randint(len(selected))
                #while x == y:
                #    x = randint(len(selected))
                #   y = randint(len(selected))

                p1 = selected[0]
                p2 = selected[1]

                #print(p1,p2)
                # crossover and mutation
                #while True:
                c=crossover(p1, p2, r_cross)

                        # mutation
                #print("AFTER CROSSOVER")
                #print(c)

                ch=mutation(c, r_mut)
                        #####################
                        #now check valid here
                #print("AFTER MUTATION")

                ch=np.array(ch)
                ch = ch.reshape(n_bits, n_bits-1)
                    #check=check_valid(ch,pop)

                    #if(check!=[]):
                    #    print("CHECK")
                    #    print(check)
                #print(ch)
                children.append(ch)
                        #print(pop)
                        #break
                #break
                    ####################
                    # store for next generation


                # replace population
            pop = children
            #print(pop)
            #best_m = np.reshape(best, (n_bits, n_bits))
            #print(best_m)


            if (flag):
                break

            print("BEST= {},Score= {}".format(best,best_eval))
            print("---- Execution Time = {} seconds ----".format(np.around((time.time() - start_time),decimals=2)))
        return [gen,best, best_eval]



    start_time = time.time()
    # rows and columns

    # perform the genetic algorithm search
    gen,best, score = genetic_algorithm(fitness, n_bits, n_iter, n_pop, r_cross, r_mut,new_pop)
    #print("GEN= {}".format(gen))
    #print("BEST= {},Score= {}".format(best,score))
    #print("---- Execution Time = {} seconds ----".format(np.around((time.time() - start_time),decimals=2)))

    ######TRAFFIC GENERATION
    total=n_bits*n_bits-n_bits
    payloads=3
    #test=np.ones([n_bits,n_bits-1])

    """
    test= [[1 ,1, 1, 1 ,1 ,0 ,1, 1, 1, 1,1, 1, 1, 1 ,0, 1],
    [1 ,1 ,1, 1, 1, 1, 1, 0, 1, 1 ,1 ,1, 1, 1, 1, 1],
    [1 ,1, 1, 0 ,1 ,0 ,0, 1, 1, 1, 0, 0, 0, 1, 1, 1],
    [0 ,1 ,1 ,1 ,1, 1 ,0 ,0 ,0 ,0 ,1 ,1, 0, 1, 1, 1],
    [1 ,1, 0 ,1, 1 ,0 ,0 ,0 ,1 ,1 ,1, 1, 1, 0, 1, 1],
    [1, 1, 1, 0, 1, 1, 1 ,0 ,0 ,0 ,1 ,1 ,1 ,0 ,0 ,0],
    [0 ,1 ,1, 1 ,1 ,0 ,0 ,1 ,0 ,0 ,1 ,1 ,0 ,0, 1 ,1],
    [0 ,1 ,1 ,1 ,1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0],
    [0 ,1, 1 ,0, 1 ,1 ,1 ,1 ,1 ,1 ,0 ,1 ,0 ,1 ,1 ,1],
    [0 ,0, 0, 1, 1 ,1, 1, 1, 1 ,1 ,0 ,1 ,0 ,1 ,1 ,1],
    [0 ,0 ,1 ,0 ,0 ,0 ,1 ,0 ,1 ,0 ,1 ,1 ,0 ,0 ,0 ,1],
    [0 ,1 ,1 ,1 ,1 ,1 ,1, 0, 1, 0 ,1 ,0 ,0, 1, 0 ,1],
    [1 ,0, 0, 1, 0 ,0 ,0, 0,1, 1, 0 ,0 ,0 ,1 ,1 ,0],
    [1 ,0, 0 ,1 ,1 ,1 ,0, 1 ,1, 1, 1, 1, 0, 1, 1, 0],
    [0, 1, 1, 1 ,1 ,0, 1 ,0 ,1,0, 0, 1 ,0 ,0 ,0 ,1]]
    """

    lst_s = list(range(0, n_bits))
    lst_d = list(range(0, n_bits-1))
    #random.shuffle(lst_s)
    #random.shuffle(lst_d)
    #print(lst_s)
    #print(lst_d)
    combos=[]
    ################3333
    result=[]
    ################3333
    for i in lst_s:
        for j in lst_d:
            combos.append([i,j])
    random.shuffle(combos)
    #print(combos)
    #print(len(combos))

    for k in combos:
        j=k[1]
        i=k[0]
        if (j >= i):
            d = j + 1
        else:
            d = j
        if (best[i][j] >= 1):
            lbs = i // columns
            source_l = bin(lbs).replace('0b', '')
            x = source_l[::-1]  # this reverses an array
            while len(x) < 4:
                x += '0'
            source_l = x[::-1]
            ubs = i % columns
            source_u = bin(ubs).replace('0b', '')
            x = source_u[::-1]  # this reverses an array
            while len(x) < 4:
                x += '0'
            source_u = x[::-1]
            source = str(source_l) + str(source_u)
            ######################
            lbd = d // columns
            dest_l = bin(lbd).replace('0b', '')
            x = dest_l[::-1]  # this reverses an array
            while len(x) < 4:
                x += '0'
            dest_l = x[::-1]
            ubd = d % columns
            dest_u = bin(ubd).replace('0b', '')
            x = dest_u[::-1]  # this reverses an array
            while len(x) < 4:
                x += '0'
            dest_u = x[::-1]
            dest = str(dest_l) + str(dest_u)

            rand_ls = np.random.random_integers(0, 1, size=(13))
            rand_ls = str(rand_ls).replace(" ", "")
            rand_ls = str(rand_ls).replace("[", "")
            rand_ls = str(rand_ls).replace("]", "")
            h_f = [str(source) , str(dest)]
            result.append(h_f)
    return result


