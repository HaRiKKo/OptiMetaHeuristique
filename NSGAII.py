# Import python packages
import random
import numpy as np
import pandas as pd

# Info sur le model
nb_tache = 5
nb_VM = 3
nb_objectif=3

# Ressources paths
task_connectivity_path = './ressources/Task_connectivity_5.csv'
task_instructions_path = './ressources/Task_instructions_5.csv'
VM_caracteristique_path = './ressources/VM_caracteristique_3.csv'
VM_cost_path= './ressources/VM_cost_3.csv'

# Read ressources
def read_ressources(task_connectivity_path=task_connectivity_path,
                    task_instructions_path=task_instructions_path,
                    VM_caracteristique_path=VM_caracteristique_path,
                    VM_cost_path=VM_cost_path):

    task_connectivity = pd.read_csv(task_connectivity_path, header=None)
    task_instructions = np.array(pd.read_csv(task_instructions_path, header=0))
    VM_caracteristique = np.array(pd.read_csv(VM_caracteristique_path, header=0))
    VM_cost = pd.read_csv(VM_cost_path, header=None)
    
    return task_connectivity, task_instructions, VM_caracteristique, VM_cost

task_connectivity, task_instructions, VM_caracteristique, VM_cost = read_ressources()

#print(task_connectivity)
# Random solutions
# solution example :[tâche,VM] [[0,1], [1,2] ,[2,1], [3,3], [4,2]]

# On prend les tâches dans l'ordre et on affecte un VM au hasard VM0, VM1 ou VM2
def random_solution(nb_tache, nb_vm):
    sol={}
    for i in range(nb_tache):
        sol[i] = random.randint(0, nb_vm-1)
    return sol

# Création de la opulation de départ 
def create_start_population(nb_pop=10):
    starter=[]
    for i in range(nb_pop):
        starter.append(random_solution(nb_tache, nb_VM))
    return starter

starter=create_start_population()
#print(starter[0])

# Fonction d'évaluation de la solution 
# Coût 
# Makespan
# Disponibilité

# compute_temps_execution : calcule le temps d'execution d'une tache sur une VM
#                           Temps d'execution en secondes
def compute_temps_execution(task_id, VM_id):

    # Nombre d'instruction que contient la tache (#)
    nb_instruction = task_instructions[task_id]
    # Nombre d'instruction par seconde que la VM peut traiter (#/s)
    VM_instruction_per_sec = VM_caracteristique[VM_id][1]
    
    return (nb_instruction/VM_instruction_per_sec)

# compute_cout_execution : calcule le cout d'execution d'une tache sur une VM
#                           Cout d'execution en €$£
def compute_cout_execution(task_id, VM_id):

    # Nombre d'instruction que contient la tache (#)
    nb_instruction = task_instructions[task_id]
    # Nombre d'instruction par seconde que la VM peut traiter (#/s)
    VM_instruction_per_sec = VM_caracteristique[VM_id][1]
    # Coût par seconde de la VM (€/s)
    VM_cost_per_sec = VM_caracteristique[VM_id][0]
    
    return (nb_instruction/VM_instruction_per_sec) * VM_cost_per_sec

# compute_cout_execution : calcule le cout de transfert pour le partage des donnée d'une VM à une autres entre deux taches
#                           Cout de transferts en €$£
def compute_cout_transfert(solution, tache_source, tache_dest):
    VM_source = solution[tache_source]
    VM_dest = solution[tache_dest]
    
    data_tranfert = task_connectivity[tache_dest][tache_source]
    cout_communication = VM_cost[VM_dest][VM_source]

    return data_tranfert * cout_communication


# compute_date_fin : calcule la date de fin d'une tache = le temps entre le début du traitement de la premier tache et la fin de la tache cible 
#                   date de fin en secondes
def compute_date_fin(solution, task_id):
    # Récupération de l'id de la VM pour la tâche task_id
    VM_id = solution[task_id]
    # Recherche des tâches précédentes
    previous_connected_tasks = []
    for previous in range(len(solution)):
        if task_connectivity[task_id][previous] !=0 :
            previous_connected_tasks.append(previous)

    return compute_temps_execution(task_id, VM_id) + max([0]+[compute_date_fin(solution, task) for task in previous_connected_tasks])

# compute_makespan : temps de completion ou temps d'execution de tout le workflow = date de fin maximum
#                   en secondes
def compute_makespan(solution):
    df_list=[compute_date_fin(solution, tache_id) for tache_id in solution.keys()]
    
    #print("makespan", max(df_list))
    return max(df_list)

