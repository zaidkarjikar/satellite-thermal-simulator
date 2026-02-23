from config.defaults import EARTH_RADIUS, EARTH_MU

class Orbit:

    def __init__(self, altitude_km, inclination_deg=51.6):
        self.altitude_km = altitude_km
        self.inclination_deg = inclination_deg
        self.radius = (EARTH_RADIUS + altitude_km) * 1000      # convert to meters
    