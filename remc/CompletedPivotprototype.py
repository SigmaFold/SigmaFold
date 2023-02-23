import numpy as np
import numpy as np
import math as math
import random as random
from copy import deepcopy

#this allows us to visualize tuples for debugging and also just being useful 
def graphicchain(chain,matrix):

    lattice=np.ndarray.tolist(np.zeros([len(matrix),len(matrix)]))
    for i in range(len(chain)):
        lattice[chain[i][1]][chain[i][2]]=chain[i][0]
    lattice=np.array(lattice)
    return(lattice)


# choosing the right VSHD move
def vsdh_move(seq, n, mate, positionsk):
    # choose a random number between 1 to n inclusive
    random_number = np.random.randint(1,n+1)
    positions=deepcopy(positionsk)
    old_mat=deepcopy(mate)
    mod=deepcopy(mate)
    new_mat=deepcopy(mate)
    #print(mate)
    # random_number = 4
    #print(f'Random number chosen: {random_number}')

    if random_number == 1 or random_number == n:
        # call the end_pull function
        #print(mate)
        #print(mate)
        #print(new_mat)
        new_mat, positions = end_move(random_number, seq, n, mod, positions)
        return new_mat, positions
    else:
        # call the corner_pull function
        new_mat, positions = corner_move(random_number, seq, n, mod, positions)
        #print(mate)
        #print(mate)
        #print(new_mat)
        return new_mat,positions
    # check if the matrix has changed
    #if np.ndarray.tolist(new_mat) == np.ndarray.tolist(old_mat):
        #print(mate)
        #print(mat)
        #return old_mat,positions
    
    
# end move
def end_move(rand_num, seq, n, mat,positions):
    free_spaces = []

    if rand_num==1:
        [row_1, col_1] = [positions[0][1],positions[0][2]]
        [row_2, col_2] = [positions[1][1],positions[1][2]]   
        # find adjacent free spaces to the 2nd element
        if row_2>0:
            if mat[row_2-1, col_2] == 0 or mat[row_2-1, col_2] == '0.0' or mat[row_2-1, col_2] == '0':
                free_spaces.append([row_2-1, col_2])
        if row_2<len(mat)-1:
            if mat[row_2+1, col_2] == 0 or mat[row_2+1, col_2] == '0.0'or mat[row_2-1, col_2] == '0':
                free_spaces.append([row_2+1, col_2])
        if col_2>0:
            if mat[row_2, col_2-1]== 0 or mat[row_2, col_2-1] == '0.0'or mat[row_2-1, col_2] == '0':
                free_spaces.append([row_2, col_2-1])
        if col_2<len(mat[1])-1:
            if mat[row_2, col_2+1] == 0 or mat[row_2, col_2+1] == '0.0'or mat[row_2-1, col_2] == '0':
                free_spaces.append([row_2, col_2+1])
        #print(f'Free Spaces: {free_spaces}')
        if len(free_spaces)>0:
            random_space = np.random.randint(0,len(free_spaces))
        #this bit should be optimized 
        #new_mat=(np.ndarray.tolist((np.zeros((len(mat),len(mat[1]))))))
        # choose a random free space
       
        
        # move 1st position to the random free space
        
            mat[free_spaces[random_space][0]][ free_spaces[random_space][1]] = positions[0][0]
            mat[row_1][col_1] = 0.0
            positions[0]=[positions[0][0],free_spaces[random_space][0], free_spaces[random_space][1]]
        return mat,positions
    else:
        # find index of the last and 2nd last elements of the sequence in the matrix
        #[[row_end], [col_end]] = np.where(mat == n)
        #[[row_2end], [col_2end]] = np.where(mat == n-1)
        [row_end, col_end] = [positions[n-1][1],positions[n-1][2]]
        [row_2end, col_2end] = [positions[n-2][1],positions[n-2][2]]  
        # find adjacent free spaces to the 2nd last element
        if row_2end>0:
            if mat[row_2end-1, col_2end] == 0 or mat[row_2end-1, col_2end] == '0.0' or mat[row_2end-1, col_2end] == '0':
                free_spaces.append([row_2end-1, col_2end])
        if row_2end<len(mat)-1:
            if mat[row_2end+1, col_2end]== 0 or mat[row_2end+1, col_2end] == '0.0' or mat[row_2end+1, col_2end] == '0':
                free_spaces.append([row_2end+1, col_2end])
        if col_2end>0:
            if mat[row_2end, col_2end-1]==0 or mat[row_2end, col_2end-1] == '0.0' or mat[row_2end, col_2end-1] == '0':
                free_spaces.append([row_2end, col_2end-1])
        if col_2end<len(mat[1])-1:
        
            if mat[row_2end, col_2end+1]==0 or mat[row_2end, col_2end+1] == '0.0' or mat[row_2end, col_2end+1] == '0' :
                free_spaces.append([row_2end, col_2end+1])
        #print(f'Free Spaces: {free_spaces}')
        
        # choose a random free space
        #print(free_spaces)
        if len(free_spaces)>0:
            random_space = np.random.randint(0,len(free_spaces))
        # move last position to the random free space
            mat[free_spaces[random_space][0], free_spaces[random_space][1]] = positions[n-1][0]
            mat[row_end, col_end] = 0.0
            positions[n-1]=[positions[n-1][0],free_spaces[random_space][0], free_spaces[random_space][1]]
        return mat,positions
    

