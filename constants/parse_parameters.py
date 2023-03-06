import os
import ruamel.yaml as yaml

paramaters = os.path.realpath('constants/params.yaml')

def parse_yaml():

    """
        Parse yaml file containing the parameters

        Input:
            -- no input
        
        Output:
            -- params: dict, contining all the parameters to be used
    """

    with open(paramaters) as file:
        params = yaml.load(file, Loader=yaml.Loader)
    
    return (params)

params = parse_yaml()

resource_path = params['resource_path']