#!/usr/bin/env python
# coding: utf-8

# In[989]:



import networkx as nx #graph library 
import numpy as np
import math as math
import random as random


# In[990]:


#this is Nabeel's input basically this turns it into something that looks like goalshape1 
testing=[[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]]
step=1;
for i in range(len(testing)):
    for k in range(len(testing[1])):
        if(testing[i][k]==1):
            testing[i][k]=step
            step=step+1


# In[991]:


#create placeholder and test matrix
#some starting parameters 
goalshape1=np.array([[1, 2, 3], [4, 0, 6], [7, 8, 9]])
goalshape=np.array(testing)
places=goalshape-1
choices=["H","P"]
sequences=[]



# In[992]:


#create adjacency matrix, which basically says looking at above, what nodes are interacting. Ie. for node 1, it can interact 
#with nodes 2/4 
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
            


# In[993]:


#Generates all possible hamiltonian paths 
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


# In[994]:


#converts each path into a matrix on a lattice for us to use as a 3 spacethis step might actually be deletable... 
# but it doesn't significantly add to compute time so doesn't matter 
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


# In[995]:


#this generates sequences based on number of choices^sequence length 
sequences=[]
for i in range(pow(len(choices),max(np.ndarray.flatten(goalshape)))):
    val=np.base_repr(i,base=len(choices))
    val=str(val).zfill(max(np.ndarray.flatten(goalshape)))
    for x in range(len(choices)):
        val=val.replace(str(x),choices[x])

    sequences.append(val)


# In[996]:


#partition function
def partition(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


# In[997]:


#this generates sequences too, but does it in a better way so sequences with more non P's get explored first as most structures
#require more H's than P's to be stable 
length=max(np.ndarray.flatten(goalshape));
bases=choices
def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]
sequence=[]
sequences=[]
for i in range(pow(len(bases),length)):
    numb=numberToBase(i,len(bases))
    seq=(numb + length * [0])[:length]    
    sequence.append(seq)
l=sequence.sort(reverse=True,key=sum)
for i in range(len(sequence)):
    sequence[i]=str(sequence[i])
    for k in range(len(choices)):
        sequence[i]=sequence[i].replace(str(k),str(choices[k]))
    sequence[i]=sequence[i].replace(' ','')
    sequence[i]=sequence[i].replace(',','')
    sequence[i]=sequence[i].replace('[','')
    sequence[i]=sequence[i].replace(']','')
sequences=sequence


# In[998]:


sequences


# In[ ]:


#convert sequences and positions into chain. This first section basically turns the matrix back into a string 
#the purpose of this is that I can turn a square into a nxn list that can be directly converted back to positions 
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


# In[ ]:


#generate chains of {positionx,positiony,value} 
#matrixpath=str(matrixpath)
#here I replace the list with the correct sequence value (such as an H etc)
# I then take the nxn chain and turn it into a tuple of {xposition,yposition,value}
for i in range(len(matrixpath)):
    chain=[]
    if (i%500000==0):
        print(i)
    matrixpath[i]=matrixpath[z].replace(str(' '),str(''))  
    matrixpath[i]=matrixpath[z].replace(str(','),str('')) 
    matrixpath[i]=matrixpath[z].replace(str("'"),str('')) 
    for j in range(max(np.ndarray.flatten(goalshape))):
        place=1+j
        if(matrixpath[i][place]!=' ' and matrixpath[i][place]!='0'):
            chain.append([math.floor(j/len(goalshape[1])),j%len(goalshape[1]),matrixpath[i][place]])
    chains.append(chain)


# In[1003]:


matrixpath[1]


# In[ ]:


#this allows us to visualize tuples for debugging and also just being useful 
def graphicchain(chain):
    boundary=np.floor(np.sqrt(len(chain))*2);
    lattice=np.ndarray.tolist(np.zeros([int(boundary),int(boundary)]))
    for i in range(len(chain)):
        lattice[chain[i][0]][chain[i][1]]=chain[i][2]
    lattice=np.array(lattice)
    return(lattice)


# In[ ]:


#COUNTER FUNCTION for each chain; this is actually incorrect, but it doesn't matter in terms of maximizing energy.
#I have a correct version of this in mathematica/Python? maybe somewhere, but I didn't want to find it... 
# note can maybe make faster by not generating a lattice every step? Effectively the problem is it double coutns and it 
#says H-H-P has an H-H interaction when we specifically exclude backbone interactions 
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


# In[976]:



