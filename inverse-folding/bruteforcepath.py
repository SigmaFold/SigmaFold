#!/usr/bin/env python
# coding: utf-8

# In[1688]:
import networkx as nx #graph library 
import numpy as np
import math as math
import random as random


# In[1689]:


testing=[[1,1,1],[1,1,1],[1,1,1]]
step=1;
for i in range(len(testing)):
    for k in range(len(testing[1])):
        if(testing[i][k]==1):
            testing[i][k]=step
            step=step+1


# In[1690]:


#create placeholder and test matrix
goalshape=np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[0,0,0,0]])
places=goalshape-1
choices=["H","P"]
sequences=[]



# In[ ]:





# In[1691]:


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
            


# In[1692]:


#partition function
def partition(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


# In[1693]:


len(matrixpath)


# In[1694]:


#find all possible paths through a space
pathlist=[]
G=nx.from_numpy_matrix(adjamat)
for x in range(max(np.ndarray.flatten(places)+1)):
    for y in range(max(np.ndarray.flatten(places)+1)):
        for path in nx.all_simple_paths(G,source=x,target=y, cutoff=max(np.ndarray.flatten(goalshape))): 

            if(len(path)>max(np.ndarray.flatten(places))):
                pathlist.append(path)


# In[1695]:


#list of all possible sequences
sequences=[]
for i in range(pow(len(choices),max(np.ndarray.flatten(goalshape)))):
    val=np.base_repr(i,base=len(choices))
    val=str(val).zfill(max(np.ndarray.flatten(goalshape)))
    for x in range(len(choices)):
        val=val.replace(str(x),choices[x])

    sequences.append(val)


# In[1696]:


#convert sequences and positions into chain
matrixpath=[];
relseq=[];  
chains=[];
for z in range(len(sequences)):
    for j in range(len(pathlist)):
        placeholder=np.ndarray.flatten(goalshape);
        strings=np.ndarray.tolist(placeholder)
        for i in reversed(range(len(pathlist[1]))):
        #here use sequence first only

            #strings=strings.replace(str(i),str(sequences[z][i]))
            strings[pathlist[j][i]]=sequences[z][i]
        matrixpath.append(str(strings))
        relseq.append(sequences[z])
#generate chains of {positionx,positiony,value} 
#matrixpath=str(matrixpath)
for z in range(len(matrixpath)):
    matrixpath[z]=matrixpath[z].replace(str(' '),str(''))  
    matrixpath[z]=matrixpath[z].replace(str(','),str('')) 
    matrixpath[z]=matrixpath[z].replace(str("'"),str('')) 
   # matrixpath[z]=matrixpath[z].replace(str('),str(''))  
for i in range(len(matrixpath)):
    chain=[]
    for j in range(max(np.ndarray.flatten(goalshape))):
        place=1+j
        if(matrixpath[i][place]!=' ' and matrixpath[i][place]!='0'):
            chain.append([math.floor(j/len(goalshape[1])),j%len(goalshape[1]),matrixpath[i][place]])
    chains.append(chain)




# In[1697]:


for z in range(len(matrixpath)):
    matrixpath[z]=matrixpath[z].replace(str(' '),str(''))  
    matrixpath[z]=matrixpath[z].replace(str(','),str('')) 
    matrixpath[z]=matrixpath[z].replace(str("'"),str('')) 
   # matrixpath[z]=matrixpath[z].replace(str('),str(''))  
for i in range(len(matrixpath)):
    chain=[]
    for j in range(max(np.ndarray.flatten(goalshape))):
        place=1+j
        if(matrixpath[i][place]!=' ' and matrixpath[i][place]!='0'):
            chain.append([math.floor(j/len(goalshape[1])),j%len(goalshape[1]),matrixpath[i][place]])
    chains.append(chain)


# In[1698]:


#COUNTER FUNCTION for each chain;
# note can maybe make faster by not generating a lattice every step?
counter=[]
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


# In[1699]:


matrixpath


# In[1704]:


def energystructure(sequence1,targetenergy):
    boundary=np.floor(np.sqrt(len(sequence1))*2);
    chain=[]
    for i in range(len(sequence1)):
        chain.append([0,0,0])
    lattice=np.zeros([int(boundary),int(boundary)])
    energy=0
    energy1=0;
    while(energy<targetenergy and energy1<500000):
        energy=0;
        broke=0
        lattice=np.zeros([int(boundary),int(boundary)])
        #print(lattice)
        #create SAW
        chain=[]
        for i in range(len(sequence1)):
            chain.append([0,0,0])
        for j in range(len(sequence1)):
            
            if(j==0):
                chain[j][0]=random.randint(0,boundary-1)#,random.randint(0,boundary)]#,sequence1[j]]
                chain[j][1]=random.randint(0,boundary-1)
                chain[j][2]=sequence1[j]
                lattice[chain[j][0]][chain[j][1]]=1;
            else:
                go=0
                tries=0
                while(go==0 and tries<20 and broke==0):
                    case=random.randint(0,3);
                    if(chain[j-1][0]<boundary-1):
                        if(case==0 and lattice[chain[j-1][0]+1][chain[j-1][1]]==0):
                            chain[j][0]=chain[j-1][0]+1
                            chain[j][1]=chain[j-1][1]
                            go=1
                    if(chain[j-1][0]>0):
                        if(case==1 and lattice[chain[j-1][0]-1][chain[j-1][1]]==0):
                            chain[j][0]=chain[j-1][0]-1
                            chain[j][1]=chain[j-1][1]
                            go=1
                    if(chain[j-1][1]<boundary-1):
                        if(case==2 and lattice[chain[j-1][0]][chain[j-1][1]+1]==0):
                            chain[j][0]=chain[j-1][0]
                            chain[j][1]=chain[j-1][1]+1
                            go=1
                    if(chain[j-1][1]>0):
                        if(case==3 and lattice[chain[j-1][0]][chain[j-1][1]-1]==0):
                            chain[j][0]=chain[j-1][0]
                            chain[j][1]=chain[j-1][1]-1
                            go=1
                    lattice[chain[j][0]][chain[j][1]]=1
                    chain[j][2]=sequence1[j]
                    #print(tries)
                    tries=tries+1
                    if tries==20:
                        broke=1;
        energy1=energy1+1               
        energy=counters(chain,lattice)

        #print(energy)
    #print(lattice)
 
    return chain
    

    


# In[1705]:


counter=[];
for z in range(len(chains)):

    counter.append(counters(chains[z],goalshape));
#counter=np.array_split(counter,len(sequences))    
#ounter=np.max(counter,axis=1)



# In[1706]:


chains


# In[1707]:


#now we take our best values for each sequence and save them in lap
lap=np.array_split(counter,len(sequences));
ck=lap
for i in range(len(lap)):
    lap[i]=max(lap[i])
len(lap)


# In[1708]:


#Let's make the goal shape into a bunch of 1's and 0's representing where we want pieces
def mattoones(goalshape1):
    for i in range(len(goalshape1)):
        for k in range(len(np.transpose(goalshape1))):
            if goalshape1[i][k]!='0.0' and goalshape1[i][k]!=0:
                goalshape1[i][k]=1
    return goalshape1
#Remove all rows/columns at edges with only 0's in order to standardize calculations 
def translator(matrix):
    sums=0;
    while(sum(matrix[0])==0):
        if (sum(matrix[0]==0)):
            matrix=np.delete(matrix,0,0)

    i=len(matrix)-1
    while(sums==0):
        sums=sum(matrix[i]);
        if(sums==0):
            matrix=np.delete(matrix,i,0)
        i=i-1
    return(matrix)

#(*use the above function but for columns too*)
def removal(matrixer):
    c=translator(matrixer);
    c=translator(np.transpose(c))
    return(np.transpose(c))
def sqdiff(m1,m2):
    return (sum(sum((m1-m2)*(m1-m2))))
def graphicchainno(chain):
    boundary=np.floor(np.sqrt(len(chain))*2);
    lattice=np.ndarray.tolist(np.zeros([int(boundary),int(boundary)]))
    for i in range(len(chain)):
        lattice[chain[i][0]][chain[i][1]]=1
    lattice=np.array(lattice)
    return(lattice)


# In[1709]:


c=mattoones(goalshape)
test=removal(goalshape)


# In[1710]:


def graphicchain(chain):
    boundary=np.floor(np.sqrt(len(chain))*2);
    lattice=np.ndarray.tolist(np.zeros([int(boundary),int(boundary)]))
    for i in range(len(chain)):
        lattice[chain[i][0]][chain[i][1]]=chain[i][2]
    lattice=np.array(lattice)
    return(lattice)


# In[1711]:


len(lap)


# In[ ]:


beat=[]
newlap=[]

for o in range(len(sequences)):
    c=energystructure(sequences[o],lap[o])
    usable=mattoones(graphicchainno(c))
    matrix=removal(usable)
    rot1=matrix;
    rot2=np.transpose(matrix)[::-1];
    rot3=np.transpose(matrix[::-1])
    rot4=np.transpose(np.transpose(matrix[::-1])[::-1])
    matrix=np.transpose(matrix)
    rot11=matrix;
    rot21=np.transpose(matrix)[::-1];
    rot31=np.transpose(matrix[::-1])
    rot41=np.transpose(np.transpose(matrix[::-1])[::-1])
    if np.shape(matrix)==np.shape(test):
        if (sqdiff(rot2,test)==0 or sqdiff(rot3,test)==0 or sqdiff(rot11,test)==0 or sqdiff(rot41,test)==0):
            beat.append(sequences[o])
            newlap.append(lap[o])
    if np.shape(rot1)==np.shape(test):
        if (sqdiff(rot1,test)==0 or sqdiff(rot4,test)==0 or sqdiff(rot21,test)==0 or sqdiff(rot31,test)==0):
            beat.append(sequences[o])
            newlap.append(lap[o])


# In[1713]:


beat


# In[1725]:


beat1=beat
newlap1=newlap
beat=[]
newlap=[]

for o in range(len(beat1)):
    c=energystructure(beat1[o],newlap1[o])
    usable=mattoones(graphicchainno(c))
    matrix=removal(usable)
    rot1=matrix;
    rot2=np.transpose(matrix)[::-1];
    rot3=np.transpose(matrix[::-1])
    rot4=np.transpose(np.transpose(matrix[::-1])[::-1])
    matrix=np.transpose(matrix)
    rot11=matrix;
    rot21=np.transpose(matrix)[::-1];
    rot31=np.transpose(matrix[::-1])
    rot41=np.transpose(np.transpose(matrix[::-1])[::-1])
    if np.shape(matrix)==np.shape(test):
        if (sqdiff(rot2,test)==0 or sqdiff(rot3,test)==0 or sqdiff(rot11,test)==0 or sqdiff(rot41,test)==0):
            beat.append(beat1[o])
            newlap.append(newlap1[o])
    if np.shape(rot1)==np.shape(test):
        if (sqdiff(rot1,test)==0 or sqdiff(rot4,test)==0 or sqdiff(rot21,test)==0 or sqdiff(rot31,test)==0):
            beat.append(beat1[o])
            newlap.append(newlap1[o])


# In[1728]:


len(chains)


# In[1566]:


len(beat)


# In[ ]:





# In[ ]:




