import numpy as np
from tqdm import tqdm
from scipy.interpolate import make_interp_spline
from scipy.optimize import fsolve
import scipy.integrate as integrate


class StandardRotor:
    """
    Class for creating a rotor object with standard properties.The StandardRotor object is
    used for the BEMT analysis, then it is required to provide the geometrical parameters
    (i.e. chord and twist) and the fluid properties and operative state data.
    """

    def __init__(self, fluid_properties: dict, operative_state: dict, hydrofoils: dict,
                 blade_chord: list, blade_twist: list, tip_speed_ratio: float):
        """
        Constructor of the StandardRotor class.
        :param fluid_properties: dict, dictionary containing the fluid properties.
        :param operative_state: dict, dictionary containing the operative state data.
        :param hydrofoils: dict, dictionary containing the hydrofoil data.
        :param blade_chord: list, list containing the chord values of the rotor blade.
        :param blade_twist: list, list containing the twist values of the rotor blade.
        """
        # Define the fluid properties.
        self.density = fluid_properties['density']
        self.kinematic_viscosity = fluid_properties['kinematic_viscosity']
        self.dynamic_viscosity = fluid_properties['dynamic_viscosity']
        # Define geometrical properties.
        self.blade_radius = operative_state['blade_radius']
        self.no_blades = operative_state['no_blades']
        self.radius_hub_pctg = operative_state['radius_hub_pctg']
        self.initial_point_pctg = operative_state['initial_point_pctg']
        self.final_point_pctg = operative_state['final_point_pctg']
        self.blade_chord = blade_chord
        self.blade_twist = blade_twist
        self.no_design_points = operative_state['no_design_points']
        self.mu_design_points = np.linspace(self.initial_point_pctg, self.final_point_pctg, self.no_design_points)
        self.radial_design_points = self.mu_design_points * self.blade_radius
        self.radial_design_points[-1] = self.radial_design_points[-1] * 0.975
        # Define operative state properties.
        self.optimal_speed = operative_state['optimal_speed']
        self.tip_speed_ratio = tip_speed_ratio
        self.omega = self.optimal_speed * self.tip_speed_ratio / self.blade_radius
        # Define polar data of the hydrofoils.
        self.hydrofoils = hydrofoils
        self.W_velocities = []
        self.AoA = []
        self.induction_axial = []
        self.induction_tangential = []
        self.total_losses = []
        self.coefficient_x = []
        self.coefficient_y = []
        self.phi_angle = []
        self.total_power = []
        self.total_thrust = []

    def evaluate_bemt(self):
        """
        Function to evaluate the StandardRotor object using the Blade Element Momentum Theory (BEMT).
        The iterative process is computed just for one specific Tip Speed Ratio (TSR).
        """
        name_hydrofoil = list(self.hydrofoils.keys())
        # Invert name_hydrofoil list.
        name_hydrofoil = name_hydrofoil[::-1]
        AoA = []
        W_velocity = []
        induction_axial = []
        induction_tangential = []
        total_losses = []
        cx_coefficient = []
        cy_coefficient = []
        phi_angle = []
        for i in tqdm(range(len(name_hydrofoil))):
            # Basic Hydrofoil Data Information (local radius, alpha, cl, cd).
            hydrofoil_data = self.hydrofoils[name_hydrofoil[i]]
            local_radius = self.radial_design_points[i]
            alphas = hydrofoil_data['alpha']
            cl = hydrofoil_data['cl']
            cd = hydrofoil_data['cd']
            # Initialize the variables for the BEMT analysis.
            a = 0.0
            b = 0.0
            # Initialize the iterative process for the convergence of the BEMT analysis.
            error_ind_axial = 0.10
            error_ind_tangential = 0.10
            while error_ind_axial > 0.001 or error_ind_tangential > 0.001:
                # Reallocate the geometrical and hydrodynamic properties.
                U_inf = self.optimal_speed
                Radius = self.blade_radius
                radius_hub = self.radius_hub_pctg * Radius
                radius = local_radius
                Nb = self.no_blades
                TipSR = self.tip_speed_ratio
                Omega = self.omega
                TipSr = Omega * radius / U_inf

                # Compute the relative velocities.
                U_disk = U_inf * (1 - a)
                U_tang = Omega * radius * (1 + b)

                # Compute the inflow angles.
                phi = np.rad2deg(np.arctan(U_disk / U_tang))
                phi_radians = np.deg2rad(phi)
                beta = self.blade_twist[i]
                alpha = phi - self.blade_twist[i]

                # Compute the blade solidity at local radius.
                sigma_r = Nb * self.blade_chord[i] / (2 * np.pi * radius)

                # Calculating the polar coefficient at the i-th radial position.
                coeff_lift = np.interp(alpha, alphas, cl)
                coeff_drag = np.interp(alpha, alphas, cd)
                C_x = coeff_lift * np.cos(phi_radians) + coeff_drag * np.sin(phi_radians)
                C_y = coeff_lift * np.sin(phi_radians) - coeff_drag * np.cos(phi_radians)

                cl_i2 = make_interp_spline(alphas, cl)(alpha)
                cd_i2 = make_interp_spline(alphas, cd)(alpha)
                hydro_eff2 = cl_i2 / cd_i2

                # Compute tip and root losses.
                F_tip = (2 / np.pi) * np.arccos(np.exp(-(((Nb / 2) * (1 - (radius / Radius))) / ((radius / Radius) * (np.sin(phi_radians))))))
                F_root = (2 / np.pi) * np.arccos(np.exp(-((Nb / 2) * ((radius - radius_hub) / (radius * np.sin(phi_radians))))))
                F_total = F_tip * F_root

                # Compute axial and tangential induction factors.
                def fa(variable_a: float):
                    return variable_a / (1 - variable_a) - (sigma_r * C_x) / (4 * F_total * (np.sin(phi_radians)) ** 2)

                def fb(variable_b: float):
                    return variable_b / (1 + variable_b) - (sigma_r * C_y) / (4 * F_total * np.sin(phi_radians) * np.cos(phi_radians))

                # Compute the new axial and tangential induction factors.
                a_new = fsolve(fa, a)
                b_new = fsolve(fb, b)

                error_ind_axial = abs(a_new - a)
                error_ind_tangential = abs(b_new - b)

                a = a_new
                b = b_new

                W = np.sqrt((U_disk * (1 - a)) ** 2 + (U_tang * (1 + b)) ** 2)
            AoA.append(alpha)
            W_velocity.append(W)
            induction_axial.append(a)
            induction_tangential.append(b)
            total_losses.append(F_total)
            cx_coefficient.append(C_x)
            cy_coefficient.append(C_y)
            phi_angle.append(phi)
            self.W_velocities = W_velocity
            self.W_velocities = [item for sublist in self.W_velocities for item in sublist]
            self.AoA = AoA
            self.AoA = [item for sublist in self.AoA for item in sublist]
            self.induction_axial = induction_axial
            self.induction_axial = [item for sublist in self.induction_axial for item in sublist]
            self.induction_tangential = induction_tangential
            self.induction_tangential = [item for sublist in self.induction_tangential for item in sublist]
            self.total_losses = total_losses
            self.total_losses = [item for sublist in self.total_losses for item in sublist]
            self.coefficient_x = cx_coefficient
            self.coefficient_x = [item for sublist in self.coefficient_x for item in sublist]
            self.coefficient_y = cy_coefficient
            self.coefficient_y = [item for sublist in self.coefficient_y for item in sublist]
            self.phi_angle = phi_angle
            self.phi_angle = [item for sublist in self.phi_angle for item in sublist]
        return

    def evaluate_performance(self, interpolation_range: int = 70):
        """
        Function to evaluate the performance of the StandardRotor object.
        :param interpolation_range: int, number of points to interpolate the performance data.
        """
        # Compute interpolated variables.
        segmented_radius = np.linspace(self.initial_point_pctg * self.blade_radius, self.blade_radius, interpolation_range + 1)
        blades_loads_a = np.interp(segmented_radius, self.radial_design_points, self.induction_axial)
        blades_loads_b = np.interp(segmented_radius, self.radial_design_points, self.induction_tangential)
        blades_loads_f_total = np.interp(segmented_radius, self.radial_design_points, self.total_losses)
        blades_loads_w = np.interp(segmented_radius, self.radial_design_points, self.W_velocities)
        blades_loads_cx = np.interp(segmented_radius, self.radial_design_points, self.coefficient_x)
        blades_loads_cy = np.interp(segmented_radius, self.radial_design_points, self.coefficient_y)
        blades_loads_chord = np.interp(segmented_radius, self.radial_design_points, self.blade_chord)
        blades_loads_phi = np.interp(segmented_radius, self.radial_design_points, self.phi_angle)
        blade_loads_thrust = []
        blade_loads_power = []
        for i in range(len(segmented_radius) - 1):
            lower_bound = segmented_radius[i]
            upper_bound = segmented_radius[i + 1]
            thrust = integrate.quad(
                lambda r: 4 * np.pi * r * self.density * self.optimal_speed ** 2 * blades_loads_a[i] * (1 - blades_loads_a[i]) * blades_loads_f_total[
                    i],
                lower_bound.astype(float), upper_bound.astype(float))
            blade_loads_thrust.append(thrust[0])
            power = integrate.quad(
                lambda r: 4 * np.pi * r ** 3 * self.density * self.optimal_speed * self.omega * blades_loads_b[i] * (1 - blades_loads_a[i]) *
                          blades_loads_f_total[i],
                lower_bound.astype(float), upper_bound.astype(float))
            blade_loads_power.append(power[0])
        # Sum all elements of the list in blade_loads_thrust.
        total_thrust = sum(blade_loads_thrust)
        total_power = sum(blade_loads_power)
        self.total_thrust = total_thrust
        self.total_power = total_power
        return total_thrust, total_power
