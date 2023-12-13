import numpy as np
def crossover(parent1,parent2):
    position=np.random.randint(1,len(parent1)-1)
    child1=np.concatenate([parent1[:position],parent2[position:]])
    child2=np.concatenate([parent2[:position],parent1[position:]])
    return child1 ,child2


def swap(item , ind1,ind2):
    temp = item[ind1]
    item[ind1]= item[ind2]
    item[ind2]=temp
    return item


def mutation(individual,pm):
    rate=random.random()
    index1=np.random.randint(len(individual))
    index2=np.random.randint(len(individual))
    if rate<pm:
        if index1 != index2:
            swap(individual,index1,index2)
        else:
            index2 +=1
            swap(individual,index1,index2)
    return individual


def crossover_mutation(selected,N):
    len_select=len(selected)
    newpop=np.empty(( len_select,N),dtype=int)
    for i in range(0, len_select,2):
        parent1=selected[i]
        parent2=selected[i+1]
        child1,child2=crossover(parent1,parent2)
        newpop[i]=child1
        newpop[i+1]=child2
    for i in range(N):
        mutation(newpop[i])
    return newpop  



# def crossover_mutation(selected,N):
#     len_select=len(selected)
#     newpop=np.empty(( len_select,N),dtype=int)
#     if(N%2==0):
#         for i in range(0, len_select,2):
#             parent1=selected[i]
#             parent2=selected[i+1]
#             child1,child2=crossover(parent1,parent2)
#             newpop[i]=child1
#             newpop[i+1]=child2
#     if (N %2 !=0):
#         for i in range(0,len_select,1):
#             parent1=selected[i]
#             parent2=selected[i+1]
#             parent3=selected[i+2]
#             child1,child2=crossover(parent1,parent2)
#             child3=crossover(child2,parent3)
#             newpop[i]=child1
#             newpop[i+1]=child2
#             newpop[i+2]=child3
#     for i in range(N):
#         mutation(newpop[i])
#     return newpop 









