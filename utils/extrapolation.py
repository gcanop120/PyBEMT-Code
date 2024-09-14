import os
import yaml
from airfoilprep import Polar
from airfoilprep import Airfoil


def create_polars(files: str, path: str):
    """
    Function to create the polars objects from the hydrofoil data files.
    The Polar objects are created using the AirfoilPrep library.
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
        polars[hydrofoil] = Polar(Re=data['reynolds'], alpha=data['alpha'], cl=data['cl'], cd=data['cd'], cm=None)

    # Create the airfoils objects from the polars objects.
    hydrofoils_names = list(hydrofoils.keys())
    airfoils = {}
    for i, hydrofoil in enumerate(hydrofoils_names):
        airfoils[hydrofoil] = Airfoil([polars[hydrofoil]])

    return hydrofoils, polars, airfoils
