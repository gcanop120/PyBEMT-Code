import os
import yaml


def hydrofoils_data_check(path: str):
    """
    Function to check the correct disposition of the hydrofoil data in the specified path.
    :param path: relative path to the hydrofoil data.
    :return: list of hydrofoil data files names.
    """
    # Complete the relative path to turn it into an absolute path
    disk = os.path.splitdrive(os.getcwd())[0]
    main_folder = "\\PyBEMT Code"
    path = os.path.join(disk, os.path.join(main_folder, path))

    # Check if the path exists and message the user if it does or not
    if os.path.exists(path):
        print(f"Path: {path} exists.")
        files = os.listdir(path)
        print(f"Number of Hydrofoils Data Files Found: {len(files)}")
        print(f"Hydrofoils Data Files: {files}")
        hydrofoils = files
        return path, hydrofoils
    else:
        print(f"Path: {path} does not exist.")
        print("Please check the path and try again.")


def hydrofoils_keys_check(files: str, path: str):
    """
    Function to check the keys of the hydrofoil data files and print the status of the data.
    By default, the hydrofoil polar data should be in YAML format and contain the following keys:
    - alpha: list of angles of attack in degrees.
    - cl: list of lift coefficients (non-dimensional).
    - cd: list of drag coefficients (non-dimensional).
    - efficiency: list of hydrodynamic efficiency values.
    - hydrofoil: name of the hydrofoil.
    - reynolds: operative reynolds number.
    - source: source of the hydrofoil data (ANSYS or XFOIL).
    :return: status of the hydrofoil data.
    """

    # List of keys that the hydrofoil data should contain.
    keys = ['alpha', 'cl', 'cd', 'efficiency', 'hydrofoil', 'reynolds', 'source']

    # Check the keys of the hydrofoil data files and print the status of the data.
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
    return None
