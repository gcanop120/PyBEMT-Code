# ====================================================================================================================================================
# PYTHON IMPLEMENTATION OF THE BEMT METHOD FOR THE OPTIMAL DESIGN AND EVALUATION OF AN OCEAN CURRENT TURBINE // IITCA-UAEMex // 2024B // Gerardo Cano.
# ====================================================================================================================================================

# Required Libraries
from utils.preprocessing import hydrofoils_data_check

# Part 1. Import the required hydrofoil and turbine setup data.
HYDROFOIL_FOLDER_PATH = "hydrofoils"
files = hydrofoils_data_check(path=HYDROFOIL_FOLDER_PATH)
