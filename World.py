#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
description : World object for mouse to move in
author      : bveitch
version     : 1.0
project     : MouseAndCheese (experiments with random walks)
date        : Friday 19th February  

"""

import numpy as np
import math

def get_distance(A,B):
        xA=A[0]
        yA=A[1]
        xB=B[0]
        yB=B[1]
        distance=math.sqrt((xA-xB)**2 +(yA-yB)**2)
        return distance

class World:
    
    def __init__(self, nx, ny, mouse_position):
        self.nx = nx
        self.ny = ny
        self.grid=np.zeros((nx,ny))
        self.mouse_position = mouse_position
        
    def add_cheese(self,position, value):
        self.grid[position[0],position[1]]=value
    
    def get_position(self):
        return self.mouse_position
    
    def get_distance_from_cheese(self,cheese_position):
        return get_distance(self.mouse_position, cheese_position)
    
    def get_smell(self):
        xpos=self.mouse_position[0]
        ypos=self.mouse_position[1]
    
        smell=0
        for ix in range(self.nx):
            for iy in range(self.ny):
                if(ix!=xpos and iy!=ypos):
                    d=get_distance([xpos,ypos],[ix,iy])
                    smell+=self.grid[ix,iy]/d**2
                
        return smell
        
    def update_mouse_position(self,step):
        if(step=='left' and self.mouse_position[0]!=0):
            self.mouse_position[0]-=1
        elif(step=='right' and self.mouse_position[0]!=self.nx-1):
            self.mouse_position[0]+=1
        elif(step=='down' and self.mouse_position[1]!=0):
            self.mouse_position[1]-=1
        elif(step=='up' and self.mouse_position[1]!=self.ny-1):
            self.mouse_position[1]+=1 
            
        
