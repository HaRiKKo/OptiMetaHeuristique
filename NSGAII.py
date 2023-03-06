# Import python packages
import os
import sys

import random
import numpy as np
import pandas as pd

from src.utils import *

import warnings
warnings.filterwarnings('ignore')

sys.path.insert(0, os.path.dirname(os.path.abspath('constants')))
from constants.parse_parameters import *

# Info sur le model
nb_tache = 5
nb_VM = 3

file_path = read_files(resource_path)

# Read ressources
def read_resources(file_path):

    task_connectivity = pd.read_csv(file_path['Task_connectivity_5.csv'], header=None)
    task_instructions = np.array(pd.read_csv(file_path['Task_instructions_5.csv'], header=0))
    VM_caracteristique = np.array(pd.read_csv(file_path['VM_caracteristique_3.csv'], header=0))
    VM_cost = pd.read_csv(file_path['VM_cost_3.csv'], header=None)
    
    return task_connectivity, task_instructions, VM_caracteristique, VM_cost

task_connectivity, task_instructions, VM_caracteristique, VM_cost = read_resources(file_path)

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
print(starter[0])

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
    
    return max(df_list)

#print("makespan",compute_makespan(starter[0]))

# compute_temps_VM : temps d'actvité d'une VM 
#                   en secondes 
#hypothèse : le temps d'activation d'une VM = DF(dernière tache) - DF(première tache) + temps execution(première tache)
def compute_temps_VM(solution, VM_id):
    tasks_id=[k for k, v in solution.items() if v == VM_id]
    print(tasks_id)
    temps_VM = compute_date_fin(solution, tasks_id[-1]) - compute_date_fin(solution, tasks_id[0]) + compute_temps_execution(tasks_id[0], VM_id)

    return temps_VM

"""NE MARCHE PAS"""
# compute_disponibilité : représente utilisation des VM dans le workflows
def compute_disponibilite(solution):
    somme = 0
    for vm in range(nb_VM):
        #somme += compute_temps_execution(key, solution[key])
        somme += compute_temps_VM(solution, vm)
    print(somme)
    print(compute_makespan(solution))

    return 1/nb_VM * (1-(somme/compute_makespan(solution)))

#print("disponibilité", compute_disponibilite(starter[0]))
# compute_cout : cout total du workflow = cout execution+cout tranferts
def compute_cout(solution):
    # compute le cout d'execution de la solution
    cout_execution = 0
    for key in solution.keys():
        cout_execution += compute_cout_execution(key, solution[key])
    print("cout d'execution :",cout_execution)

    # compute le cout de tranfers de la solution
    cout_transfert = 0
    for idx, i in np.ndenumerate(task_connectivity):
        #print(idx,i)
        if i != 0:
            #print(idx[0], idx[1])
            cout_transfert += compute_cout_transfert(solution, idx[0], idx[1])
    print("cout de transfert",cout_transfert)
    return cout_execution+cout_transfert

#print("cout",compute_cout(starter[0]))

def evaluate_population(population):
    print(population)
    for s in population:
        compute_cout(s)
        compute_makespan(s)
        compute_disponibilite(s)