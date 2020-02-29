import numpy as np
from pprint import pprint
from solve import *
import sys
import os
import zipfile
import RandSet

# nr_of_different_books nr_libraries nr_of_days
# scores of each book

# nr of books in library - nr of days for library signup - nr of book per day
# ids of books

class Book:
    def __init__(self, n, s):
        self.id = n
        self.score = s
        self.libs = []
        
        self.reset()
        
    @property
    def num_libs(self):
        return sum(1 for l in self.libs if not l.done)
    
    @property
    def scanned(self):
        return self.scanned_by is not None
        
    def reset(self):
        self.scanned_by = None
        
    def __repr__(self):
        return f'B{self.id}({self.score})'

class Lib:
    def __init__(self, n, d, s):
        self.id = n
        self.days = d
        self.shiprate = s
        self.books = []
        
        self.reset()
        
    def reset(self):
        self.rem_days = 0
        self.scanned_books = []
        self.done = False
        
    def capacity(self, days=None):
        if days is None:
            days = self.rem_days
            
        return days * self.shiprate - len(self.scanned_books)
        
    def __repr__(self):
        return f'L{self.id}({self.days}/{self.shiprate})'
        
class Problem:
    def __init__(self, books, libs, days):
        self.books = books
        self.libs = libs
        self.days = days
        
    def reset(self):
        self.signup = []
        
        for b in self.books:
            b.reset()
            
        for l in self.libs:
            l.reset()
            
    def score(self):
        return sum(b.score for b in self.books if b.scanned_by is not None)
    
    def prepare_for_output(self):
        self.signup = list(filter(lambda x: x.scanned_books, self.signup))
    
    def output_sol(self, f):
        f.write(str(len(self.signup)))
        f.write('\n')
                
        for lib in self.signup:
            f.write(str(lib.id) + ' ' + str(len(lib.scanned_books)))
            f.write('\n')
            f.write(' '.join(str(b.id) for b in lib.scanned_books))
            f.write('\n')
        
        
        
def read_file(name):
    with open(name) as rd:
        lines = list(rd)
        
    _, num_libs, num_days = map(int, lines[0].split())
    books = [Book(i, int(s)) for i, s in enumerate(lines[1].split())]
    lines = lines[2:]
    
    libs = []
    for i in range(num_libs):
        l1, l2 = lines[i * 2], lines[i * 2 + 1]
        
        _, days, shiprate = map(int, l1.split())
        lib = Lib(i, days, shiprate)
        lib.books = [books[int(i)] for i in l2.split()]
        libs.append(lib)
        
    for lib in libs:
        for b in lib.books:
            b.libs.append(lib)

    return Problem(books, libs, num_days)

def get_prob_names(start=''):
    return [f for f in os.listdir()
            if f[0] != '0' and f.endswith('.txt') and f.startswith(start)]

def zip_code():
    with zipfile.ZipFile('0_code.zip', 'w') as z:
        for file in [f for f in os.listdir() if f.endswith('.py')]:
            with z.open(file, 'w') as w:
                with open(file) as r:
                    w.write(r.read().encode('utf-8'))
    

def main(start='', genetic=False):
    zip_code()

    for p in get_prob_names(start):
        prob = read_file(p)
        solve(prob, genetic)
    
        prob.prepare_for_output()
        
        if False:
            print(prob.score())
            print('---- CUT HERE ----')
            prob.output_sol(sys.stdout)
            
        with open('0_sol_' + p, 'w') as f:
            prob.output_sol(f)
    
    
    

if __name__ == "__main__":
    main()