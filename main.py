# ==================================================================================================================================
# PYTHON IMPLEMENTATION OF THE BEMT METHOD FOR THE DESIGN AND EVALUATION OF AN OCEAN CURRENT TURBINE // IITCA-UAEMex // 2024B // GCP
# ==================================================================================================================================

# Part 1. Airfoil Data Extrapolation by using the AirfoilPrep library to extrapolate the airfoil data.
# The library is developed by S.A Ning NREL and is available at: https://github.com/WISDEM/AirfoilPreppy.git

# Required Libraries
from utils.preprocessing import hydrofoils_data_check
from utils.preprocessing import hydrofoils_keys_check

# ======================================== PART 1: HYDROFOIL DATA CHECK ============================================================
HYDROFOILS_FOLDER_NAME = "hydrofoils"  # Folder name where the hydrofoil data is stored.
[absolute_path, files] = hydrofoils_data_check(path=HYDROFOILS_FOLDER_NAME)  # Check if the hydrofoil data is correctly stored.
hydrofoils_keys_check(files=files, path=absolute_path)  # Check if the hydrofoil data files contain the correct keys.

# ======================================== PART 2: AIRFOIL DATA EXTRAPOLATION ======================================================

