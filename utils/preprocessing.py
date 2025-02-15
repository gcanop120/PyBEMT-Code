import os
import yaml


def hydrofoils_data_check(path: str):
    """
    Function for checking the availability of the hydrofoil data files.
    Function reports if the folder exists or not, and the number of files found.
    In addition, reports if the files have the correct extension and data structure.

    :param path: str, path to the folder containing the hydrofoil data files.
    :return: files: list, list of the files found in the folder.
    """
    if os.path.exists(path):
        # Check  if the path exists and print the number of files found.
        print(f"Folder {path} exists. The path is correct. (\u2713)")
        files = os.listdir(path)
        print(f"Number of files found: {len(files)} (i.e. design points).")
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


def fluid_properties_data_check(path: str):
    """
    Function for checking the availability of the fluid properties data files.
    Function reports if the folder exists or not, and if the data structure is correct.
    :param path: str, path to the folder containing the fluid properties data files.
    """
    # Check if the path exists.
    if os.path.exists(path):
        print(f"File {path} exists. The path is correct. (\u2713)")
        if path.endswith(".yml"):
            print(f"File {path} has the correct extension. (\u2713)")
            keys = ['density', 'kinematic_viscosity', 'dynamic_viscosity', 'salinity', 'temperature']
            with open(path, 'r') as f:
                data = yaml.safe_load(f)
                if all(key in data.keys() for key in keys):
                    print(f"File {path} has the correct data structure. (\u2713)")
                else:
                    print(f"File {path} does not have the correct data structure. Please check the file. (x)")
                    return None
        else:
            print(f"File {path} does not have the correct extension. Please check the file. (x)")
            return None
    else:
        print(f"File {path} does not exist. Please check the path. (x)")
        return None
    return data


def operative_state_data_check(path: str):
    """
    Function for checking the availability of the operative state data files.
    Function reports if the folder exists or not, and if the data structure is correct.
    :param path: str, path to the folder containing the operative state data files.
    """
    # Check if the path exists.
    if os.path.exists(path):
        print(f"File {path} exists. The path is correct. (\u2713)")
        if path.endswith(".yml"):
            print(f"File {path} has the correct extension. (\u2713)")
            keys = ['optimal_speed', 'tip_speed_ratio', 'angular_speed', 'rpm', 'blade_radius', 'no_blades',
                    'radius_hub_pctg', 'initial_point_pctg', 'final_point_pctg', 'no_design_points', 'operative_reynolds']
            with open(path, 'r') as f:
                data = yaml.safe_load(f)
                if all(key in data.keys() for key in keys):
                    print(f"File {path} has the correct data structure. (\u2713)")
                else:
                    print(f"File {path} does not have the correct data structure. Please check the file. (x)")
                    return None
        else:
            print(f"File {path} does not have the correct extension. Please check the file. (x)")
            return None
    else:
        print(f"File {path} does not exist. Please check the path. (x)")
        return None
    return data


def hydrofoils_data_rearrange(files: list, path: str):
    """
    Function for rearranging the hydrofoil data files into a single dictionary data structure.
    :param files: list, list of the files found in the folder.
    :param path: str, path to the folder containing the hydrofoil data files.
    :return: hydrofoil_data: dict, dictionary containing the hydrofoil data.
    """
    hydrofoils = {}
    for file in files:
        with open(f"{path}/{file}", 'r') as f:
            data = yaml.safe_load(f)
            hydrofoil = data['hydrofoil']
            hydrofoils[hydrofoil] = data
    return hydrofoils


def hydrofoils_ext_data_rearrange(hydrofoils_ext: dict):
    """
    Function for rearranging the extrapolated hydrofoil data files into a single dictionary data structure.
    :param hydrofoils_ext: dict, dictionary containing the extrapolated hydrofoil data as Hydrofoil objects.
    :return: hydrofoil_data: dict, dictionary containing the hydrofoil data.
    """
    hydrofoils_names = list(hydrofoils_ext.keys())
    hydrofoils_extended = {}
    for i in range(len(hydrofoils_names)):
        alpha = hydrofoils_ext[hydrofoils_names[i]].polars[0].alpha
        cl = hydrofoils_ext[hydrofoils_names[i]].polars[0].cl
        cd = hydrofoils_ext[hydrofoils_names[i]].polars[0].cd
        cm = hydrofoils_ext[hydrofoils_names[i]].polars[0].cm
        reynolds = hydrofoils_ext[hydrofoils_names[i]].polars[0].Re
        hydrofoils_extended[hydrofoils_names[i]] = {'alpha': alpha, 'cl': cl, 'cd': cd, 'cm': cm, 'reynolds': reynolds}
    return hydrofoils_extended
