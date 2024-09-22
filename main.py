# ====================================================================================================================================================
# PYTHON IMPLEMENTATION OF THE BEMT METHOD FOR THE OPTIMAL DESIGN AND EVALUATION OF AN OCEAN CURRENT TURBINE // IITCA-UAEMex // 2024B // Gerardo Cano.
# ====================================================================================================================================================

# Required Libraries
from utils.preprocessing import hydrofoils_data_check
from utils.preprocessing import fluid_properties_data_check
from utils.preprocessing import operative_state_data_check

# Part 1. Import the required hydrofoil and turbine setup data.
HYDROFOIL_FOLDER_PATH = "hydrofoils"
FLUID_PROPERTIES_FILE_PATH = "turbine/fluid_properties.yml"
OPERATIVE_STATE_FILE_PATH = "turbine/operative_state.yml"

# Part 1.A Check if the hydrofoil data, fluid properties data, and operative state data
# are available and have the correct data structure required for the analysis.
files_hydrofoils = hydrofoils_data_check(path=HYDROFOIL_FOLDER_PATH)
file_fluid_properties = fluid_properties_data_check(path=FLUID_PROPERTIES_FILE_PATH)
file_operative_state = operative_state_data_check(path=OPERATIVE_STATE_FILE_PATH)