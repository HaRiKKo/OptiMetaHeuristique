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

starter = create_start_population()

# score = evaluate_population(starter)

# ranking(score)

print(starter[0], "\n", compute_disponibilite(starter[0]))
