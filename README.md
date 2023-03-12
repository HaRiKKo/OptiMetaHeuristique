# Multi-Objective Optimization : Workflow scheduling

## Description

Worflow scheduling using Multi-Objective Optimization (MOO) with a Pareto approach : NSGA-II and PSO (optional)

**Credits:**
* Ruben Aloukou (<aloukourub@cy-tech.fr>)
* Célia Benmessaouda (<benmessao@cy-tech.fr>)
* Chléo Chevrier (<chevrierch@cy-tech.fr>)
* Thomas Fiou (<fiouthomas@cy-tech.fr>)


**Pre-requisites:**
* Python version >=3.8.10 
* Pip version >= 20.0.2

## Project worktree

* **constants:**
    * params.yaml contains all constant variables we need to run the project
    * parse_parameters.py parses all constant variables from yaml file in order to use them

* **doc:**
    * modelization.pdf summarizes the notations and technicals choices we made for modelling the project
    * report.pdf (coming soon)


* **src:**
    * compute_objectives.py contains all functions for evaluating the objectives functions
    * functions.py contains all functions required for genetic algorithms to work (in particular NSGA-II)
    * utils.py contains functions for conding more conviently and respecting devops rules

## Installation

1. Clone the following repository: 

`git clone https://github.com/HaRiKKo/OptiMetaHeuristique.git`

2. Create a virtual Python environment with the command below in your terminal, please replace venv_name_project with you own name project: 

`python3 -m venv venv_name_project`

3. Activate your environement by executing this command: 

`. venv_name_project/bin/activate`

4. Please be sure pip module is already installed on your device and install all dependencies with: 

`pip install -r requirements.txt`

Notices:
- You can desactivate the environmnent by doing this in your terminal: `deactivate`
- You have to install the dependencies in your project directory.
- We recommand you to name your venv : venv_workflow_scheduling

## How to run

To run the project, you have to configure the parameter file that you can find in the constants folder :

* **resource_path** : the string with the location where the required resources for the project are stored

After having configured the parameter file and activated the virtual environment, you can run the projet by using this command :

`python main.py`