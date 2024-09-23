import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import fsolve


class OptimalRotor:
    def __init__(self, fluid_properties: dict, operative_state: dict, hydrofoils: dict):
        self.density = fluid_properties['density']
        self.kinematic_viscosity = fluid_properties['kinematic_viscosity']
        self.dynamic_viscosity = fluid_properties['dynamic_viscosity']
        self.optimal_speed = operative_state['optimal_speed']
        self.tip_speed_ratio = operative_state['tip_speed_ratio']
        self.blade_radius = operative_state['blade_radius']
        self.omega_speed = self.tip_speed_ratio * self.optimal_speed / self.blade_radius
        self.no_blades = operative_state['no_blades']
        self.radius_hub_pctg = operative_state['radius_hub_pctg']
        self.initial_point_pctg = operative_state['initial_point_pctg']
        self.final_point_pctg = operative_state['final_point_pctg']
        self.no_design_points = operative_state['no_design_points']
        self.hydrofoils_data = hydrofoils
        self.optimal_chord = []
        self.optimal_twist = []
        self.design_points = []

    def get_design_points(self):
        """
        Function to compute the optimal polars for the ocean current turbine blade design.
        The optimal polars are computed by fitting the hydrofoil data with a polynomial function.
        """
        # Defining initial and final points for the design.
        initial_point = self.initial_point_pctg * self.blade_radius
        final_point = self.final_point_pctg * self.blade_radius
        number_points = self.no_design_points

        # Defining the design points along the blade (in terms of local radius).
        design_points = np.linspace(initial_point, final_point, number_points)

        # Check if the number of design points match with the number of hydrofoils data.
        if len(design_points) == len(self.hydrofoils_data):
            self.design_points = design_points
            print("The number of design points match with the number of hydrofoils data. (\u2713)")
        else:
            print("The number of design points does not match with the number of hydrofoils data. Please check the data.")
        return None

    def get_optimal_chord_twist(self, path):
        """
        Function to compute the optimal chord and twist angle for the ocean current turbine blade design.
        The optimal chord and twist angle are computed using the Blade Element Momentum Theory (BEMT).
        :param path: str, path to the folder where polar plots will be saved.
        """
        # Define the design points (in terms of local radius) and the hydrofoils considered for the analysis.
        # By default, the hydrofoils are considered to be in the same order as the design points.
        # TODO: Create a function to reorder the relation between the hydrofoils and the design points.
        design_points = self.design_points
        design_points[-1] = design_points[-1] * 0.975
        design_hydrofoils = list(self.hydrofoils_data.keys())

        # Defining lists where the optimal chord and twist angle will be stored.
        chords = []
        twists = []

        # Initialize the iterative process to compute the optimal chord and twist angle.
        for i in range(len(design_hydrofoils)):
            # Extracting the polar data for the selected hydrofoil.
            hydrofoil = design_hydrofoils[i]
            local_radius = design_points[i]
            alpha = self.hydrofoils_data[hydrofoil]['alpha']
            cl = self.hydrofoils_data[hydrofoil]['cl']
            cd = self.hydrofoils_data[hydrofoil]['cd']
            hydro_eff = [cl[j] / cd[j] for j in range(len(cl))]

            # Fitting the hydrofoil data with a polynomial function.
            coeff_hydro_eff = np.polyfit(alpha, hydro_eff, deg=7)
            coeff_cl = np.polyfit(alpha, cl, deg=7)
            coeff_cd = np.polyfit(alpha, cd, deg=7)

            # Compute extended polars for the hydrofoil data.
            alpha_extended = np.linspace(min(alpha), max(alpha), num=100)
            hydro_eff_extended = np.polyval(coeff_hydro_eff, alpha_extended)
            cl_extended = np.polyval(coeff_cl, alpha_extended)
            cd_extended = np.polyval(coeff_cd, alpha_extended)

            # Get the index of the maximum efficiency point.
            max_hydro_eff_index = np.argmax(hydro_eff_extended)
            optimal_alpha = alpha_extended[max_hydro_eff_index]
            optimal_cl = cl_extended[max_hydro_eff_index]
            optimal_cd = cd_extended[max_hydro_eff_index]

            # Plot the Hydrodynamic Efficiency of the Hydrofoils.
            plt.figure(figsize=(10, 6))
            plt.plot(alpha, hydro_eff, 'o', label='Hydrofoil Data')
            plt.plot(alpha_extended, hydro_eff_extended, label='Polynomial Fit', color='teal')
            plt.plot(optimal_alpha, np.max(hydro_eff_extended), 'ro', label='Optimal Point')
            plt.xlabel("Angle of Attack [deg]")
            plt.ylabel("Hydrodynamic Efficiency [-]")
            plt.title(f"Hydrodynamic Efficiency of Hydrofoil {hydrofoil}")
            plt.legend()
            plt.minorticks_on()
            plt.grid(which='major', linestyle='-', linewidth='0.5', color='grey', alpha=0.25)
            plt.grid(which='minor', linestyle=':', linewidth='0.5', color='grey', alpha=0.30)
            plt.savefig(f"{path}/hydrofoil_{hydrofoil}_efficiency.png", dpi=300)

            # Initialize the chord and axial and tangential induction factors.
            chord = 0.01 * self.blade_radius
            beta = 0.0
            a = 0.0
            b = 0.0
            # Initialize the iterative process to compute the optimal chord and twist angle.
            while a < 0.333:
                # Initialize the axial and tangential induction errors.
                error_ind_axial = 0.10
                error_ind_tangential = 0.10
                while error_ind_axial > 0.001 or error_ind_tangential > 0.001:
                    # Reallocate the geometrical and hydrodynamic variables.
                    # TODO: Figure out how to avoid the reallocation of the geometrical and hydrodynamic variables.
                    U_inf = self.optimal_speed
                    Radius = self.blade_radius
                    radius_hub = self.radius_hub_pctg * Radius
                    radius = local_radius
                    Nb = self.no_blades
                    TipSR = self.tip_speed_ratio
                    Omega = U_inf * TipSR / Radius

                    # Compute the relative velocities.
                    U_disk = U_inf * (1 - a)
                    U_tang = Omega * radius * (1 + b)

                    # Compute the flow angles at the local radius.
                    phi = np.rad2deg(np.arctan(U_disk / U_tang))
                    alpha = optimal_alpha
                    beta = phi - alpha
                    phi_radians = np.deg2rad(phi)

                    # Compute the axial and tangential force factors.
                    coeff_lift = optimal_cl
                    coeff_drag = optimal_cd
                    C_x = coeff_lift * np.cos(phi_radians) + coeff_drag * np.sin(phi_radians)
                    C_y = coeff_lift * np.sin(phi_radians) - coeff_drag * np.cos(phi_radians)

                    # Compute the local blade solidity.
                    sigma_r = Nb * chord / (2 * np.pi * radius)

                    # Compute the tip and root losses.
                    F_tip = (2 / np.pi) * np.arccos(np.exp(-(((Nb / 2) * (1 - (radius / Radius))) / ((radius / Radius) * (np.sin(phi_radians))))))
                    F_root = (2 / np.pi) * np.arccos(np.exp(-((Nb / 2) * ((radius - radius_hub) / (radius * np.sin(phi_radians))))))
                    F_total = F_tip * F_root

                    # Compute the axial and tangential induction factors.
                    # TODO: Try to define the functions as global functions.
                    def fa(variable_a: float):
                        return variable_a / (1 - variable_a) - (sigma_r * C_x) / (4 * F_total * (np.sin(phi_radians)) ** 2)

                    def fb(variable_b: float):
                        return variable_b / (1 + variable_b) - (sigma_r * C_y) / (4 * F_total * np.sin(phi_radians) * np.cos(phi_radians))

                    # Compute the axial and tangential induction factors.
                    a_new = fsolve(fa, a)
                    b_new = fsolve(fb, b)

                    # Compute the axial and tangential induction errors.
                    error_ind_axial = abs(float(a_new) - a)
                    error_ind_tangential = abs(float(b_new) - b)

                    # Update the axial and tangential induction factors.
                    a = a_new
                    b = b_new
                chord = chord + 0.00001
            chords.append(chord)
            twists.append(beta)
        self.optimal_chord = chords
        self.optimal_twist = twists
        return None
