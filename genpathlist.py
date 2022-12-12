#!/usr/bin/env python
# coding: utf-8

# In[207]:



import networkx as nx #graph library 
import numpy as np
import math as math
import random as random


# In[208]:


testing=[[1,1,1],[1,0,0],[1,1,1]]
step=1;
for i in range(len(testing)):
    for k in range(len(testing[1])):
        if(testing[i][k]==1):
            testing[i][k]=step
            step=step+1


# In[210]:


#create placeholder and test matrix
goalshape1=np.array([[1, 2, 3], [4, 0, 6], [7, 8, 9]])
goalshape=np.array(testing)
places=goalshape-1
choices=["H","P"]
sequences=[]



# In[211]:


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
            


# In[212]:


pathlist=[]
G=nx.from_numpy_matrix(adjamat)
for x in range(max(np.ndarray.flatten(places)+1)):
    for y in range(max(np.ndarray.flatten(places)+1)):
        for path in nx.all_simple_paths(G,source=x,target=y, cutoff=max(np.ndarray.flatten(goalshape))): 

            if(len(path)>max(np.ndarray.flatten(places))):
                pathlist.append(path)
#This is for accounting for any zeros in the middle within the path
addzeros=[]
for i in range(len(np.ndarray.flatten(goalshape))):
    if np.ndarray.flatten(goalshape)[i]==0:
        addzeros.append(i)
  #fix path list
for k in range(len(addzeros)):
    for j in range(len(pathlist)):
        for i in range(len(pathlist[j])):
            if addzeros[k]<pathlist[j][i] or addzeros[k]==pathlist[j][i]:
                pathlist[j][i]=pathlist[j][i]+1 


# In[213]:


pathlist


# In[214]:





# In[217]:


pathmat=[]

for i in range(len(pathlist)):
    count=0;
    specpath=[]
    current=pathlist[i]

    for j in range(len(pathlist[1])):
        if goalshape[math.floor(pathlist[i][j]/len(goalshape[1])),pathlist[i][j]%len(goalshape[1])]!=0:
            specpath.append([math.floor(pathlist[i][j]/len(goalshape[1])),pathlist[i][j]%len(goalshape[1]),int(j+1)])
        else:
            count=count+1

    pathmat.append(specpath)


# In[218]:


def graphicchain(chain):
    boundary=np.floor(np.sqrt(len(chain))*2);
    lattice=np.ndarray.tolist(np.zeros([int(boundary),int(boundary)]))
    for i in range(len(chain)):
        lattice[chain[i][0]][chain[i][1]]=chain[i][2]
    lattice=np.array(lattice)
    return(lattice)


# In[219]:


graphicchain(pathmat[1])


# In[ ]:




