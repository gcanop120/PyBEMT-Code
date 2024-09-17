# ======================================================================================================================================================
# PYTHON IMPLEMENTATION OF THE BEMT METHOD FOR THE DESIGN AND EVALUATION OF AN OCEAN CURRENT TURBINE // IITCA-UAEMex // 2024B // GCP
# ======================================================================================================================================================

# Part 1. Airfoil Data Extrapolation by using the AirfoilPrepPy library to extrapolate the airfoil data.
# The library is developed by S.A Ning NREL and is available at: https://github.com/WISDEM/AirfoilPreppy.git

# Required Libraries
from utils.preprocessing import hydrofoils_data_check
from utils.preprocessing import fluid_properties_data_check
from utils.preprocessing import operative_state_data_check
from utils.extrapolation import create_objects
from utils.extrapolation import extrapolate_airfoil_data
from utils.extrapolation import save_aerodyn_files
from utils.bemt_design import optimal_chord_twist

# ======================================== PART 1: HYDROFOIL DATA CHECK ================================================================================
HYDROFOILS_FOLDER_NAME = "hydrofoils"                           # Folder name where the hydrofoil data is stored.
PATH_FLUID_PROPERTIES = "turbine/fluid_properties.yml"          # Path to the fluid properties file.
PATH_OPERATIVE_STATE = "turbine/operative_state.yml"            # Path to the operative state file.

[absolute_path_hydrofoils, files] = hydrofoils_data_check(folder_name=HYDROFOILS_FOLDER_NAME)   # Check the hydrofoil data files.
fluid_properties = fluid_properties_data_check(relative_path=PATH_FLUID_PROPERTIES)             # Check the fluid properties file.
operative_state = operative_state_data_check(relative_path=PATH_OPERATIVE_STATE)                # Check the operative state file.

# ================================ PART 2: HYDROFOIL DATA CORRECTION AND EXTRAPOLATION =================================================================
[hydrofoils, polars_obj, airfoils_obj] = create_objects(files=files, path=absolute_path_hydrofoils)  # Create hydrofoils, polars and airfoils objects.

# ================================= PART 2A: BLADE CHORD AND TWIST DESIGN ==============================================================================
[optimal_chord, optimal_twist] = optimal_chord_twist(hydrofoils=hydrofoils)

# ================================= PART 2B: AIRFOIL DATA EXTRAPOLATION ================================================================================
hydrofoils_extrapolated = extrapolate_airfoil_data(airfoils=airfoils_obj)           # Extrapolate the hydrofoil data.
save_aerodyn_files(hydrofoils_extrapolated=hydrofoils_extrapolated)                 # Save the extrapolated hydrofoil data into a new file.


                                                