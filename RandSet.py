from collections.abc import MutableSet
import random
 
class RandSet(MutableSet):
    def __init__(self, it=[]):
        super().__init__()
       
        self.dict = {}
        self.list = []
 
        self.extend(it)
       
    def add(self, item):
        if item not in self.dict:
            self.dict[item] = len(self.list)
            self.list.append(item)
 
    def extend(self, seq):
        for x in seq:
            self.add(x)
           
    def discard(self, item):
        if item in self.dict:
            index = self.dict[item]
            self.list[index], self.list[-1] = self.list[-1], self.list[index]
            self.dict[self.list[index]] = index
            del self.dict[self.list.pop()]
 
    def __repr__(self):
        return repr(set(self))
           
    def __len__(self):
        return len(self.list)
 
    def __iter__(self):
        return iter(self.list)
 
    def __contains__(self, v):
        return v in self.dict                
 
    def get_rand(self, r=random):
        if self.list:
            return self.list[r.randint(0,len(self.list)-1)]