# corner move
def corner_move(rand_num, seq, n, mat,positions):
    free_spaces_bef = []
    free_spaces_aft = []
    
    # find the index of the element, the element before and the alement after it in the sequence in the matrix
    [row_1, col_1] = [positions[0][1],positions[0][2]]
    [row_num,col_num] = [positions[rand_num-1][1],positions[rand_num-1][2]]
    [row_bef,col_bef] = [positions[rand_num-2][1],positions[rand_num-2][2]]
    [row_aft,col_aft] = [positions[rand_num][1],positions[rand_num][2]]
    
    # find adjacent free spaces to the element before
    # TODO: make it more efficient by checking corners of element 
    if row_bef>0:
        if mat[row_bef-1, col_bef]==0 or mat[row_bef-1, col_bef] == '0.0' or mat[row_bef-1, col_bef] == '0' :
            free_spaces_bef.append([row_bef-1, col_bef])
    if row_bef<len(mat)-1:

        if mat[row_bef+1, col_bef]==0 or mat[row_bef+1, col_bef] == '0.0' or mat[row_bef+1, col_bef] == '0' :
            free_spaces_bef.append([row_bef+1, col_bef])
    if col_bef>0:        
        if mat[row_bef, col_bef-1]==0 or mat[row_bef, col_bef-1] == '0.0' or mat[row_bef, col_bef-1] == '0' :
            free_spaces_bef.append([row_bef, col_bef-1])
    if col_bef<len(mat)-1:
        if mat[row_bef, col_bef+1]==0 or mat[row_bef, col_bef+1] == '0.0' or mat[row_bef, col_bef+1] == '0' :
            free_spaces_bef.append([row_bef, col_bef+1])
    # find adjacent free spaces to the element before
    if row_aft>0:
    
        if mat[row_aft-1, col_aft]==0 or mat[row_aft-1, col_aft] == '0.0' or mat[row_aft-1, col_aft] == '0' :
            free_spaces_aft.append([row_aft-1, col_aft])
    if row_aft<len(mat)-1:
        
        if mat[row_aft+1, col_aft]==0 or mat[row_aft+1, col_aft] == '0.0' or mat[row_aft+1, col_aft] == '0' :
            free_spaces_aft.append([row_aft+1, col_aft])
    if col_aft>0:
        if mat[row_aft, col_aft-1]==0 or mat[row_aft, col_aft-1] == '0.0' or mat[row_aft, col_aft-1] == '0' :
            free_spaces_aft.append([row_aft, col_aft-1])
    if col_aft<len(mat)-1:
        if mat[row_aft, col_aft+1]==0 or mat[row_aft, col_aft+1] == '0.0' or mat[row_aft, col_aft+1] == '0' :
            free_spaces_aft.append([row_aft, col_aft+1])    
    
    # find the common free space between the two lists
    common_space = list(set(tuple(x) for x in free_spaces_bef) & set(tuple(x) for x in free_spaces_aft))
    #print(f'Common Space: {common_space}')
    
    if len(common_space) == 0:
        pass
    else:
        # choose a random common free space
        random_space = np.random.randint(0,len(common_space))
        # move the element to the random common free space

        
        mat[common_space[random_space][0], common_space[random_space][1]] = positions[rand_num-1][0]
        #print(f'oldplace: {row_num,col_num}')
        mat[row_num, col_num] = 0.0
        positions[rand_num-1]=[positions[rand_num-1][0],common_space[random_space][0], common_space[random_space][1]]
    return mat,positions


