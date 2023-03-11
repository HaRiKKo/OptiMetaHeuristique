import os
import sys

import pandas as pd

from src.compute_objectives import *
from src.functions import *
from src.utils import *

import warnings

warnings.filterwarnings("ignore")

sys.path.insert(0, os.path.dirname(os.path.abspath("constants")))
from constants.parse_parameters import *

file_path = read_files(resource_path)
task_connectivity, task_instructions, VM_caracteristique, VM_cost = read_resources(
    file_path
)

### Algorithme NSGA II

CRITERE_ARRET = 100

# Initialisation de la population de départ
population_depart = create_start_population()
print("Population de départ : ", population_depart)
display_pop(population_depart)

print(
    "Evaluation de la population de départ :\n", evaluate_population(population_depart)
)

# Entrée dans la boucle
for i in range(CRITERE_ARRET):
    # print("\n____ Debut de la boucle ", i)
    # Evaluation de la population
    score = evaluate_population(population_depart)

    # Rang
    rank = ranking(score)
    # print("Rang de la population de départ : ", score)

    ### Child population - début
    selected_solution = selection(population_depart, rank)
    # print("Population sélectionnée : ", selected_solution)

    # Crossover
    crossed_population = crossover(selected_solution)

    # Mutation
    mutated_population = mutation(crossed_population)
    # print("Population enfant : ", mutated_population)

    ### Child population - fin

    # Combinaison des populations
    combined_population = population_depart + mutated_population

    selected_elite_population = elitism_selection(10, combined_population)
    # print("Elite population : ", selected_elite_population)

    # La population elite devient la nouvelle population de départ
    population_depart = selected_elite_population

print("\nPopulation finale : ", selected_elite_population)
display_pop(selected_elite_population)
print(
    "Evaluation de la population finale :\n",
    evaluate_population(selected_elite_population),
)
