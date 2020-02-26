import random as rn
from time import clock
from RandSet import RandSet
import itertools

top = 5
breed_size = 20
pool_size = 50


def create_pop(start_gene):    
    pool = [start_gene]

    for i in range(pool_size - 1):
        rn_start_gene = start_gene.copy()
        rn.shuffle(rn_start_gene)
        pool.append(rn_start_gene)
        
    return pool

def get_with_score(l, i, remove=True):
    tot = 0
    for score, creature in l:
        tot += score
        
        if tot > i: 
            if remove:
                l.remove((score, creature))
            return score, creature
    
    return l[0][1]
       
def sum_pool(l):
    return sum(s for s, _ in l)

def breeding(pool, creature_score, drastic):
    scored_creatures = [(creature_score(c), c) for c in pool]
    scored_creatures.sort(key = lambda x: x[0], reverse=True)

    breeding_pool = scored_creatures[:top]
    next_pool = [x for _, x in breeding_pool]
    
    scored_creatures = scored_creatures[top:]
    
    tot_score = sum_pool(scored_creatures)
    breed_score = sum_pool(breeding_pool)
    
    # add random creature to potentially make big step
    nr_rand_creatures = 2
    if drastic:
        nr_rand_creatures = breed_size - top
        
    for i in range(nr_rand_creatures):
        rand_creature = breeding_pool[0][1].copy()
        rn.shuffle(rand_creature)
        breeding_pool.append((creature_score(rand_creature), rand_creature))
        
    while len(breeding_pool) < breed_size:           
        
        s, x = get_with_score(scored_creatures, rn.random() * tot_score)
        tot_score -= s
        breed_score += s
        breeding_pool.append((s, x))
        
    while len(next_pool) < pool_size:
        
        p1 = get_with_score(breeding_pool,
                            rn.random() * breed_score, False)
        p2 = get_with_score(breeding_pool,
                            rn.random() * breed_score, False)
        child = crossover(p1, p2, 0.6)
        
        next_pool.append(child)
        
        
    return next_pool    


def mutate(gene):
    
    rn_length = rn.randint(1,len(gene)//4)
    rn_start_ind = rn.randint(0,len(gene)-rn_length-1)
    extracted_sequence = gene[rn_start_ind:rn_length+rn_start_ind]
    rn.shuffle(extracted_sequence)
    gene[rn_start_ind:rn_length+rn_start_ind] = extracted_sequence
    
    return gene

def crossover_lists(list1, list2, parent1_factor,
                    mutation_factor):
    #print(len(list1))
#     global set_cache
    
#     if len(list1) not in set_cache:
#         set_cache[len(list1)] = set(list1)
        
#     rem_books = set_cache[len(list1)].copy()
    
    ret = list1.copy()
    rem_books = RandSet(list1)
    indices = list(range(len(list1)))
    
    rn.shuffle(indices)
    random_sample = rn.sample
    
    for ii in indices:
        zip_l = [list1[ii], list2[ii]]  
        zip_l = [element for element in zip_l if element in rem_books]
        
        if len(zip_l) == 0 or rn.random() < mutation_factor:
            val = rem_books.get_rand()
            
        elif len(zip_l) == 1:
            val = zip_l[0]
            
        else:
            i = int(rn.random() >= parent1_factor)
            val = zip_l[i]
            

        rem_books.remove(val)

        ret[ii] = val    
    
    return ret

def crossover_lists_pres_order(list1, list2,
                               mutation_factor):
    ret = list1.copy()
    
    ln = len(list1)
    rn_length = rn.randint(1,len(ret)//2)
    rn_start_ind = rn.randint(0,len(ret)-rn_length-1)
    
    extracted_sequence = set(list1[rn_start_ind:rn_length+rn_start_ind])
    
    def next_allele():
        pointer_l2 = (rn_start_ind + rn_length) % ln
        while len(extracted_sequence) < ln:
            el = list2[pointer_l2]
            
            if el not in extracted_sequence:
                extracted_sequence.add(el)
                yield el
            
            pointer_l2 += 1
            pointer_l2 %= ln
    
    list2_els = next_allele()
    
    
    to_fill_in = itertools.chain(range(rn_start_ind + rn_length, ln),
                                 range(0, rn_start_ind))
    
    for ind in to_fill_in:
        ret[ind] = next(list2_els)
        
    if rn.random() < mutation_factor:
            ret = mutate(ret)
    
    return ret
    


def crossover(gene_1, gene_2, mutation_factor=0.1):
    g1_score, g1 =  gene_1
    g2_score, g2 =  gene_2
    
    mut_lib = crossover_lists_pres_order(g1, g2, mutation_factor)
   
    return mut_lib
    

def compare_score():
    pass

