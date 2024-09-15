import os
import yaml
import numpy as np
from airfoilprep import Polar
from airfoilprep import Airfoil


def create_objects(files: str, path: str):
    """
    Function to create the polars hydrofoil, polar and airfoil objects.
    The objects are created directly from the AirfoilPrepPy library.
    :param path: absolute path to the hydrofoil data.
    :param files: list of hydrofoil data files names.
    :return: dictionary of hydrofoil, polars, and airfoils objects.
    """
    # Save the information of the hydrofoil data files into a dictionary.
    hydrofoils = {}
    for file in files:
        with open(os.path.join(path, file), 'r') as stream:
            data = yaml.safe_load(stream)
            hydrofoils[data['hydrofoil']] = data

    # Create the polars objects from the hydrofoil data files.
    polars = {}
    for hydrofoil, data in hydrofoils.items():
        polars[hydrofoil] = Polar(Re=data['reynolds'], alpha=data['alpha'], cl=data['cl'], cd=data['cd'], cm=data['cm'])

    # Create the airfoils objects from the polars objects.
    hydrofoils_names = list(hydrofoils.keys())
    airfoils = {}
    for i, hydrofoil in enumerate(hydrofoils_names):
        airfoils[hydrofoil] = Airfoil([polars[hydrofoil]])

    return hydrofoils, polars, airfoils


def extrapolate_airfoil_data(airfoils: dict):
    """
    Function to extrapolate the airfoil data by using the AirfoilPrepPy library.
    :param airfoils:
    :return:
    """
    airfoils_extrapolated = {}
    for airfoil, properties in airfoils.items():
        cd_list = airfoils[airfoil].polars[0].cd
        cd_min = np.min(cd_list)
        aspect_ratio = 10
        cd_max = 1.11 + 0.018 * aspect_ratio
        airfoil_extrapolated = airfoils[airfoil].extrapolate(AR=aspect_ratio, cdmax=cd_max, cdmin=cd_min)
        airfoils_extrapolated[airfoil] = airfoil_extrapolated
    return airfoils_extrapolated
