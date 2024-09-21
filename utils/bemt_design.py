import numpy as np
from scipy.optimize import fsolve


def optimal_chord_twist(hydrofoils: dict, fluid_properties: dict, operative_state: dict):
    """
    Function to compute the optimal chord and twist for the blade based on the hydrofoil data and BEMT method.
    :param hydrofoils: dictionary of hydrofoil data.
    :param fluid_properties: dictionary of fluid properties.
    :param operative_state: dictionary of operative state.
    :return:
    """
    # Defining the list of design points along the blade (based on the local radius).
    initial_point = operative_state['initial_stage_pctg'] * operative_state['blade_radius']
    final_point = operative_state['blade_radius']
    number_points = operative_state['no_design_stations']

    design_points = np.linspace(initial_point, final_point, number_points)
    design_hydrofoils = list(hydrofoils.keys())
    chords = []

    for i in range(4, 5):
        # Extracting the hydrofoil data.
        hydrofoil = design_hydrofoils[i]  # Hydrofoil name.
        local_radius = design_points[i]  # Local radius.
        alpha = hydrofoils[hydrofoil]['alpha']  # Angle of attack.
        cl = hydrofoils[hydrofoil]['cl']  # Lift coefficient.
        cd = hydrofoils[hydrofoil]['cd']  # Drag coefficient.
        hydro_eff = [cl[i] / cd[i] for i in range(len(cl))]  # Hydrodynamic efficiency.

        # Fitting a Curve to the Hydrofoil Data.
        coefficients_cl = np.polyfit(alpha, cl, deg=7)  # Polynomial fit to the lift coefficient.
        coefficients_cd = np.polyfit(alpha, cd, deg=7)  # Polynomial fit to the drag coefficient.

        # Create a Curve for the Hydrodynamic Coefficients.
        alpha_curve = np.linspace(min(alpha), max(alpha), num=100)  # Angle of attack curve.
        cl_curve = np.polyval(coefficients_cl, alpha_curve)  # Lift coefficient curve.
        cd_curve = np.polyval(coefficients_cd, alpha_curve)  # Drag coefficient curve.
        hydro_eff_curve = [cl_curve[i] / cd_curve[i] for i in range(len(cl_curve))]  # Hydrodynamic efficiency curve.

        # Get the Index of the Maximum Efficiency and the Alpha, Cl, Cd Values Associated.
        max_hydro_eff_index = np.argmax(hydro_eff_curve)  # Index of the maximum hydrodynamic efficiency.
        optimal_alpha = alpha_curve[max_hydro_eff_index]  # Optimal angle of attack.
        optimal_cl = cl_curve[max_hydro_eff_index]  # Optimal lift coefficient.
        optimal_cd = cd_curve[max_hydro_eff_index]  # Optimal drag coefficient.

        # Compute the Optimal Chord and Twist.

        # Setting the Initial Guess for the Blade Chord.
        chord = 0.01  # Initial guess must be greater than zero for a better convergence.
        a = 0  # Initializing the axial induction factor.
        b = 0  # Initializing the tangential induction factor.
        error_ind_axial = 0.1  # Error percentage for the axial induction factor.
        error_ind_tangential = 0.1  # Error percentage for the tangential induction factor.

        # Iterative_process to compute the optimal chord and twist.
        while a < 0.333:
            a = 0  # Reset the axial induction factor.
            b = 0  # Reset the tangential induction factor.
            error_ind_axial = 0.1  # Reset the error percentage for the axial induction factor.
            error_ind_tangential = 0.1  # Reset the error percentage for the tangential induction factor.
            while error_ind_axial > 0.001 or error_ind_tangential > 0.001:
                # Define Blade Geometry and Hydrodynamic Parameters.
                U_inf = operative_state['optimal_speed']
                Radius = operative_state['blade_radius']
                radius_hub = operative_state['radius_hub']
                radius = local_radius
                Nb = operative_state['no_blades']
                rho = fluid_properties['density']
                TipSR = operative_state['tip_speed_ratio']
                Omega = U_inf * TipSR / Radius

                # Compute the Relative Velocities at the Local Radius.
                U_disk = U_inf * (1 - a)  # Axial velocity at the disk.
                U_tang = Omega * radius * (1 + b)  # Tangential velocity at the disk.

                # Compute the Flow Angles at the Local Radius.
                phi = np.rad2deg(np.arctan(U_disk / U_tang))  # Inflow angle.
                alpha = optimal_alpha  # Optimal angle of attack.
                beta = phi - alpha  # Twist angle.
                phi_radians = np.deg2rad(phi)  # Inflow angle in radians.
                alpha_radians = np.deg2rad(alpha)  # Optimal angle of attack in radians.
                beta_radians = np.deg2rad(beta)  # Twist angle in radians.

                # Compute the Axial and Tangential Force Coefficients.
                coeff_lift = optimal_cl  # Optimal lift coefficient.
                coeff_drag = optimal_cd  # Optimal drag coefficient.
                C_x = coeff_lift * np.cos(phi_radians) + coeff_drag * np.sin(phi_radians)  # Coefficient of Force in x-axis.
                C_y = coeff_lift * np.sin(phi_radians) - coeff_drag * np.cos(phi_radians)  # Coefficient of Force in y-axis.

                # Compute the Local Blade Solidity.
                sigma_r = Nb * chord / (2 * np.pi * radius)  # Local blade solidity.

                # Compute the Tip and Root Losses.
                F_tip = (2 / np.pi) * np.arccos(np.exp(-(((Nb / 2) * (1 - (radius / Radius))) / ((radius / Radius) * (np.sin(phi_radians))))))
                F_root = (2 / np.pi) * np.arccos(np.exp(-((Nb / 2) * ((radius - radius_hub) / (radius * np.sin(phi_radians))))))
                F_total = F_tip * F_root

                # Compute the Axial and Tangential Induction Factors.
                def fa(a):
                    return a / (1 - a) - (sigma_r * C_x) / (4 * F_total * (np.sin(phi_radians)) ** 2)

                def fb(b):
                    return b / (1 + b) - (sigma_r * C_y) / (4 * F_total * np.sin(phi_radians) * np.cos(phi_radians))

                a_new = fsolve(fa, a)
                b_new = fsolve(fb, b)

                # Compute the Error Percentage for the Axial and Tangential Induction Factors.
                error_ind_axial = abs(a_new - a)
                error_ind_tangential = abs(b_new - b)

                # Update the Axial and Tangential Induction Factors.
                a = a_new
                b = b_new
            chord = chord + 0.00001
        chords.append(chord)
    return chords
