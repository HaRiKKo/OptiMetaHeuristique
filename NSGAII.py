# Import python packages
import random
import numpy as np
import pandas as pd

# Info sur le model
nb_tache = 5
nb_VM = 3

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
#print(starter)

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

def compute_cout_transfert(solution, tache_source, tache_dest):
    VM_source = solution[tache_source]
    VM_dest = solution[tache_dest]
    
    data_tranfert = task_connectivity[tache_dest][tache_source]
    cout_communication = VM_cost[VM_dest][VM_source]

    return data_tranfert * cout_communication


# compute_date_fin : calcule la date de fin d'une tache = le temps entre le début du traitement de la premier tache et la fin de la tache cible 
#                   date de fin en seconde
def compute_date_fin(solution, task_id):
    # Récupération de l'id de la VM pour la tâche task_id
    VM_id = solution[task_id]
    # Recherche des tâches précédentes
    previous_connected_tasks = []
    for previous in range(len(solution)):
        if task_connectivity[task_id][previous] !=0 :
            previous_connected_tasks.append(previous)

    return compute_temps_execution(task_id, VM_id) + max([0]+[compute_date_fin(solution, task) for task in previous_connected_tasks])

"""
test = starter[0]
print("solution : ",test)
print(compute_temps_execution(0,test[0]))

for i in range(5):
     print("current task id:",i)
     print("date fin:")
     print(compute_date_fin(test,i))
"""

def compute_makespan(solution):
    df_list=[compute_date_fin(solution, tache_id) for tache_id in solution.keys()]
    
    return max(df_list)

#print(compute_makespan(starter[0]))

def compute_disponibilite(solution):
    somme = 0
    for key in solution.keys():
        somme += compute_temps_execution(key, solution[key])

        return 1/nb_VM * (1-somme/compute_makespan(solution))
