from config.defaults import SOLAR_CONSTANT, STEFAN_BOLTZMANN

class Satellite:

    def __init__(self, mass, area, absorptivity, emissivity, specific_heat):
        self.mass = mass                          # kg
        self.area = area                          # m^2
        self.absorptivity = absorptivity          # 0 to 1
        self.emissivity = emissivity              # 0 to 1
        self.specific_heat = specific_heat        # J/kg.K
    