def energystructure(sequence1,targetenergy):
    boundary=np.floor(np.sqrt(len(sequence1))*2);
    #create boundary and parameters. Initialize base lattice all calculations performed on 
    chain=[]
    for i in range(len(sequence1)):
        chain.append([0,0,0])
    lattice=np.zeros([int(boundary),int(boundary)])
    energy=0
    energy1=0;
    #as long as the energy of a structure is below target keep doing this 
    while(energy<targetenergy):
        #wipe values so that we can start again. This lack of recursion allows us to multiprocess very easily 
        energy=0;
        broke=0
        lattice=np.zeros([int(boundary),int(boundary)])
        #print(lattice)
        #create SAW
        chain=[]
        #basically generate an empty chain of length n
        for i in range(len(sequence1)):
            chain.append([0,0,0])
        for j in range(len(sequence1)):
            
            #this is to add the first element in the chain in a random positon on the lattice 
            if(j==0):
                chain[j][0]=random.randint(0,boundary-1)#,random.randint(0,boundary)]#,sequence1[j]]
                chain[j][1]=random.randint(0,boundary-1)
                chain[j][2]=sequence1[j]
                lattice[chain[j][0]][chain[j][1]]=1;
            else:
                #this is to add next elements. How I deal with trapped chains is have the program try to fidn a place
                #20 times. If it fails, it will conclude this cycle and start a new chain 
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
        #calculate the energy of the completed structure 
        energy1=energy1+1               
        energy=counters(chain,lattice)

        #print(energy)
    #print(lattice)
 
    return chain, energy


    


# In[977]:


#for every single possible sequence+path find the energy of it which we use as our goal value for forward folding 
counter=[];
for z in range(len(chains)):

    counter.append(counters(chains[z],goalshape));
#counter=np.array_split(counter,len(sequences))    
#ounter=np.max(counter,axis=1)



# In[978]:


#now we take our best values for each sequence from above and save them in lap
lap=list(partition(counter,len(pathlist)));
ck=lap
for i in range(len(lap)):
    lap[i]=max(lap[i])
len(lap)


# In[979]:



#the following bits are basically just to deal with translations and rotations in a pretty efficient manner. Note the 
#translation+removal functions have no for loops so it's pretty quick 
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
#I think this lets us visualize chains as 1/0s instead of HP but it's not very useful 
def graphicchainno(chain):
    boundary=np.floor(np.sqrt(len(chain))*2);
    lattice=np.ndarray.tolist(np.zeros([int(boundary),int(boundary)]))
    for i in range(len(chain)):
        lattice[chain[i][0]][chain[i][1]]=1
    lattice=np.array(lattice)
    return(lattice)


# In[980]:


c=mattoones(goalshape)
test=removal(goalshape)


# In[981]:


beat=[]
newlap=[]

#for all sequences we should run this program 
for o in range(len(sequences)):
    if o%1000==0:
        print(o)
    #outputs for a sequence and goal minimum energy a chain that does this as well as the calculated energy
    c,y=energystructure(sequences[o],lap[o])
    #this is if no chain exists that beats the goal, which would happen if you limited the number of attempts, the program should give up 
    if y<lap[o]:
        beat.append(sequences[o])
        newlap.append(lap[o]) 
    #this bit is to see if there are any rotations that can do the same thing and then tests the difference from the goal shape 
    #if they are identical there should be no differences 
    else:
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
        elif np.shape(rot1)==np.shape(test):
            if (sqdiff(rot1,test)==0 or sqdiff(rot4,test)==0 or sqdiff(rot21,test)==0 or sqdiff(rot31,test)==0):
                beat.append(sequences[o])
                newlap.append(lap[o])


# In[982]:


#usually run this 4-5 times to probabilistically determine true structures
#run this multiple times 
beat1=beat
newlap1=newlap
beat=[]
newlap=[]
for o in range(len(beat1)):
    if o%100==0:
        print(o)
    c,y=energystructure(beat1[o],newlap1[o])
    if y<newlap1[o]:
        beat.append(beat1[o])
        newlap.append(newlap1[o]) 
    if True:   
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
    
        elif np.shape(rot1)==np.shape(test):
            if (sqdiff(rot1,test)==0 or sqdiff(rot4,test)==0 or sqdiff(rot21,test)==0 or sqdiff(rot31,test)==0):
                beat.append(beat1[o])
                newlap.append(newlap1[o])


# In[988]:


#list of all possible sequences that fit structure 
beat

