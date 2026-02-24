import pytest
import math
from src.orbit import Orbit

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def iss_orbit():
    """Orbit instance at ISS altitude (408 km) with default inclination."""
    return Orbit(altitude_km=408)

@pytest.fixture
def high_orbit():
    """Orbit instance at 2000 km for high-LEO comparison tests."""
    return Orbit(altitude_km=2000)

# ---------------------------------------------------------------------------
# calculate_orbital_period
# ---------------------------------------------------------------------------

def test_orbital_period_iss_known_value(iss_orbit):
    """ISS orbital period should be approximately 92.6 minutes (5556 seconds).
    Reference value taken from publicly documented ISS orbital parameters.
    Tolerance of 10 seconds accounts for the simplified circular orbit assumption."""
    assert abs(iss_orbit.calculate_orbital_period() - 5556) < 10

def test_orbital_period_very_low_altitude():
    """A 200 km orbit should give a period of approximately 88 minutes (5280 seconds).
    This is near the lower bound of practical LEO. Wider tolerance of 60 seconds
    used since the reference is a rough approximation."""
    orbit = Orbit(altitude_km=200)
    assert abs(orbit.calculate_orbital_period() - 5280) < 60

def test_orbital_period_geostationary():
    """GEO at 35786 km should give approximately 86164 seconds (one sidereal day).
    Note: the reference is the sidereal day (~86164s), not the solar day (~86400s),
    because GEO is defined by matching Earth's sidereal rotation rate."""
    geo = Orbit(altitude_km=35786)
    assert abs(geo.calculate_orbital_period() - 86164) < 60

def test_orbital_period_higher_altitude_longer(iss_orbit, high_orbit):
    """Higher altitude should produce a longer orbital period.
    Validates Kepler's third law: T² ∝ r³, so period increases with orbital radius."""
    assert high_orbit.calculate_orbital_period() > iss_orbit.calculate_orbital_period()

def test_orbital_period_unaffected_by_inclination():
    """Orbital period should be identical regardless of inclination.
    The current model uses only altitude in the period calculation — inclination
    is stored but intentionally ignored. This test locks in that contract so any
    future change that accidentally wires inclination into the period is caught."""
    o2 = Orbit(altitude_km=408, inclination_deg=90)
    assert o1.calculate_orbital_period() == o2.calculate_orbital_period()