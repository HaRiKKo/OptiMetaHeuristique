import random
import numpy as np
import pandas as pd

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
    task_instructions = pd.read_csv(task_instructions_path, header=0)
    VM_caracteristique = pd.read_csv(VM_caracteristique_path, header=0)
    VM_cost = pd.read_csv(VM_cost_path, header=None)
    
    return task_connectivity, task_instructions, VM_caracteristique, VM_cost

task_connectivity, task_instructions, VM_caracteristique, VM_cost = read_ressources()

# Random solutions
# solution example :[tâche,VM] [[0,1], [1,2] ,[2,1], [3,3], [4,2]]

# On prend les tâches dans l'ordre et on affecte un VM au hasard VM0, VM1 ou VM2

def random_solution(nb_tache, nb_vm):
    sol=[]
    for i in range(nb_tache):
        sol.append([i,random.randint(0, nb_vm-1)])
    return sol

print(random_solution(5,3))
