#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
description : Experiment with coding adaptive random walk
author      : bveitch
version     : 1.0
project     : MouseAndCheese (experiments with random walks)
date        : Friday 19th February  


Code to illustrate how an artificial mouse might adapt its programmed behaviour 
to find cheese which it can only ‘smell’. In short, given a grid position the mouse will move to a 
neighbouring position at random, but as information is learned as to the ’strength’ of the smell
 these probabilities are updated and the mouse will converge to the cheese. 

This was intended as a bit of fun to illustrate some basic concepts from 
reinforcement learning and random walks. I suppose it could equally help students think about problem design,
simplification and abstraction. I warn you the code is somewhat hacky right now, there is a bug 
(when mouse encounters an edge, which I ought to fix) and it needs a better design for a ‘Mouse’ object 
having clearly defined state and actions. 

I wondered if this might make a decent project or lab demonstration? 
   
"""

import numpy as np
import matplotlib.pyplot as plt

import math

import World as wld
import Mouse as mouseagent

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

    ax.plot(history[0][0], history[0][1], 'b', marker='^',label='mouse')
    ax.plot(cheese_position[0], cheese_position[1], 'k', marker='x',label='cheese')
    ax.axis(xmin = 0, xmax = nx)
    ax.axis(ymin = 0, ymax = ny)
    for i in range(len(history)-1):
        pos0=history[i]
        pos1=history[i+1]
        ax.arrow(pos0[0], pos0[1], pos1[0]-pos0[0], pos1[1]-pos0[1], head_width=0.02, head_length=0.025, fc='b', ec='b')
    
    ax.legend(loc='lower right',shadow=True)
    plt.show()
    if(fname is not None):  
        plt.savefig(fname)
 
    
cheeseValue   = +100

nx=100
ny=100

cheesePos=[90,91]
discount=1.0
memsize=10
    
mouse_pos=[math.floor((nx+1)/2),math.floor((ny+1)/2)]
print(mouse_pos)
directions=['left','right','up','down']     

world=wld.World(nx,ny,mouse_pos)
world.add_cheese(cheesePos,cheeseValue)
smell = world.get_smell()

mouse=mouseagent.Mouse(directions,memsize)
number_iterations = 200

history=[]
distances_from_cheese=[]


for i in range(number_iterations):
    
    mouse_position = world.get_position()
    history.append([mouse_position[0],mouse_position[1]])
    
    d = world.get_distance_from_cheese(cheesePos)
    distances_from_cheese.append(d) 
    
    # check for solution
    if(mouse_position==cheesePos):
        print('Yay! The mouse found the cheese')
        break
    #get a direction from existing probabilities
    step = mouse.get_step()
  
    print("iteration = ", i, "direction = ", step)
    #move to a new position in direction
    world.update_mouse_position(step)
    #update states
   
    #sniff this position
    smell = world.get_smell()
    #update mouse's memory
    mouse.update_memory(step,smell)
    
    #calculate weights for next step (hard bit)
    mouse.update_step_weights()

#done, let's plot stuff:
plot_convergence(distances_from_cheese,'convergence.png')

plot_mouse_positions(history,cheesePos,'mouse_finds_cheese.png')