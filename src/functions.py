import random

# Info sur le model
nb_tache = 5
nb_VM = 3

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

# Fonction d'évaluation de la solution 
# Coût 
# Makespan
# Disponibilité

"""
def evaluate_population(population):
    print(population)
    for s in population:
        compute_cout(s)
        compute_makespan(s)
        compute_disponibilite(s)
"""