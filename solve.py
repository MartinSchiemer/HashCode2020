import random
from genetic import *

def init_gene(prob):

    for lib in prob.libs:
        avg_score = sum(b.score for b in lib.books) / len(lib.books)
        days = prob.days - lib.days
        lib.score = days * lib.shiprate * avg_score
        
        
    libs_rev = sorted(prob.libs,
                 key=lambda x: x.score,
                 reverse=True)
    libs_i = [l.id for l in libs_rev]

    #random.shuffle(libs_i)
    
    
    return libs_i #, books_i
          
last_per = -1
def percent(x, out_of):
    global last_per
    cur = int(x / out_of * 100)
    if cur > last_per:
        last_per = cur
        print(f'{cur}%')
    
def big_boi_search(prob):    
    def score_lib(lib, days):
        days -= lib.days
        books = pick_books_for_lib(lib, lib.capacity(days))
        lib.candid_books = books
        return sum(b.score for b in books)
        
    def lib_order(libs, days):
        libs = [x for x in libs if x.days < days]
        
        while libs:
            s_libs = [(x, score_lib(x, days)) for x in libs]
            s_libs.sort(key=lambda x: x[1], reverse=True)
            
            lib = s_libs[0][0]
            days -= lib.days
            lib.rem_days = days
            assign_books_to_lib(lib, lib.candid_books)
            percent(len(prob.libs) - len(libs), len(prob.libs))
            
            yield lib
            
            libs.remove(lib)
            libs = [x for x in libs if x.days < days]

    prob.signup = list(lib_order(prob.libs, prob.days))
        
def signup_libs(prob, dna):
    libs_i = dna
    
    ret = [prob.libs[i] for i in libs_i]
    
    last_index = 0
    rem_days = prob.days
    for i, l in enumerate(ret):
        rem_days -= l.days
        if rem_days <= 0:
            break
        l.rem_days = rem_days
        last_index = i

    prob.signup = ret[:last_index + 1]
    
def pick_books_for_lib(lib, cap):
    return sorted((b for b in lib.books
                   if not b.scanned),
                   key=lambda x: x.score,
                   reverse=True)[:cap]
    
def assign_books_to_lib(lib, books):
    lib.scanned_books = books
    for b in books:
        b.scanned_by = lib
    lib.done = True
    
def assign_books(prob, dna):
    
    lst = sorted(prob.signup,
                 key=lambda x: x.capacity(),
                 reverse=True)
    
    for lib in lst:
        assign_books_to_lib(lib, pick_books_for_lib(lib, lib.capacity()))


    

_counter = 0
def dbg_print(s):
    global _counter
    if _counter < 500:
        print(s)
        _counter += 1
    
def assign_books_(prob, dna):
    _, books_i = dna
    
    for b in [prob.books[i] for i in books_i]:
        avail_libs = [l for l in b.libs if l.capacity > 0]
        if avail_libs:
            # TODO, better way to do this?
            l = avail_libs[0]
            
            l.scanned_books.append(b)
            b.scanned_by = l
        

        
def solve(prob):
    if True:
        prob.reset()
        big_boi_search(prob)
        s = prob.score()
        print(str(s))
        return s
    
    
    init_score = 1
    
    def score(dna, div=True):
        prob.reset()
        signup_libs(prob, dna)
        assign_books(prob, dna)
        return prob.score()
        
    def score_c(dna):
        
        s = score(dna)
        s /= init_score
        s **= 5
        return s
    
    g = init_gene(prob)
    init_score = score(g)
    
    if False:
        print(str(init_score))
        return prob
    
    pool = create_pop(g)
    non_improve_counter = 0
    old_score = 0
    drastic = False
    for i in range(10000):
        if non_improve_counter == 5:
            drastic = True
            
        pool = breeding(pool, score_c, drastic=False)
        s = score(pool[0])
        if s < old_score:
            non_improve_counter += 1
        else:
            non_improve_counter = 0
        print(str(s))
        old_score = s
        
        if drastic:
            drastic = False
    return prob
