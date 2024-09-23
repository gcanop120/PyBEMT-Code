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
        self.design_points = operative_state['no_design_points']
        # Define operative state properties.
        self.optimal_speed = operative_state['optimal_speed']
        self.tip_speed_ratio = tip_speed_ratio
        self.omega = self.optimal_speed * self.tip_speed_ratio / self.blade_radius
        # Define polar data of the hydrofoils.
        self.hydrofoils = hydrofoils

    def evaluate_bemt(self):
        """
        Function to evaluate the StandardRotor object using the Blade Element Momentum Theory (BEMT).
        The iterative process is computed just for one specific Tip Speed Ratio (TSR).
        """
