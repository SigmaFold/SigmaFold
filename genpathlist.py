#!/usr/bin/env python
# coding: utf-8

# In[1]:



import networkx as nx #graph library 
import numpy as np
import math as math
import random as random


# In[2]:


testing=[[1,1,1],[1,1,1],[1,1,1]]
step=1;
for i in range(len(testing)):
    for k in range(len(testing[1])):
        if(testing[i][k]==1):
            testing[i][k]=step
            step=step+1


# In[3]:


#create placeholder and test matrix
goalshape=np.array(testing)
places=goalshape-1
choices=["H","P"]
sequences=[]



# In[4]:


#create adjacency matrix
adjamat=np.zeros([max(np.ndarray.flatten(goalshape)),max(np.ndarray.flatten(goalshape))]);
for i in range(len(goalshape[1])):
    for j in range(len(goalshape)):
        if(j<len(goalshape)-1):
            if(goalshape[j][i]>0 and goalshape[j+1][i]!=0):
                adjamat[places[j+1][i]][places[j][i]]=1
                
        if(j>0):
            if(goalshape[j][i]>0 and goalshape[j-1][i]!=0):
                adjamat[places[j-1][i]][places[j][i]]=1
        if(i<len(goalshape[1])-1):
            if(goalshape[j][i]>0 and goalshape[j][i+1]!=0):
                adjamat[places[j][i]][places[j][i+1]]=1
                
        if(i>0):
            if(goalshape[j][i]>0 and goalshape[j][i-1]!=0):
                adjamat[places[j][i]][places[j][i-1]]=1
            


# In[5]:


pathlist=[]
G=nx.from_numpy_matrix(adjamat)
for x in range(max(np.ndarray.flatten(places)+1)):
    for y in range(max(np.ndarray.flatten(places)+1)):
        for path in nx.all_simple_paths(G,source=x,target=y, cutoff=max(np.ndarray.flatten(goalshape))): 

            if(len(path)>max(np.ndarray.flatten(places))):
                pathlist.append(path)


# In[6]:


pathmat=[]
for i in range(len(pathlist)):
    specpath=[]
    for j in range(max(pathlist[1])+1):
        specpath.append([math.floor(pathlist[i][j]/len(goalshape[1])),pathlist[i][j]%len(goalshape[1]),int(j+1)])
    pathmat.append(specpath)


# In[9]:


def graphicchain(chain):
    boundary=np.floor(np.sqrt(len(chain))*2);
    lattice=np.ndarray.tolist(np.zeros([int(boundary),int(boundary)]))
    for i in range(len(chain)):
        lattice[chain[i][0]][chain[i][1]]=chain[i][2]
    lattice=np.array(lattice)
    return(lattice)


# In[13]:


graphicchain(pathmat[3])


# In[ ]:




