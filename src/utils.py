import os

def read_files(input_path='./resources/'):
    filenames = os.listdir(input_path)
    csv_filenames = list(filter(lambda f: f.endswith('.csv'), filenames))
    
    file_path = {}

    for filename in csv_filenames:
        file_path[filename] = os.path.join(input_path, filename)
    
    return (file_path)