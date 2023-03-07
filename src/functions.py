import random

from src.compute_objectives import *

# print(task_connectivity)
# Random solutions
# solution example :[tâche,VM] [[0,1], [1,2] ,[2,1], [3,3], [4,2]]

# On prend les tâches dans l'ordre et on affecte un VM au hasard VM0, VM1 ou VM2
def random_solution(nb_tache, nb_vm):
    sol = {}
    for i in range(nb_tache):
        sol[i] = random.randint(0, nb_vm - 1)
    return sol


# Création de la opulation de départ
def create_start_population(nb_pop=10):
    starter = []
    for i in range(nb_pop):
        starter.append(random_solution(nb_tache, nb_VM))
    return starter


# Fonction d'évaluation de la solution
# Coût
# Makespan
# Disponibilité


def evaluate_population(population):
    print("population", population)
    print()
    score = {}
    for i in range(len(population)):
        cout = compute_cout(population[i])[0]
        makespan = compute_makespan(population[i])[0]
        dispo = compute_disponibilite(population[i])[0]
        score[i] = [cout, makespan, dispo]
    print("score", score)
    print()
    return score


# ranking des population selon la methode NSGA:
## rank 1: solution non dominée
## rank 2: solution dominé par les ranks 1
## rank 3: solution dominé par les ranks 2
## ...

# liste des solutions dominantes de chaque solution
def dominance(score):
    dominance = {}
    for key in score.keys():  # pour chaque clé = solution
        print("##############", key)
        dominante = list(
            score.keys()
        )  # initialisé la liste des solutions dominantes à toute les solutions
        # print(dominante)
        for i in range(3):  # pour chaque objectif
            objectif_key = score[key][i]  # on récupère sa valeur
            print()
            print("objectif", i)
            print("objectif_key", objectif_key)
            # print(dominante)
            for s in list(dominante):  # pour chaque solution dominante
                print("solution teste", s)
                print("score solution", score[s][i])
                if (
                    objectif_key <= score[s][i]
                ):  # on regarde si l'objectif de la solution ciblé est inferieur à l'objectif de la solution dominante
                    dominante.remove(
                        s
                    )  # si oui alors on supprime la solution dominante de la liste
                # print(dominante)
        # rank[key]=len(dominante)+1
        dominance[key] = dominante
    print("dominance", dominance)
    print()
    return dominance


# calcule du rank d'une solution à l'aide de sa liste de solution dominante
def compute_rank(rank, list):
    r_max = 2
    for e in list:
        if rank[e] >= r_max:
            print(e)
            print(rank[e])
            r_max = rank[e] + 1
    return r_max


# calcule du rank de toute les solution
def ranking(score):
    # on récupère la list des dominance et on la trie
    dominance_list = dominance(score)
    dominance_list_sorted = {
        k: v for k, v in sorted(dominance_list.items(), key=lambda l: len(l[1]))
    }
    print(dominance_list_sorted)  # les solution avec le mins de dominance au début
    rank = {}

    for k in dominance_list_sorted.keys():  # pour chaque solution
        if (
            len(dominance_list[k]) == 0
        ):  # on attribue le rank 1 au solution sans dominance
            rank[k] = 1
        else:
            r = compute_rank(
                rank, dominance_list[k]
            )  # on calcule le rank des autres solutions = rank max de leur dominance +1
            rank[k] = r
    print(rank)
    return rank
