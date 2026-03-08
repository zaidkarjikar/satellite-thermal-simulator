import math
from config.defaults import EARTH_RADIUS, EARTH_MU

class Orbit:
    """Represents a circular Earth orbit defined by altitude and inclination.
    Provides orbital mechanics calculations based on the two-body problem.
    Inclination is stored but not used in calculations — the current model 
    assumes a simple circular orbit geometry."""
    
    def __init__(self, altitude_km, inclination_deg=51.6):
        """Initialise an orbit at the given altitude above Earth's surface.

        Args:
            altitude_km (float): Orbital altitude in kilometres above Earth's surface.
            inclination_deg (float): Orbital inclination in degrees. Defaults to 51.6
                (ISS inclination). Currently unused in calculations.
        """
        self.altitude_km = altitude_km
        self.inclination_deg = inclination_deg
        self.orbital_radius = (EARTH_RADIUS + altitude_km) * 1000      # convert to meters
    
    def calculate_orbital_period(self):
        """Calculate the orbital period for a circular orbit.

        Uses the standard two-body formula: T = 2π√(r³/μ), where r is the
        orbital radius in metres and μ is Earth's gravitational parameter.

        Returns:
            float: Orbital period in seconds.
        """
        orbital_period = 2 * math.pi * math.sqrt(self.orbital_radius**3 / EARTH_MU)
        return orbital_period
    
    def calculate_eclipse_fraction(self):
        """Calculate the fraction of the orbit time spent in Earth's shadow.
        
        Simple cylindrical shadow approximation assuming:
        - Circular orbit
        - beta angle = 0° (worst-case eclipse)
        - Sun at infinite distance

        Returns:
            float: Fraction of orbit time spent in shadow (0 to 1).
        """
        ratio = (EARTH_RADIUS * 1000) / self.orbital_radius
        ratio = max(-1.0, min(1.0, ratio))
        
        eclipse_fraction = (1 / math.pi) * math.asin(ratio)
        return eclipse_fraction
    