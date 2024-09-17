import os
import yaml


def hydrofoils_data_check(folder_name: str):
    """
    Function to check the correct disposition of the hydrofoil data in the specified path.
    :param folder_name: relative path to the hydrofoil data.
    :return: list of hydrofoil data files names.
    """
    # Complete the relative path and transform it into an absolute path.
    disk = os.path.splitdrive(os.getcwd())[0]
    main_folder = "\\PyBEMT Code"
    folder_name = os.path.join(disk, os.path.join(main_folder, folder_name))

    # Check if the hydrofoil data files are correctly stored.
    if os.path.exists(folder_name):
        print(f"Path: {folder_name} exists.")
        files = os.listdir(folder_name)
        print(f"Number of Hydrofoils Data Files Found: {len(files)}")
        print(f"Hydrofoils Data Files: {files}")

        # Check if the hydrofoil data files have the correct keys.
        keys = ['alpha', 'cl', 'cd', 'cm', 'efficiency', 'hydrofoil', 'reynolds', 'source']
        for file in files:
            with open(os.path.join(folder_name, file), 'r') as stream:
                try:
                    data = yaml.safe_load(stream)
                    if all(key in data for key in keys):
                        print(f"Hydrofoil Data File: {file} is Correct.")
                    else:
                        print(f"Hydrofoil Data File: {file} is Incorrect.")
                except yaml.YAMLError as exc:
                    print("YAML Loading Error:", exc)
        return folder_name, files
    else:
        print(f"Path: {folder_name} does not exist.")
        print("Please check the path and try again.")
        return None, None


def fluid_properties_data_check(relative_path: str):
    """
    Function to check the correct disposition of the fluid properties file in the specified path.
    :param relative_path: Relative path to the fluid properties file.
    :return: fluid properties.
    """
    # Check if the fluid properties file is correctly stored given the relative path.
    if os.path.exists(relative_path):
        print(f"Path: {relative_path} exists.")
        with open(relative_path, 'r') as stream:
            data = yaml.safe_load(stream)
            keys = ['density', 'dynamic_viscosity', 'kinematic_viscosity', 'salinity', 'temperature']
            if all(key in data for key in keys):
                print(f"Fluid Properties File: {relative_path} is Correct.")
            else:
                print(f"Fluid Properties File: {relative_path} is Incorrect.")
        return data
    else:
        print(f"Path: {relative_path} does not exist.")
        print("Please check the path and try again.")
        return None


def operative_state_data_check(relative_path: str):
    """
    Function to check the correct disposition of the operative state file in the specified path.
    :param relative_path: Relative path to the operative state file.
    :return: operative state data.
    """
    # Check if the operative state file is correctly stored given the relative path.
    if os.path.exists(relative_path):
        print(f"Path: {relative_path} exists.")
        with open(relative_path, 'r') as stream:
            data = yaml.safe_load(stream)
            keys = ['angular_speed', 'blade_radius', 'chord_reference', 'operating_reynolds',
                    'optimal_speed', 'rpm', 'tip_speed_ratio', 'no_design_stations', 'initial_stage_pctg']
            if all(key in data for key in keys):
                print(f"Operative State File: {relative_path} is Correct.")
            else:
                print(f"Operative State File: {relative_path} is Incorrect.")
        return data
    else:
        print(f"Path: {relative_path} does not exist.")
        print("Please check the path and try again.")
        return None