#print("makespan",compute_makespan(starter[0]))

# compute_temps_VM : temps d'actvité d'une VM 
#                   en secondes 
#hypothèse : le temps d'activation d'une VM = DF(dernière tache) - DF(première tache) + temps execution(première tache)
def compute_temps_VM(solution, VM_id):
    tasks_id=[k for k, v in solution.items() if v == VM_id]
    #print(tasks_id)
    if len(tasks_id)>0:
        temps_VM = compute_date_fin(solution, tasks_id[-1]) - compute_date_fin(solution, tasks_id[0]) + compute_temps_execution(tasks_id[0], VM_id)
        return temps_VM
    else:
        return 0

"""NE MARCHE PAS"""
# compute_disponibilité : représente utilisation des VM dans le workflows
def compute_disponibilite(solution):
    somme = 0
    makespan = compute_makespan(solution)
    for vm in range(nb_VM):
        #somme += compute_temps_execution(key, solution[key])
        somme += compute_temps_VM(solution, vm)/makespan
    #print(somme)
    #print(compute_makespan(solution))

    #print("disponibilité", 1/nb_VM * (1-somme))
    return 1/nb_VM * (1-somme)

#print("disponibilité", compute_disponibilite(starter[0]))
# compute_cout : cout total du workflow = cout execution+cout tranferts
def compute_cout(solution):
    # compute le cout d'execution de la solution
    cout_execution = 0
    for key in solution.keys():
        cout_execution += compute_cout_execution(key, solution[key])
    #print("cout d'execution :",cout_execution)

    # compute le cout de tranfers de la solution
    cout_transfert = 0
    for idx, i in np.ndenumerate(task_connectivity):
        #print(idx,i)
        if i != 0:
            #print(idx[0], idx[1])
            cout_transfert += compute_cout_transfert(solution, idx[0], idx[1])
    #print("cout de transfert",cout_transfert)

    #print("cout total", cout_execution+cout_transfert)
    return cout_execution+cout_transfert

#print("cout",compute_cout(starter[0]))

def evaluate_population(population):
    print("population",population)
    print()
    score={}
    for s in population:
        cout = compute_cout(s)[0]
        makespan = compute_makespan(s)[0]
        dispo = compute_disponibilite(s)[0]
        score[population.index(s)] = [cout, makespan, dispo]
    print("score",score)
    print()
    return score

score = evaluate_population(starter)

# ranking des population selon la methode NSGA:
## rank 1: solution non dominée
## rank 2: solution dominé par les ranks 1
## rank 3: solution dominé par les ranks 2
## ... 

# liste des solutions dominantes de chaque solution
def dominance(score):
    dominance={}
    for key in score.keys(): # pour chaque clé = solution
        print("##############", key)
        dominante=list(score.keys()) #initialisé la liste des solutions dominantes à toute les solutions
        #print(dominante)
        for i in range(3): # pour chaque objectif 
            objectif_key = score[key][i] # on récupère sa valeur
            print()
            print("objectif",i)
            print("objectif_key",objectif_key)
            #print(dominante)
            for s in list(dominante): # pour chaque solution dominante 
                print("solution teste", s)
                print("score solution",score[s][i])
                if (objectif_key<=score[s][i]): # on regarde si l'objectif de la solution ciblé est inferieur à l'objectif de la solution dominante 
                    dominante.remove(s) # si oui alors on supprime la solution dominante de la liste
                #print(dominante)
        #rank[key]=len(dominante)+1
        dominance[key]=dominante
    print("dominance",dominance)
    print()
    return dominance

# calcule du rank d'une solution à l'aide de sa liste de solution dominante
def compute_rank(rank, list):
    r_max=2
    for e in list:
        if rank[e]>=r_max:
            print(e)
            print(rank[e])
            r_max=rank[e]+1
    return r_max

# calcule du rank de toute les solution
def ranking(score):
    # on récupère la list des dominance et on la trie
    dominance_list = dominance(score)
    dominance_list_sorted = {k:v for k,v in sorted(dominance_list.items(), key=lambda l:len(l[1]))} 
    print(dominance_list_sorted) #les solution avec le mins de dominance au début
    rank={}

    for k in dominance_list_sorted.keys(): # pour chaque solution
        if len(dominance_list[k])==0: # on attribue le rank 1 au solution sans dominance 
            rank[k]=1
        else:
            r=compute_rank(rank, dominance_list[k]) # on calcule le rank des autres solutions = rank max de leur dominance +1
            rank[k]=r 
    print(rank)
    return rank

ranking(score)
            
