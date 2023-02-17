#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import math as math
import random as random


# In[65]:


forwardbias=1
offset=0
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


def srmc(oldmat,newmat,guesse,possibles,temp,sequence):
    bestenergy=guesse
    result=oldmat
    delt=counter(newmat,sequence)-guesse
    if delt>0:
        guesse=counter(newmat,sequence)
        result=newmat
        possibles=[]
        return possibles,result
    elif delt==0:
        possibles.append(newmat)
        result=newmat
        return possibles,result
    else:
        p=random.random()
        if p>math.exp(delt/temp):
            result=newmat
        return possibles,result
#replicalist is a list of {matrix,energy,temperature}
def remc(replicalist,offset):
    i=offset+1
    while i+1<len(replicalist):
        j=i+1
        delta=(replicalist[j][2]-replicalist[i][2])*(-replicalist[i][1]+replicalist[j][1])
        if delta<0:
            replicalist[j][0],replicalist[i][0]=replicalist[i][0],replicalist[j][0]
            replicalist[j][1],replicalist[i][1]=replicalist[i][1],replicalist[j][1]
        else: 
            p=random.random()
            if p<math.exp(-delta):
                            
                replicalist[j][0],replicalist[i][0]=replicalist[i][0],replicalist[j][0]
                replicalist[j][1],replicalist[i][1]=replicalist[i][1],replicalist[j][1]        
    
            
            
            
        
    
    


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