#energy function 
def counter(matrix,sequence):
    extras=0
    count=0
    for i in range(len(sequence)):
        #basically count how many interactions occur within the sequence and must be removed
        if sequence[i]!="P":
            if i<len(sequence)-1:
                if sequence[i]==sequence[i+1] and i<len(sequence)-1:
                    extras=extras+1
            if i>0:        
                if sequence[i]==sequence[i-1] and i>0:
                    extras=extras+1
    #given a matrix, loop through and count the energy. This can be much more efficient by only looking locally via using the chain 
    for i in range(len(matrix)):
        for j in range(len(matrix[1])):
            if matrix[i][j]!="P" and matrix[i][j]!=0 and matrix[i][j]!='0' and matrix[i][j]!='0.0':
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


def srmc(oldmat,newmat,bestenergy,possibles,temp,sequence,positionsj,positionsold):
    positions=deepcopy(positionsold)
    guesse=counter(oldmat,sequence)
    result=deepcopy(oldmat)
    currentenergy=counter(newmat,sequence)
    #calculate differences in energy between matrices
    delt=currentenergy-guesse
    #print(graphicchain(positions,test_matrix))
    #depending on whether the new energy is better or not choose three states
    if delt>0:
        #if new energy is closer to ground state, switch structure. 
        
        result=newmat
        #if the newenergy is actually the best we've seen so far. Reset best energy and degen list
        if currentenergy==bestenergy:
            possibles.append(result)
        if currentenergy>bestenergy:
            bestenergy=counter(newmat,sequence)
            possibles=[result]
        positions=deepcopy(positionsj)

            
        return possibles,result,bestenergy,currentenergy,positions
    #if the energies are equal, go with new structure
    elif delt==0:
        #if the energy equal to best energy, add it to degeneracy list 
        result=newmat
        if currentenergy==bestenergy:
            possibles.append(result)
        positions=deepcopy(positionsj)
        
        return possibles,result,bestenergy,currentenergy,positions
    else:
        #if the newmat is worse than oldmat, probabilistically switch to newmat
        p=random.random()
        if p<math.exp(speedfactor*delt/temp):
            result=newmat
            positions=deepcopy(positionsj)
        #possibles=[possibles]
        return possibles,result,bestenergy,currentenergy,positions


#replicalist is a list of {matrix,energy,temperature}
#fix to be matrix,positions,energy,temperature
def remc(replicalist,offset):
    #offset to allow comparisons between different pairs 
    i=offset+1
    while i+1<len(replicalist):
        #basically compare each replica with the one next over with weighting from the temperature 
        j=i+1
        delta=(-replicalist[j][3]+replicalist[i][3])*(-replicalist[i][2]+replicalist[j][2])
        if delta<0:
            #this means either the temoperature or energy is wrong, so we need to switch the temperatures (I chose to switch the matrixes instead) 
                replicalist[j][0],replicalist[i][0]=replicalist[i][0],replicalist[j][0]
                replicalist[j][1],replicalist[i][1]=replicalist[i][1],replicalist[j][1]
                replicalist[j][2],replicalist[i][2]=replicalist[i][2],replicalist[j][2]
        else: 
            p=random.random()
            if p<math.exp(-delta):
                #probability of switching if actually the first is better than the second 
                replicalist[j][0],replicalist[i][0]=replicalist[i][0],replicalist[j][0]
                replicalist[j][1],replicalist[i][1]=replicalist[i][1],replicalist[j][1]
                replicalist[j][2],replicalist[i][2]=replicalist[i][2],replicalist[j][2]
    #change the offset 
        i=i+1

    offset=1-offset
    return replicalist,offset


