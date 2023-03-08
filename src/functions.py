import random
import math

from src.compute_objectives import *

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
    # print("population",population)
    score = {}
    for i in range(len(population)):
        cout = compute_cout(population[i])[0]
        makespan = compute_makespan(population[i])[0]
        dispo = compute_disponibilite(population[i])[0]
        score[i] = [cout, makespan, dispo]
    # print("score",score)
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
        dominante = list(
            score.keys()
        )  # initialisé la liste des solutions dominantes à toute les solutions
        for i in range(3):  # pour chaque objectif
            objectif_key = score[key][i]  # on récupère sa valeur

            for s in list(dominante):  # pour chaque solution dominante
                if (
                    objectif_key <= score[s][i]
                ):  # on regarde si l'objectif de la solution ciblé est inferieur à l'objectif de la solution dominante
                    dominante.remove(
                        s
                    )  # si oui alors on supprime la solution dominante de la liste

        dominance[key] = dominante
    # print("dominance",dominance)
    return dominance


# calcule du rank d'une solution à l'aide de sa liste de solution dominante
def compute_rank(rank, list):
    r_max = 2
    for e in list:
        if rank[e] >= r_max:
            r_max = rank[e] + 1
    return r_max


# calcule du rank de toute les solution
def ranking(score):
    # on récupère la list des dominance et on la trie
    dominance_list = dominance(score)
    dominance_list_sorted = {
        k: v for k, v in sorted(dominance_list.items(), key=lambda l: len(l[1]))
    }  # les solution avec le mions de dominance au début
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
    # print(rank)
    return rank


# calcule de la crowding distance
def crowding_distance(liste_solutions):
    objective_functions = [compute_makespan, compute_cout, compute_disponibilite]
    l = len(liste_solutions)
    # Initialisation des distances
    distance = {}
    for i in range(l):
        distance[i] = 0

    # Tri en fonction de chaque objectif
    for objectif in objective_functions:
        # Evaluation
        evaluated_pop = list(map(objectif, liste_solutions))
        # Sort
        sorted_pop = sorted(range(len(evaluated_pop)), key=lambda k: evaluated_pop[k])
        # Infini pour les valeurs extrêmes
        distance[sorted_pop[0]] = [math.inf]
        distance[sorted_pop[-1]] = [math.inf]
        for i in range(1, l - 1):
            distance[sorted_pop[i]] += (
                evaluated_pop[sorted_pop[i + 1]] - evaluated_pop[sorted_pop[i - 1]]
            )

    # arrondie les distances à 2 chiffres après la virgule
    res = dict()
    for key in distance:
        if distance[key] != math.inf:
            res[key] = round(distance[key][0], 2)
        else:
            res[key] = distance[key][0]
    # print("crowding distance", res)
    return res


# Selection des solutions avec un tournois binaires
def selection(liste_solutions, ranking):
    # On selectionne la moitié des solutions
    # Comparaison des solutions 2 par 2 (choisies au hasard) puis sélection de la meilleure
    distance_dict = crowding_distance(liste_solutions)
    id_solutions = [*range(len(liste_solutions))]
    random.shuffle(id_solutions)
    selected_solutions = []

    for i in range(0, len(liste_solutions) - 1, 2):
        index1 = id_solutions[i]
        index2 = id_solutions[i + 1]
        rank = ranking[index1] - ranking[index2]
        if rank == 0:  # si les deux solution on le même rang
            if distance_dict[index1] >= distance_dict[index2]:
                selected_solutions.append(liste_solutions[index1])
            else:
                selected_solutions.append(liste_solutions[index2])
        elif rank < 0:  # si le candidat 1 à un rang inférieur => on le selectionne
            selected_solutions.append(liste_solutions[index1])
        else:  # si le candidat 2 à un rang inférieur => on le selectionne
            selected_solutions.append(liste_solutions[index2])

    # print("solution selectionner", selected_solutions)
    return selected_solutions


def sort_dictionary(dict):
    nouveau_dict = {}
    for i in range(len(dict)):
        nouveau_dict[i] = dict[i]
    return nouveau_dict


def crossover(population):
    taille_pop = len(population)
    nouvelle_population = []
    for i in range(0, taille_pop - 1, 2):
        nouveau_candidat_1 = {}
        nouveau_candidat_2 = {}
        for key, value in population[i].items():
            if key <= nb_tache // 2:
                nouveau_candidat_1[key] = value
            else:
                nouveau_candidat_2[key] = value
        for key, value in population[i + 1].items():
            if key <= nb_tache // 2:
                nouveau_candidat_2[key] = value
            else:
                nouveau_candidat_1[key] = value
        nouvelle_population.append(sort_dictionary(nouveau_candidat_1))
        nouvelle_population.append(sort_dictionary(nouveau_candidat_2))
    return nouvelle_population


def mutation(population):
    nb_tache = len(population[0])
    taille_population = len(population)
    tache_mutee = random.randint(0, nb_tache - 1)
    # print("La tâche mutante est la numéro ", tache_mutee)
    for i in range(taille_population):
        population[i][tache_mutee] = random.randint(
            0, 2
        )  # VM choisie au hasard pour la tâche mutée
    return population


# Combine population before
def elitism_selection(n, population):
    rank = ranking(evaluate_population(population))
    selected_pop = []
    for key, value in rank.items():
        if len(selected_pop) < n:
            selected_pop.append(population[key])
        else:
            break
    return selected_pop
