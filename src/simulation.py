from config.defaults import DEFAULT_TIMESTEP

class Simulation:
    def __init__(self, satellite, orbit, duration_orbits=10, timestep=DEFAULT_TIMESTEP):
        self.satellite = satellite
        self.orbit = orbit
        self.timestep = timestep
        self.duration = duration_orbits
        self.initial_temperature = 293.0       # K, roughly 20 degree Celsius
    