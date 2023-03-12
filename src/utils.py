import os

import numpy as np
import pandas as pd

def read_files(input_path='./data/'):
    filenames = os.listdir(input_path)
    csv_filenames = list(filter(lambda f: f.endswith('.csv'), filenames))
    
    file_path = {}

    for filename in csv_filenames:
        file_path[filename] = os.path.join(input_path, filename)
    
    return (file_path)

# Read ressources
def read_resources(file_path):

    task_connectivity = pd.read_csv(file_path['Hybrid15_map.csv'], header=None)
    task_instructions = np.array(pd.read_csv(file_path['Hybrid15_comp.csv'], header=0))
    VM_caracteristique = np.array(pd.read_csv(file_path['Ressource_car.csv'], header=0))
    VM_cost = pd.read_csv(file_path['mapcost.csv'], header=None)
    
    return task_connectivity, task_instructions, VM_caracteristique, VM_cost