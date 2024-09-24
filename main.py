# ====================================================================================================================================================
# PYTHON IMPLEMENTATION OF THE BEMT METHOD FOR THE OPTIMAL DESIGN AND EVALUATION OF AN OCEAN CURRENT TURBINE // IITCA-UAEMex // 2024B // Gerardo C.
# ====================================================================================================================================================

# Required Libraries
from utils.preprocessing import hydrofoils_data_check
from utils.preprocessing import hydrofoils_data_rearrange
from utils.preprocessing import fluid_properties_data_check
from utils.preprocessing import operative_state_data_check
from utils.optimal_bemt import OptimalRotor
from utils.extrapolation import create_objects
from utils.extrapolation import extrapolate_hydrofoil_data
from utils.extrapolation import save_aerodyn_files
from utils.preprocessing import hydrofoils_ext_data_rearrange
from utils.evaluation_bemt import StandardRotor

# SECTION 1. Defining the paths of the required data files.
HYDROFOIL_FOLDER_PATH = "hydrofoils"
HYDROFOIL_EXT_FOLDER_PATH = "hydrofoils_ext"
FLUID_PROPERTIES_FILE_PATH = "turbine/fluid_properties.yml"
OPERATIVE_STATE_FILE_PATH = "turbine/operative_state.yml"
POLAR_PLOTS_FOLDER_PATH = "resources/polar plots"
OPTIMAL_ROTOR_FOLDER_PATH = "resources/optimal_rotor"

# SECTION 2. Check if the hydrofoil data, fluid properties data, and operative state data
# are available and have the correct data structure required for the analysis.
files_hydrofoils = hydrofoils_data_check(path=HYDROFOIL_FOLDER_PATH)                                # Check the hydrofoil data.
file_hydrofoils = hydrofoils_data_rearrange(files=files_hydrofoils, path=HYDROFOIL_FOLDER_PATH)     # Rearrange the hydrofoil data.
file_fluid_properties = fluid_properties_data_check(path=FLUID_PROPERTIES_FILE_PATH)                # Check the fluid property data.
file_operative_state = operative_state_data_check(path=OPERATIVE_STATE_FILE_PATH)                   # Check the operative state data.

# SECTION 3. Compute the optimal chord and twist angle for the ocean current turbine.
# The optimal chord and twist angle are computed using the Blade Element Momentum Theory (BEMT).
optimal_rotor = OptimalRotor(fluid_properties=file_fluid_properties,                # Create the OptimalRotor object.
                             operative_state=file_operative_state,                  # OptimalRotor object requires the fluid properties
                             hydrofoils=file_hydrofoils)                            # and operative state data to be defined.
optimal_rotor.get_design_points()                                                   # Define the design points.
optimal_rotor.get_optimal_chord_twist(path=POLAR_PLOTS_FOLDER_PATH)                 # Compute the optimal chord and twist.
optimal_rotor.save_properties(path=OPTIMAL_ROTOR_FOLDER_PATH)                       # Save the optimal rotor properties.

# SECTION 4. Once the optimal chord and twist angle are computed, it is required to extrapolate
# the hydrofoil data to the entire rotor blade possible configurations. This is done by using the
# AirfoilPrep library developed by the NREL. Available at: https://github.com/WISDEM/AirfoilPreppy.git
[polar_obj, hydrofoils_obj] = create_objects(hydrofoils=file_hydrofoils)                # Create the Polar and Hydrofoil objects.
hydrofoils_obj_extrapolated = extrapolate_hydrofoil_data(hydrofoils=hydrofoils_obj)     # Extrapolate the hydrofoil data.
save_aerodyn_files(hydrofoils_extra=hydrofoils_obj_extrapolated, path=HYDROFOIL_EXT_FOLDER_PATH)  # Save the aerodynamic data files.

# SECTION 5. The hydrofoil extrapolated data is now ready to be used for the BEMT analysis.
# The hydrofoil extrapolated data is rearranged into a single dictionary data structure for the analysis.
files_hydrofoils_extrapolated = hydrofoils_ext_data_rearrange(hydrofoils_ext=hydrofoils_obj_extrapolated)

# SECTION 6. The BEMT analysis is performed using the StandardRotor object.
standard_rotor = StandardRotor(fluid_properties=file_fluid_properties,
                               operative_state=file_operative_state,
                               hydrofoils=files_hydrofoils_extrapolated,
                               blade_chord=optimal_rotor.optimal_chord,
                               blade_twist=optimal_rotor.optimal_betas,
                               tip_speed_ratio=5)
AoA = standard_rotor.evaluate_bemt()