#generate replicas with info matrix,path,energy,temp 
def genreplicalist(startmatrix,positions,numberofthings,starttemp,endtemp):
    z=[]
    energy=counter(startmatrix,sequence)
    for i in range(numberofthings):
        #equation for temp assignment
        tempstep=starttemp+(i)*(endtemp-starttemp)/(numberofthings-1)
        z.append([startmatrix,positions,energy,tempstep])
    return z


#final code

#fix to be matrix,positions,energy,temperature

#generate replicalist off random sequence 
def singlestep(replicalist,possibles,truebestenergy):
    #do this for each replica
    for i in range(len(replicalist)):
        #save our initials 
        old=deepcopy(replicalist[i][0])
        oldmemory=deepcopy(replicalist[i][0])
        temp=replicalist[i][3]
        positions12=deepcopy(replicalist[i][1])
        bestenergy1=truebestenergy
        #create a set of new matrices with a single move difference 
        new_matrix,positions13=vsdh_move(sequence,n,old,positions12)
        #decide whether to keep the new or old matrix based on delta energy difference
        possibles,result,bestenergy,currentenergy,positions15=srmc(oldmemory,new_matrix,bestenergy1,possibles,temp,sequence,positions13,positions12)
        #update the replica 
        replicalist[i][0],replicalist[i][1],replicalist[i][2]=result,positions15,currentenergy

        #potentially update best energy seen so far 
        if currentenergy>truebestenergy:
            truebestenergy=currentenergy
            
    return replicalist,truebestenergy,possibles
        

#replicalist,truebestenergy,possibles
def alltogether(positions,numberofthings,starttemp,endtemp,latticesize,guesstruebest,offset,time,sequence):
   empty=np.zeros((latticesize,latticesize))
   startmatrix=graphicchain(positions,empty)

   possibles=[]
   deltatime=0
   truebestenergy=guesstruebest
   #generate base replicates off some guess positions 
   replicates=genreplicalist(startmatrix,positions,numberofthings,starttemp,endtemp)
   zees=deepcopy(replicates)
   #can change this to time step, so choose number of iterations 
   while truebestenergy<9:
       #print(deltatime)
   #generate a replicalist of the size specified at the start
       #choose replicas to keep/changes to make 
       zees,truebestenergy,possibles=singlestep(zees,possibles,truebestenergy)
       #correct the temperature accordingly via remc 
       zees,offset=remc(zees,offset)
       deltatime=deltatime+1
       avgs[0]=avgs[0]+counter(zees[0][0],sequence)
       avgs[4]=avgs[4]+counter(zees[4][0],sequence)
   #print("end")
   return zees,truebestenergy,possibles


if __name__ == "__main__":
    forwardbias=1
    offset=0
    bestenergy=0
    sequence = "HHHHHHHHPHHHHPHH"
    speedfactor=2
    possibles=[]
    n = len(sequence)
    
    #create a test matrix of size 11X11 where the origin is at the center [5,5]
    test_matrix = np.ndarray.tolist(np.zeros((10,10)))
    positions1=[['H',4, 5],['H',5, 5],['H',5, 4], ['H',6, 4],['H',6, 5],['H',7, 5],['H',7, 4],['H',7, 3],['P',7, 2],['H',6, 2],['H',6, 3],['H',5, 3],['H',5, 2],['P',4, 2],['H',4, 3],['H',4, 4]]
    test_matrix=graphicchain(positions1,test_matrix)
    test_matrix=np.array(test_matrix)

    len(positions1)

    counter(test_matrix,sequence)

    p,r,b,c,p1=srmc(test_matrix,o1,bestenergy,possibles,15,sequence,p1,positions1)
    genreplicalist(test_matrix,positions1,5,160,220);
    replicates=genreplicalist(test_matrix,positions1,5,5,1)
    possibles=[]

    avgs=[0,0,0,0,0]

    #replicalist,best energy, list of structures with best energy

    r,t,p=alltogether(r[1][1],5,160,220,10,0,0,60000,sequence)