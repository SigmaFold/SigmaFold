#!/usr/bin/env python
# coding: utf-8

# In[2]:


import networkx as nx #graph library 
import numpy as np
import math as math
import random as random


# In[5]:


#parameters
alpha = -1; #how much we like H-H bond
beta = .2; # how much we punish external H 
testing=[[1,0,0,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]] #goal shape 
step=1;
sequence='HHPPHHHHHPPPHH'
for i in range(len(testing)):
    for k in range(len(testing[1])):
        if(testing[i][k]==1):
            testing[i][k]=step
            step=step+1
goalshape=np.array(testing) #reformatted goalshape
path=[2,6,10,14,13,9,5,4,8,12,11,7,3,1]


# In[6]:


[[1,0,0,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]]


# In[7]:


#turns chains of {xpositon,yposition,residuevalue} into matrix of values only 
def graphicchain(chain):
    boundary=np.floor(max([len(goalshape),len(goalshape[1])]));
    lattice=np.ndarray.tolist(np.zeros([int(boundary),int(boundary)]))
    for i in range(len(chain)):
        lattice[chain[i][0]][chain[i][1]]=chain[i][2]
    lattice=np.array(lattice)
    return(lattice)


# In[8]:


#counts nearby Hs 
def counters(chaining,goalmatrix):
    count=0
    lattice1=np.ndarray.tolist(np.zeros([len(goalmatrix)+1,len(goalmatrix[0])+1]))
    for m in range(len(chaining)):
        lattice1[chaining[m][0]][chaining[m][1]]=chaining[m][2]


    for k in range(len(chaining)):
        if(chaining[k][2]!='P'and chaining[k][2]!='0'and chaining[k][2]!=0):
            if(lattice1[chaining[k][0]+1][chaining[k][1]]==chaining[k][2]):
                count=count+1
            if(lattice1[chaining[k][0]-1][chaining[k][1]]==chaining[k][2]):
                count=count+1
            if(lattice1[chaining[k][0]][chaining[k][1]+1]==chaining[k][2]):
                count=count+1
            if(lattice1[chaining[k][0]][chaining[k][1]-1]==chaining[k][2]):
                count=count+1

    return(count)


# In[9]:



def rewardfunc(seq,path,shape):
    #this initial bit is to turn our inputs into a chain. Basically it's so we can visualize the shape. It's a bit slow since 
    #i copy pasted from my initial prototype for brute force 
    addzeros=[]
    chain=[]
    for i in range(len(np.ndarray.flatten(goalshape))):
        if np.ndarray.flatten(goalshape)[i]==0:
            addzeros.append(i)
      #fix path list
    for k in range(len(addzeros)):
        for i in range(len(path)):
            if addzeros[k]<path[i]:
                    path[i]=path[i]+1 
    placeholder=np.ndarray.flatten(goalshape);
    strings=np.ndarray.tolist(placeholder)
    for i in reversed(range(len(path))):
            #here use sequence first onl            #strings=strings.replace(str(i),str(sequences[z][i]))
        strings[path[i]-1]=sequence[i]
    strings[i]=strings[i].replace(str(' '),str(''))  
    strings[i]=strings[i].replace(str(','),str('')) 
    strings[i]=strings[i].replace(str("'"),str('')) 
    strings[i]=strings[i].replace(str('['),str('')) 
    strings[i]=strings[i].replace(str(']'),str('')) 
    for j in range(max(np.ndarray.flatten(goalshape)+len(addzeros))):
        place=j
        if(strings[place]!=' ' and strings[place]!='0' and strings[place]!=0):
                chain.append([math.floor(j/len(goalshape[1])),j%len(goalshape[1]),strings[place]])
    matrix=graphicchain(chain)
    
    #the above bit is basically just formatting
    
    #interactions counts the number of H-H interactions 
    interactions=counters(chain,goalshape)/2
    for i in range(len(sequence)-1):
        if sequence[i]!='P' and sequence[i+1]==sequence[i]:
            interactions=interactions-1
    outsideh=0
    #outsideh is how we calculate the outside Hs 
    for y in range(len(matrix)):
        for x in range(len(matrix[1])):
            # if you're on the edge of the goalshape matrix we know you must be outside 
            if matrix[y][x]!='P' and matrix[y][x] != '0.0' and matrix[y][x]!=0 and (x==0 or x==len(matrix[1])-1 or y==0 or y==len(matrix)-1):
                outsideh=outsideh+1
            #if you're touching a zero as a hydrophobic residue we must punish you
            elif matrix[y][x]!='P' and matrix[y][x] != 0 and matrix[y][x]!= '0.0' and (matrix[y-1][x]=='0.0' or matrix[y+1][x]=='0.0' or matrix[y][x+1]=='0.0' or matrix[y][x-1]=='0.0'):
                outsideh=outsideh+1
    #alpha is how much to weight H-H bonds and outsideh is how much to punish external hydrophobic residues
    return alpha*interactions+outsideh*beta

# In[10]:

sequence='PHHPHHHHHHPHHH'
reward=rewardfunc(sequence,[2,6,10,14,13,9,5,4,8,12,11,7,3,1],goalshape)