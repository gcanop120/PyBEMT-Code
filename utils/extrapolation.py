import numpy as np
from airfoilprep import Polar
from airfoilprep import Hydrofoil


def create_objects(hydrofoils: dict):
    """
    Function for creating the Polar and Hydrofoil objects from the hydrofoil data.
    :param hydrofoils: dict, dictionary containing the hydrofoil data.
    :return: polars and hydrofoil_objects.
    """
    # Create the Polar objects.
    polars_obj = {}
    for hydrofoil, data in hydrofoils.items():
        polars_obj[hydrofoil] = Polar(Re=data['reynolds'], alpha=data['alpha'], cl=data['cl'], cd=data['cd'], cm=data['cm'])
    # Create the Hydrofoil objects.
    hydrofoils_names = list(hydrofoils.keys())
    hydrofoils_obj = {}
    for i, hydrofoils in enumerate(hydrofoils_names):
        hydrofoils_obj[hydrofoils] = Hydrofoil([polars_obj[hydrofoils]])
    return polars_obj, hydrofoils_obj


def extrapolate_hydrofoil_data(hydrofoils: dict):
    """
    Function for extrapolating the hydrofoil data to the entire rotor
    blade configurations alpha angles. By default -180 to 180 degrees.
    :param hydrofoils: dict, dictionary containing the hydrofoil data.
    """
    hydrofoils_extrapolated = {}
    for hydrofoil, properties in hydrofoils.items():
        cd_list = hydrofoils[hydrofoil].polars[0].cd
        cd_min = np.min(cd_list)
        aspect_ratio = 10
        cd_max = 1.11 + 0.018 * aspect_ratio
        hydrofoil_extrapolated = hydrofoils[hydrofoil].extrapolate(AR=aspect_ratio, cdmax=cd_max, cdmin=cd_min)
        hydrofoils_extrapolated[hydrofoil] = hydrofoil_extrapolated
    return hydrofoils_extrapolated


def save_aerodyn_files(hydrofoils_extra: dict, path: str):
    """
    Function for saving the aerodynamic data files of the hydrofoils.
    :param hydrofoils_extra: dict, dictionary containing the extrapolated hydrofoil data.
    :param path: str, path to the folder where the aerodynamic data files will be saved.
    """
    for hydrofoil in hydrofoils_extra.keys():
        hydrofoils_extra[hydrofoil].writeToAerodynFile(f"{path}/{hydrofoil}.dat")
        print(f"File {hydrofoil}.dat saved successfully. (\u2713)")