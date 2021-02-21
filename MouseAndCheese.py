#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
description : Mouse moves in random walks, search probablilities updated
author      : bveitch
version     : 1.0
project     : MouseAndCheese (experiments with random walks)
date        : Friday 19th February     
"""

import numpy as np
import matplotlib.pyplot as plt

import random
import math

CheeseValue   = +100

nx=100
ny=100

cheese_pos=[90,91]
discount=1.0
memsize=10
memory = []

grid2D=np.zeros((nx,ny))
grid2D[cheese_pos[0],cheese_pos[1]]=CheeseValue
    
def distance(mouse_pos,pos):
    mouse_xpos=mouse_pos[0]
    mouse_ypos=mouse_pos[1]
    xpos=pos[0]
    ypos=pos[1]
    distance=math.sqrt((mouse_xpos-xpos)**2 +(mouse_ypos-ypos)**2)
    return distance

def calculate_score(pos,grid):
    xpos=pos[0]
    ypos=pos[1]
    
    score=0
    for ix in range(nx):
        for iy in range(ny):
            if(ix!=xpos and iy!=ypos):
                d=distance(pos,[ix,iy])
                score+=grid[ix,iy]/d**2
                
    return score

def reassign_weights_for_search(memory,search):
    directions=list(search.keys())
    old_weights=list(search.values())
    
    new_weights = np.zeros(len(directions))
    counts=[0]*len(directions)
    for m in memory[::-1]:
       
        for i in range(len(directions)):
            direction = directions[i]
            if m[0]==direction:
                new_weights[i]+=m[1]
                counts[i]+=1
    
    #take means over counts:
    for i in range(len(directions)):
        if(counts[i]>0):
            new_weights[i]/=counts[i]
        
    #make all positive:
    minimum=np.min(new_weights)
    new_weights-=minimum
 
    #convert to a probability:
    total=np.sum(new_weights)
    new_weights/=total
    
    #add on old weights
    new_weights+=discount*np.array(old_weights)
    
    #recalibrate to probability once more
    total=sum(new_weights) 
    new_weights/=total
    
        
    new_search=zip(directions,new_weights)         
    return dict(new_search)
    
def get_move(search):
    direction = random.choices(list(search.keys()), weights = list(search.values()), k = 1)
    return direction[0]

def make_move(direction,mouse_pos):
    if(direction=='left' and mouse_pos[0]!=0):
        mouse_pos[0]-=1
    elif(direction=='right' and mouse_pos[0]!=nx-1):
        mouse_pos[0]+=1
    elif(direction=='down' and mouse_pos[1]!=0):
        mouse_pos[1]-=1
    elif(direction=='up' and mouse_pos[1]!=ny-1):
        mouse_pos[1]+=1    
    return mouse_pos
    
    
def update_memory(memory,direction,score):
    memory.append([direction,score])
    if(len(memory)> memsize):
        memory.pop(0)
 
def plot_convergence(distances_from_cheese,fname):
    niterations=len(distances_from_cheese)
    fig, ax=plt.subplots(1,1,squeeze=False, figsize=(18,10))
    ax[0,0].set_title("Distance from Cheese",fontsize=10)
    ax[0,0].set_xlabel('Iterations')
    ax[0,0].xaxis.labelpad=-25
    ax[0,0].set_ylabel('Distance')
    ax[0,0].plot(range(niterations), distances_from_cheese , 'r')
    plt.show()
    if(fname is not None):  
        plt.savefig(fname)
        
def plot_mouse_positions(history,cheese_position,fname):
    fig, ax = plt.subplots()
    ax.set_title("Mouse searching for cheese",fontsize=10)
    ax.set_xlabel('x position')
    ax.set_ylabel('y position')

    ax.plot(cheese_position[0], cheese_position[1], 'k', marker='x',label='cheese')
    ax.axis(xmin = 0, xmax = nx)
    ax.axis(ymin = 0, ymax = ny)
    for i in range(len(history)-1):
        pos0=history[i]
        pos1=history[i+1]
        ax.arrow(pos0[0], pos0[1], pos1[0]-pos0[0], pos1[1]-pos0[1], head_width=0.02, head_length=0.025, fc='b', ec='b',label='mouse')
    
    ax.legend(loc='lower right',shadow=True)
    plt.show()
    if(fname is not None):  
        plt.savefig(fname)
   
      
mouse_pos=[math.floor((nx+1)/2),math.floor((ny+1)/2)]
print(mouse_pos)
directions=['left','right','up','down']
weights=0.25*np.ones(len(directions))

search=dict(zip(directions, weights))

number_iterations = 200
current_score=calculate_score(mouse_pos,grid2D)
history=[[mouse_pos[0],mouse_pos[1]]]
distances_from_cheese=[distance(mouse_pos,cheese_pos)]

for i in range(number_iterations):
    direction = get_move(search)
    print("iteration = ", i, "direction = ", direction)
   
    mouse_pos = make_move(direction,mouse_pos)
    history.append([mouse_pos[0],mouse_pos[1]])
    d=distance(mouse_pos,cheese_pos)
    distances_from_cheese.append(d)
    
    if(mouse_pos==cheese_pos):
        print('Yay! The mouse found the cheese')
        break
    
    new_score=calculate_score(mouse_pos,grid2D)
    
    update_memory(memory,direction,new_score-current_score)
    
    current_score=new_score
   
    if(len(memory) == memsize):
        search=reassign_weights_for_search(memory,search)

#done, let's plot stuff:
plot_convergence(distances_from_cheese,'convergence.png')

plot_mouse_positions(history,cheese_pos,'mouse_finds_cheese.png')
