import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
np.random.seed(0)


def optimal_blade_chord_twist(hydrofoils: dict, fluid_properties: dict, operative_state: dict):
    """
    Function to compute the optimal chord and twist for the blade based on the
    hydrofoil data and BEMT method.
    :param hydrofoils: dictionary of hydrofoil data.
    :param fluid_properties: dictionary of fluid properties.
    :param operative_state: dictionary of operative state.
    :return:
    """
    # Defining initial and final points for the design stations
    initial_point = operative_state['initial_stage_pctg'] * operative_state['blade_radius']
    final_point = operative_state['blade_radius']
    number_points = operative_state['no_design_stations']

    # Defining the list of design points along the blade (based on the local radius).
    design_points = np.linspace(initial_point, final_point, number_points)
    design_points[-1] = design_points[-1] * 0.95
    design_hydrofoils = list(hydrofoils.keys())

    # Check if the number of design points matches the number of hydrofoils.
    if design_points.shape[0] != len(design_hydrofoils):
        print("The number of design points does not match the number of hydrofoils.")
        print("Please check the number of design points and try again.")
        return None

    # Defining a list where the optimal chord will be stored.
    chords = []
    betas = []

    for i in range(len(design_points)):
        # Extracting the hydrofoil data.
        hydrofoil = design_hydrofoils[i]
        local_radius = design_points[i]
        alpha = hydrofoils[hydrofoil]['alpha']
        cl = hydrofoils[hydrofoil]['cl']
        cd = hydrofoils[hydrofoil]['cd']
        hydro_eff = [cl[i] / cd[i] for i in range(len(cl))]

        # Fitting a Curve to the Hydrofoil Data.
        coeff_hydro_eff = np.polyfit(alpha, hydro_eff, deg=7)
        coeff_cl = np.polyfit(alpha, cl, deg=7)
        coeff_cd = np.polyfit(alpha, cd, deg=7)

        # Generate extended versions of the hydrofoil data.
        alpha_extended = np.linspace(min(alpha), max(alpha), num=100)
        hydro_eff_extended = np.polyval(coeff_hydro_eff, alpha_extended)
        cl_extended = np.polyval(coeff_cl, alpha_extended)
        cd_extended = np.polyval(coeff_cd, alpha_extended)

        # Get the index of the maximum efficiency and the alpha, cl, cd values associated.
        max_hydro_eff_index = np.argmax(hydro_eff_extended)
        optimal_alpha = alpha_extended[max_hydro_eff_index]
        optimal_cl = cl_extended[max_hydro_eff_index]
        optimal_cd = cd_extended[max_hydro_eff_index]

        # Initialize the chord and axial and tangential induction factors.
        chord = 0.005
        a = 0.0
        b = 0.0
        # Initializing the iterative process.
        while a < 0.333:
            error_ind_axial = 0.10
            error_ind_tangential = 0.10
            while error_ind_axial > 0.001 or error_ind_tangential > 0.001:
                # Get the geometrical and hydrodynamic parameters.
                U_inf = operative_state['optimal_speed']
                Radius = operative_state['blade_radius']
                radius_hub = operative_state['radius_hub']
                radius = local_radius
                Nb = operative_state['no_blades']
                rho = fluid_properties['density']
                TipSR = operative_state['tip_speed_ratio']
                Omega = U_inf * TipSR / Radius

                # Compute the relative velocities at the local radius.
                U_disk = U_inf * (1 - a)
                U_tang = Omega * radius * (1 + b)

                # Compute the flow angles at the local radius.
                phi = np.rad2deg(np.arctan(U_disk / U_tang))
                alpha = optimal_alpha
                beta = phi - alpha
                phi_radians = np.deg2rad(phi)
                alpha_radians = np.deg2rad(alpha)
                beta_radians = np.deg2rad(beta)

                # Compute the axial and tangential force factors.
                coeff_lift = optimal_cl
                coeff_drag = optimal_cd
                C_x = coeff_lift * np.cos(phi_radians) + coeff_drag * np.sin(phi_radians)
                C_y = coeff_lift * np.sin(phi_radians) - coeff_drag * np.cos(phi_radians)

                # Compute the local blade solidity.
                sigma_r = Nb * chord / (2 * np.pi * radius)

                # Compute the root and tip losses.
                F_tip = (2 / np.pi) * np.arccos(np.exp(-(((Nb / 2) * (1 - (radius / Radius))) / ((radius / Radius) * (np.sin(phi_radians))))))
                F_root = (2 / np.pi) * np.arccos(np.exp(-((Nb / 2) * ((radius - radius_hub) / (radius * np.sin(phi_radians))))))
                F_total = F_tip * F_root

                # Compute the axial and tangential induction factors.
                def fa(variable_a):
                    return variable_a / (1 - variable_a) - (sigma_r * C_x) / (4 * F_total * (np.sin(phi_radians)) ** 2)

                def fb(variable_b):
                    return variable_b / (1 + variable_b) - (sigma_r * C_y) / (4 * F_total * np.sin(phi_radians) * np.cos(phi_radians))

                # Compute the axial and tangential induction factors.
                a_new = fsolve(fa, a)
                b_new = fsolve(fb, b)

                # Compute the error percentage for the axial and tangential induction factors.
                error_ind_axial = abs(a_new - a)
                error_ind_tangential = abs(b_new - b)

                # Update the axial and tangential induction factors.
                a = a_new
                b = b_new
            chord = chord + 0.00001
        chords.append(chord)
        betas.append(beta)
    return chords, betas
