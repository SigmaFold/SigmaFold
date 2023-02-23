#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import math as math
import random as random


# In[65]:


forwardbias=1
offset=0
#this is just a method for counting energy. It effectively takes a matrix of H and Ps and subtracts 
#the bonds that are backbone affiliated
def counter(matrix,sequence):
    extras=0
    count=0
    for i in range(len(sequence)):

        if sequence[i]!="P":
            if i<len(sequence)-1:
                if sequence[i]==sequence[i+1] and i<len(sequence)-1:
                    extras=extras+1
            if i>0:        
                if sequence[i]==sequence[i-1] and i>0:
                    extras=extras+1
            print(extras)
    for i in range(len(matrix)):
        for j in range(len(matrix[1])):
            if matrix[i][j]!="P" and matrix[i][j]!=0:
                if i>0:
                    if matrix[i][j]==matrix[i-1][j]:
                        count=count+1
                if i<len(matrix)-1:
                    if matrix[i][j]==matrix[i+1][j]:
                        count=count+1
                if j>0:
                    if matrix[i][j]==matrix[i][j-1]:
                        count=count+1
                if j<len(matrix[1])-1:
                    if matrix[i][j]==matrix[i][j+1]:
                        count=count+1
    return (count-extras)/2


# In[86]:


#this takes in an old matrix and a revised matrix with a change. It also keeps a list of degenerate shapes of equal energy 
#temp is for the replica exchange monte carlo bit and is effectively a weighting factor
#sequence is mainly for the counter function 
def srmc(oldmat,newmat,bestenergy,possibles,temp,sequence):
    
    guesse=counter(oldmat,sequence)
    result=oldmat
    #calculate differences in energy between matrices
    delt=counter(newmat,sequence)-guesse
    #depending on whether the new energy is better or not choose three states
    if delt>0:
        #if new energy is closer to ground state, switch structure. 
        
        result=newmat
        #if the newenergy is actually the best we've seen so far. Reset best energy and degen list
        if counter(newmat,sequence)>bestenergy:
            bestenergy=counter(newmat,sequence)
            possibles=[newmat]
        return possibles,result,bestenergy
    #if the energies are equal, go with new structure
    elif delt==0:
        #if the energy equal to best energy, add it to degeneracy list 
        if counter(newmat,sequence)==bestenergy:
            possibles.append(newmat)
        result=newmat
        return possibles,result,bestenergy
    else:
        #if the newmat is worse than oldmat, probabilistically switch to newmat
        p=random.random()
        if p>math.exp(delt/temp):
            result=newmat
        return possibles,result,bestenergy
#replicalist is a list of {matrix,energy,temperature}
def remc(replicalist,offset):
    #offset to allow comparisons between different pairs 
    i=offset+1
    while i+1<len(replicalist):
        #basically compare each replica with the one next over with weighting from the temperature 
        j=i+1
        delta=(replicalist[j][2]-replicalist[i][2])*(-replicalist[i][1]+replicalist[j][1])
        if delta<0:
            #this means either the temoperature or energy is wrong, so we need to switch the temperatures (I chose to switch the matrixes instead) 
            replicalist[j][0],replicalist[i][0]=replicalist[i][0],replicalist[j][0]
            replicalist[j][1],replicalist[i][1]=replicalist[i][1],replicalist[j][1]
        else: 
            p=random.random()
            if p<math.exp(-delta):
                #probability of switching if actually the first is better than the second 
                replicalist[j][0],replicalist[i][0]=replicalist[i][0],replicalist[j][0]
                replicalist[j][1],replicalist[i][1]=replicalist[i][1],replicalist[j][1]
    #change the offset 
    offset=1-offset
    
            
            
            
        
    
    


# In[103]:


a=[[0,'H','H'],['H','H','H'],[0,0,'H']]
b=[['H','H','H'],['H','0','H'],['H',0,0]]
blue=[]
j,des=srmc(a,b,1,blue,1,'HHHHHH')


# In[104]:


des


# In[102]:


des


# In[68]:


c


# In[36]:


list[1],list[2]=list[0],list[3]


# In[37]:


list


# In[38]:


list[1],list[2]=list[2],list[1]


# In[39]:


list


# In[ ]:




