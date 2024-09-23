# ====================================================================================================================================================
# PYTHON IMPLEMENTATION OF THE BEMT METHOD FOR THE OPTIMAL DESIGN AND EVALUATION OF AN OCEAN CURRENT TURBINE // IITCA-UAEMex // 2024B // Gerardo Cano.
# ====================================================================================================================================================

# Required Libraries
from utils.preprocessing import hydrofoils_data_check
from utils.preprocessing import hydrofoils_data_rearrange
from utils.preprocessing import fluid_properties_data_check
from utils.preprocessing import operative_state_data_check
from utils.optimal_bemt import OptimalRotor

# SECTION 1. Defining the paths of the required data files.
HYDROFOIL_FOLDER_PATH = "hydrofoils"
FLUID_PROPERTIES_FILE_PATH = "turbine/fluid_properties.yml"
OPERATIVE_STATE_FILE_PATH = "turbine/operative_state.yml"
POLAR_PLOTS_FOLDER_PATH = "resources/polar plots"

# SECTION 2. Check if the hydrofoil data, fluid properties data, and operative state data
# are available and have the correct data structure required for the analysis.
files_hydrofoils = hydrofoils_data_check(path=HYDROFOIL_FOLDER_PATH)
file_hydrofoils = hydrofoils_data_rearrange(files=files_hydrofoils, path=HYDROFOIL_FOLDER_PATH)
file_fluid_properties = fluid_properties_data_check(path=FLUID_PROPERTIES_FILE_PATH)
file_operative_state = operative_state_data_check(path=OPERATIVE_STATE_FILE_PATH)

# SECTION 3. Compute the optimal chord and twist angle for the ocean current turbine.
# The optimal chord and twist angle are computed using the Blade Element Momentum Theory (BEMT).
optimal_rotor = OptimalRotor(fluid_properties=file_fluid_properties, operative_state=file_operative_state, hydrofoils=file_hydrofoils)
optimal_rotor.get_design_points()
optimal_rotor.get_optimal_chord_twist(path=POLAR_PLOTS_FOLDER_PATH)
