import os
import yaml


def hydrofoils_data_check(path: str):
    """
    Function to check the correct disposition of the hydrofoil data in the specified path.
    :param path: relative path to the hydrofoil data.
    :return: list of hydrofoil data files names.
    """
    # Complete the relative path and transform it into an absolute path.
    disk = os.path.splitdrive(os.getcwd())[0]
    main_folder = "\\PyBEMT Code"
    path = os.path.join(disk, os.path.join(main_folder, path))

    # Check if the hydrofoil data files are correctly stored.
    if os.path.exists(path):
        print(f"Path: {path} exists.")
        files = os.listdir(path)
        print(f"Number of Hydrofoils Data Files Found: {len(files)}")
        print(f"Hydrofoils Data Files: {files}")

        # Check if the hydrofoil data files have the correct keys.
        keys = ['alpha', 'cl', 'cd', 'cm', 'efficiency', 'hydrofoil', 'reynolds', 'source']
        for file in files:
            with open(os.path.join(path, file), 'r') as stream:
                try:
                    data = yaml.safe_load(stream)
                    if all(key in data for key in keys):
                        print(f"Hydrofoil Data File: {file} is Correct.")
                    else:
                        print(f"Hydrofoil Data File: {file} is Incorrect.")
                except yaml.YAMLError as exc:
                    print("YAML Loading Error:", exc)
        return path, files
    else:
        print(f"Path: {path} does not exist.")
        print("Please check the path and try again.")
        return None, None
