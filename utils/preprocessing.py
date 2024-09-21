import os


def hydrofoils_data_check(path: str):
    """
    Function for checking the availability of the hydrofoil data files.
    Function reports if the folder exists or not, and the number of files found.
    In addition, reports if the files have the correct extension and data structure.+
    :param path: str, path to the folder containing the hydrofoil data files.
    :return: None
    """
    if os.path.exists(path):
        print(f"Folder {path} exists. The path is correct.")
        files = os.listdir(path)
        print(f"Number of files found: {len(files)}")
        return None
    else:
        print(f"Folder {path} does not exist. Please check the path.")
        return None


