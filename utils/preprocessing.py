import os
import yaml


def hydrofoils_data_check(path: str):
    """
    Function for checking the availability of the hydrofoil data files.
    Function reports if the folder exists or not, and the number of files found.
    In addition, reports if the files have the correct extension and data structure.+
    :param path: str, path to the folder containing the hydrofoil data files.
    :return: None
    """
    if os.path.exists(path):
        # Check  if the path exists and print the number of files found.
        print(f"Folder {path} exists. The path is correct. (\u2713)")
        files = os.listdir(path)
        print(f"Number of files found: {len(files)}")
        # Check if the files have the correct extension.
        for file in files:
            if file.endswith(".yml"):
                print(f"File {file} has the correct extension. (\u2713)")
                # Check if the files have the correct data structure.
                keys = ['alpha', 'cl', 'cd', 'cm', 'efficiency', 'hydrofoil', 'reynolds', 'source']
                with open(f"{path}/{file}", 'r') as f:
                    data = yaml.safe_load(f)
                    if all(key in data.keys() for key in keys):
                        print(f"File {file} has the correct data structure. (\u2713)")
                    else:
                        print(f"File {file} does not have the correct data structure. Please check the file. (x)")
                        return None
            else:
                print(f"File {file} does not have the correct extension. Please check the file. (x)")
                return None
    else:
        print(f"Folder {path} does not exist. Please check the path. (x)")
        return None
    return files
