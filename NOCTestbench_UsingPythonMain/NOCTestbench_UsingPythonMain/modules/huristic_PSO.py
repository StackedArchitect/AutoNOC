import numpy as np
import numpy.random as numpy_random
from numpy.random import randint
from numpy.random import rand
import time
import logging


def  source_destination_generator_pos(m,n):
    logging.info("\033[93m"+"POS is selected"+"\033[0m")
    def redundancy_check(val,pop,pop_size,iter_size):
        cov = []
        valid = []
        for i in range(len(pop)):
            t = 0
            for j in range(val):
                for k in range(val-1):
                    if pop[i][j][k] == 1:
                        t=t+1
            cov.append(t)
        #print(cov)
        for i in range(len(pop)):
            if cov[i] not in cov[:i]:
                valid.append(pop[i])
        return valid
                
    def fitness(arr,n_pop,val):
        coverage = []
        for i in range(n_pop):
            t = 0
            for j in range(val):
                for k in range(val-1):
                    if arr[i][j][k] == 1:
                        t=t+1
            f = np.around((t/size)*100,decimals = 2)
            coverage.append(f)
        #print("Coverage: ")
        #print(coverage)
        #print()
        return coverage              
        
    def pso(m, n, iter_size, pop_size, size):
        # initial population of numpy_random bitstring
        pop = []
        for i in range(pop_size):
            particle = np.random.randint(2, size=(val, val-1))
            pop.append(particle)
        #print(pop)
        valid_pop = redundancy_check(val,pop, pop_size, iter_size)
        #print(valid_pop)
        p_best = [0 for i in range(len(valid_pop))]
        global_best = 0
        best = 0
        alpha = 0.9
        
        for gen in range(iter_size):  
            #print(valid_pop)
            coverage = fitness(valid_pop,len(valid_pop),val)
            #print(coverage)
            for i in range(len(valid_pop)):
                if coverage[i] > p_best[i]:
                    p_best[i] = coverage[i]
            if max(p_best) > global_best:
                global_best=max(p_best)
                best = p_best.index(global_best)
            #print(best,global_best)
            for j in range(len(valid_pop)):
                for c in range(20):
                    a = numpy_random.randint(0,val-1)
                    b = numpy_random.randint(0,val-2)
                    #check for a mutation
                    if rand() < alpha:
                        if valid_pop[j][a][b] == 0:
                            valid_pop[j][a][b] = 1
                        #else:
                            #valid_pop[j][a][b] = 0
        print("Generation ",gen,": Global Best: ",global_best)
        print("Particle:",valid_pop[best])
        #print("Global Best: ")
        #print(global_best)
        print()
        
        return valid_pop[best]
        
    ##################################################################
    iter_size =4100
    pop_size = 600
    val = m*n
    size = (val*val)-val
    best = pso(m,n,iter_size,pop_size,size)
    ######################## TRAFFIC GENERATION ########################
    payloads=3
    #test=np.ones([val,val-1])
    #test = np.reshape(best,(val,val-1))
    test = best
    #print(test)
    lst_s = list(range(0, val))
    lst_d = list(range(0, val-1))
    #numpy_random.shuffle(lst_s)
    #numpy_random.shuffle(lst_d)
    #print(lst_s)
    #print(lst_d)
    combos=[]
    for i in lst_s:
        for j in lst_d:
            combos.append([i,j])
    numpy_random.shuffle(combos)
    #print(combos)
    #print(len(combos))
    ##################
    result=[]
    ##################
    for k in combos:
        j=k[1]
        i=k[0]
        if (j >= i):
            d = j + 1
        else:
            d = j
        if (test[i][j] >= 1):
            lbs = i // n
            source_l = bin(lbs).replace('0b', '')
            x = source_l[::-1]  # this reverses an array
            while len(x) < 4:
                x += '0'
            source_l = x[::-1]
            ubs = i % n
            source_u = bin(ubs).replace('0b', '')
            x = source_u[::-1]  # this reverses an array
            while len(x) < 4:
                x += '0'
            source_u = x[::-1]
            source = str(source_l) + str(source_u)
            ######################
            lbd = d // n
            dest_l = bin(lbd).replace('0b', '')
            x = dest_l[::-1]  # this reverses an array
            while len(x) < 4:
                x += '0'
            dest_l = x[::-1]
            ubd = d % n
            dest_u = bin(ubd).replace('0b', '')
            x = dest_u[::-1]  # this reverses an array
            while len(x) < 4:
                x += '0'
            dest_u = x[::-1]
            dest = str(dest_l) + str(dest_u)

            rand_ls = np.random.randint(0, 1, size=(13))
            rand_ls = str(rand_ls).replace(" ", "")
            rand_ls = str(rand_ls).replace("[", "")
            rand_ls = str(rand_ls).replace("]", "")
            h_f = [str(source) ,str(dest)]
            result.append(h_f)
            
    return result
