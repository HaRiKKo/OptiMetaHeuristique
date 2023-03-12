import os
import sys

import numpy as np

from src.utils import *

sys.path.insert(0, os.path.dirname(os.path.abspath("constants")))
from constants.parse_parameters import *

file_path = read_files()
task_connectivity, task_instructions, VM_caracteristique, VM_cost = read_resources(
    file_path
)

# Info sur le model
nb_tache = 15
nb_VM = 3
nb_objectif = 3

# compute_temps_execution : calcule le temps d'execution d'une tache sur une VM
#                           Temps d'execution en secondes
def compute_temps_execution(task_id, VM_id):

    # Nombre d'instruction que contient la tache (#)
    nb_instruction = task_instructions[task_id]
    # Nombre d'instruction par seconde que la VM peut traiter (#/s)
    VM_instruction_per_sec = VM_caracteristique[VM_id][1]

    return nb_instruction / VM_instruction_per_sec


# compute_cout_execution : calcule le cout d'execution d'une tache sur une VM
#                           Cout d'execution en €$£
def compute_cout_execution(task_id, VM_id):

    # Nombre d'instruction que contient la tache (#)
    nb_instruction = task_instructions[task_id]
    # Nombre d'instruction par seconde que la VM peut traiter (#/s)
    VM_instruction_per_sec = VM_caracteristique[VM_id][1]
    # Coût par seconde de la VM (€/s)
    VM_cost_per_sec = VM_caracteristique[VM_id][0]

    return (nb_instruction / VM_instruction_per_sec) * VM_cost_per_sec


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
        if task_connectivity[task_id][previous] != 0:
            previous_connected_tasks.append(previous)

    return compute_temps_execution(task_id, VM_id) + max(
        [0] + [compute_date_fin(solution, task) for task in previous_connected_tasks]
    )


# compute_makespan : temps de completion ou temps d'execution de tout le workflow = date de fin maximum
#                   en secondes
def compute_makespan(solution):
    df_list = [compute_date_fin(solution, tache_id) for tache_id in solution.keys()]
    return max(df_list)


# print("makespan",compute_makespan(starter[0]))

# compute_temps_VM : temps d'actvité d'une VM
#                   en secondes
# hypothèse : le temps d'activation d'une VM = DF(dernière tache) - DF(première tache) + temps execution(première tache)
def compute_temps_VM(solution, VM_id):
    tasks_id = [k for k, v in solution.items() if v == VM_id]
    # print(tasks_id)
    if len(tasks_id) > 0:
        temps_VM = (
            compute_date_fin(solution, tasks_id[-1])
            - compute_date_fin(solution, tasks_id[0])
            + compute_temps_execution(tasks_id[0], VM_id)
        )
        return temps_VM
    else:
        return 0


# compute_disponibilité : représente utilisation des VM dans le workflow
def compute_disponibilite(solution):
    somme = 0
    makespan = compute_makespan(solution)
    for vm in range(nb_VM):
        somme += (-1) * compute_temps_VM(solution, vm) / makespan
    return (1 - somme) / nb_VM


# compute_cout : cout total du workflow = cout execution+cout tranferts
def compute_cout(solution):
    # compute le cout d'execution de la solution
    cout_execution = 0
    for key in solution.keys():
        cout_execution += compute_cout_execution(key, solution[key])

    # compute le cout de tranfers de la solution
    cout_transfert = 0
    for idx, i in np.ndenumerate(task_connectivity):
        if i != 0:
            cout_transfert += compute_cout_transfert(solution, idx[0], idx[1])
    return cout_execution + cout_transfert
