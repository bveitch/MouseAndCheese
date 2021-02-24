#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
description : Mouse object to intercact with a world 
author      : bveitch
version     : 1.0
project     : MouseAndCheese (experiments with random walks)
date        : Friday 19th February  

"""

import numpy as np
import random
  
class MemoryBank:

    def __init__(self,memsize):
        self.memory =[['none',0]]*memsize
        self.current_smell = 0
        print(self.memory)

    def size(self):
        return len(self.memory)

    def update(self,step,smell):
        self.memory.pop(0)
        self.memory.append([step,smell-self.current_smell])
        self.current_smell=smell

    def get_step_weights(self,directions):
        
        weights = np.zeros(len(directions))
        counts=[0]*len(directions)
        for m in self.memory[::-1]:
        
            for i in range(len(directions)):
                direction = directions[i]
                if m[0]==direction:
                    weights[i]+=m[1]
                    counts[i]+=1
    
        #take means over counts:
        for i in range(len(directions)):
            if(counts[i]>0):
                weights[i]/=counts[i]
        
        #make all positive:
        minimum=np.min(weights)
        weights-=minimum
 
        #convert to a probability:
        total=np.sum(weights)
        weights/=total
        
        return weights

class Mouse:
    
    def __init__(self, directions, memsize=10):
        self.directions = directions
        self.memorybank = MemoryBank(memsize)
        self.step_weights=0.25*np.ones(len(directions))
        self.discount=1.0

    def update_memory(self,step,smell):
        self.memorybank.update(step,smell)

    def update_step_weights(self):

        weights=self.step_weights
    
        new_weights = self.memorybank.get_step_weights(self.directions)
    
        #add on new weights
        weights+=self.discount*new_weights
    
        #recalibrate to probability once more
        total=sum(weights) 
        weights/=total
            
        self.step_weights=np.copy(weights)
              
    def get_step(self):
        direction = random.choices(self.directions, weights = self.step_weights, k = 1)
        return direction[0]
 
 