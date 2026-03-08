import pytest
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

@pytest.fixture
def low_orbit():
    """Orbit instance at 200 km for low-LEO comparison tests."""
    return Orbit(altitude_km=200)

@pytest.fixture
def geo_orbit():
    """Orbit instance at GEO altitude (35786 km)."""
    return Orbit(altitude_km=35786)

# ---------------------------------------------------------------------------
# calculate_orbital_period
# ---------------------------------------------------------------------------

def test_orbital_period_iss_known_value(iss_orbit):
    """ISS orbital period should be approximately 92.6 minutes (5556 seconds).
    Reference value taken from publicly documented ISS orbital parameters.
    Tolerance of 10 seconds accounts for the simplified circular orbit assumption."""
    assert iss_orbit.calculate_orbital_period() == pytest.approx(5556, abs=10)

def test_orbital_period_very_low_altitude():
    """A 200 km orbit should give a period of approximately 88 minutes (5280 seconds).
    This is near the lower bound of practical LEO. Wider tolerance of 60 seconds
    used since the reference is a rough approximation."""
    orbit = Orbit(altitude_km=200)
    assert orbit.calculate_orbital_period() == pytest.approx(5280, abs=60)

def test_orbital_period_geostationary():
    """GEO at 35786 km should give approximately 86164 seconds (one sidereal day).
    Note: the reference is the sidereal day (~86164s), not the solar day (~86400s),
    because GEO is defined by matching Earth's sidereal rotation rate."""
    geo = Orbit(altitude_km=35786)
    assert geo.calculate_orbital_period() == pytest.approx(86164, abs=60)

def test_orbital_period_higher_altitude_longer(iss_orbit, high_orbit):
    """Higher altitude should produce a longer orbital period.
    Validates Kepler's third law: T² ∝ r³, so period increases with orbital radius."""
    assert high_orbit.calculate_orbital_period() > iss_orbit.calculate_orbital_period()

def test_orbital_period_unaffected_by_inclination():
    """Orbital period should be identical regardless of inclination.
    The current model uses only altitude in the period calculation — inclination
    is stored but intentionally ignored. This test locks in that contract so any
    future change that accidentally wires inclination into the period is caught."""
    o1 = Orbit(altitude_km=408, inclination_deg=0)
    o2 = Orbit(altitude_km=408, inclination_deg=90)
    assert o1.calculate_orbital_period() == o2.calculate_orbital_period()

# ---------------------------------------------------------------------------
# eclipse_fraction
# ---------------------------------------------------------------------------

def test_eclipse_fraction_iss_known_value(iss_orbit):
    """At ISS altitude and beta = 0, eclipse fraction should be approximately 0.39."""
    assert iss_orbit.calculate_eclipse_fraction() == pytest.approx(0.39, abs=0.01)

def test_eclipse_fraction_between_zero_and_one_iss(iss_orbit):
    """Eclipse fraction should always be between 0 and 1."""
    assert 0 < iss_orbit.calculate_eclipse_fraction() < 1

def test_eclipse_fraction_between_zero_and_one_high(high_orbit):
    """Eclipse fraction should always be between 0 and 1."""
    assert 0 < high_orbit.calculate_eclipse_fraction() < 1

def test_eclipse_fraction_between_zero_and_one_low(low_orbit):
    """Eclipse fraction should always be between 0 and 1."""
    assert 0 < low_orbit.calculate_eclipse_fraction() < 1

def test_eclipse_fraction_decreases_with_altitude(high_orbit, low_orbit):
    """Eclipse fraction should decrease as altitude increases."""
    assert high_orbit.calculate_eclipse_fraction() < low_orbit.calculate_eclipse_fraction()

def test_eclipse_fraction_geo(geo_orbit):
    """At GEO altitude and beta = 0, eclipse fraction should be approximately 0.05 (≈72 minutes per orbit)."""
    assert geo_orbit.calculate_eclipse_fraction() == pytest.approx(0.05, abs=0.02)

def test_eclipse_fraction_unaffected_by_inclination():
    """Eclipse fraction should be identical regardless of inclination.
    The current model uses only altitude in the eclipse fraction calculation — inclination
    is stored but intentionally ignored. This test locks in that contract so any
    future change that accidentally wires inclination into the eclipse fraction is caught."""
    o1 = Orbit(altitude_km=408, inclination_deg=0)
    o2 = Orbit(altitude_km=408, inclination_deg=90)
    assert o1.calculate_eclipse_fraction() == o2.calculate_eclipse_fraction()

# ---------------------------------------------------------------------------
# sunlight_duration
# ---------------------------------------------------------------------------

def test_sunlight_duration_iss_known_value(iss_orbit):
    """At ISS altitude, sunlight duration should be approximately 56-57 minutes (3390 seconds)."""
    assert iss_orbit.calculate_sunlight_duration() == pytest.approx(3394, abs=60)

def test_sunlight_plus_eclipse_equals_orbital_period(iss_orbit):
    """Sunlight duration + eclipse duration must equal the orbital period."""
    sunlight_duration = iss_orbit.calculate_sunlight_duration()
    eclipse_duration = iss_orbit.calculate_eclipse_fraction() * iss_orbit.calculate_orbital_period()
    orbital_period = iss_orbit.calculate_orbital_period()

    assert sunlight_duration + eclipse_duration == pytest.approx(orbital_period, rel=1e-3)

def test_sunlight_duration_increases_with_altitude(high_orbit, low_orbit):
    """Higher altitude should result in longer sunlight duration."""
    assert high_orbit.calculate_sunlight_duration() > low_orbit.calculate_sunlight_duration()

def test_sunlight_duration_positive(iss_orbit):
    """Sunlight duration must always be positive."""
    assert iss_orbit.calculate_sunlight_duration() > 0

def test_sunlight_duration_less_than_orbital_period(iss_orbit):
    """Sunlight duration cannot exceed the orbital period."""
    assert iss_orbit.calculate_sunlight_duration() < iss_orbit.calculate_orbital_period()

def test_sunlight_duration_geo(geo_orbit):
    """At GEO altitude, sunlight duration should be about 95% of the orbit (81800 seconds)."""
    assert geo_orbit.calculate_sunlight_duration() == pytest.approx(81800, abs=1000)

def test_sunlight_duration_unaffected_by_inclination():
    """Sunlight duration should not depend on inclination in this model."""
    o1 = Orbit(altitude_km=408, inclination_deg=0)
    o2 = Orbit(altitude_km=408, inclination_deg=90)

    assert o1.calculate_sunlight_duration() == o2.calculate_sunlight_duration()

def test_orbit_lighting_identity(iss_orbit):
    """Sunlight fraction + eclipse fraction must equal 1."""
    sunlight_fraction = iss_orbit.calculate_sunlight_duration() / iss_orbit.calculate_orbital_period()
    eclipse_fraction = iss_orbit.calculate_eclipse_fraction()

    assert sunlight_fraction + eclipse_fraction == pytest.approx(1.0, rel=1e-6)

# ---------------------------------------------------------------------------
# eclipse_duration
# ---------------------------------------------------------------------------

def test_eclipse_duration_iss_known_value(iss_orbit):
    """At ISS altitude, eclipse duration should be approximately 36 minutes (2160 seconds)"""
    assert iss_orbit.calculate_eclipse_duration() == pytest.approx(2160, abs=60)

def test_eclipse_duration_positive(iss_orbit):
    """Eclipse duration must always be positive."""
    assert iss_orbit.calculate_eclipse_duration() > 0

def test_eclipse_duration_less_than_orbital_period(iss_orbit):
    """Eclipse duration cannot exceed the orbital period."""
    assert iss_orbit.calculate_eclipse_duration() < iss_orbit.calculate_orbital_period()

def test_eclipse_duration_geo(geo_orbit):
    """At GEO altitude, eclipse duration should be about 5% of the orbit (4300 seconds)."""
    assert geo_orbit.calculate_eclipse_duration() == pytest.approx(4300, abs=500)

def test_eclipse_duration_unaffected_by_inclination():
    """Eclipse duration should not depend on inclination in this model."""
    o1 = Orbit(altitude_km=408, inclination_deg=0)
    o2 = Orbit(altitude_km=408, inclination_deg=90)

    assert o1.calculate_eclipse_duration() == o2.calculate_eclipse_duration()

def test_eclipse_duration_plus_sunlight_duration_equals_orbital_period_iss(iss_orbit):
    """Eclipse duration + sunlight duration must equal the orbital period."""
    eclipse_duration = iss_orbit.calculate_eclipse_duration()
    sunlight_duration = iss_orbit.calculate_sunlight_duration()
    orbital_period = iss_orbit.calculate_orbital_period()

    assert eclipse_duration + sunlight_duration == pytest.approx(orbital_period, rel=1e-3)

def test_eclipse_duration_plus_sunlight_duration_equals_orbital_period_high(high_orbit):
    """Eclipse duration + sunlight duration must equal the orbital period."""
    eclipse_duration = high_orbit.calculate_eclipse_duration()
    sunlight_duration = high_orbit.calculate_sunlight_duration()
    orbital_period = high_orbit.calculate_orbital_period()

    assert eclipse_duration + sunlight_duration == pytest.approx(orbital_period, rel=1e-3)

def test_eclipse_duration_decreases_with_altitude(low_orbit, high_orbit):
    """Higher altitude should result in shorter eclipse duration."""
    assert high_orbit.calculate_eclipse_duration() < low_orbit.calculate_eclipse_duration()

def test_eclipse_duration_matches_fraction_formula(iss_orbit):
    """Eclipse duration should equal eclipse_fraction × orbital_period."""
    expected = (
        iss_orbit.calculate_eclipse_fraction()
        * iss_orbit.calculate_orbital_period()
    )

    assert iss_orbit.calculate_eclipse_duration() == pytest.approx(expected)

def test_eclipse_fraction_consistency(iss_orbit):
    """Eclipse duration divided by orbital period should equal eclipse fraction."""
    eclipse_fraction = iss_orbit.calculate_eclipse_fraction()
    eclipse_duration = iss_orbit.calculate_eclipse_duration()
    orbital_period = iss_orbit.calculate_orbital_period()

    assert eclipse_duration / orbital_period == pytest.approx(eclipse_fraction)

def test_eclipse_duration_reasonable_fraction(iss_orbit):
    """Eclipse duration should be less than half an orbit for LEO."""
    assert iss_orbit.calculate_eclipse_duration() < 0.5 * iss_orbit.calculate_orbital_period()

def test_eclipse_duration_extreme_altitude():
    """At extremely high altitude eclipse duration should approach zero."""
    orbit = Orbit(altitude_km=1_000_000)

    assert orbit.calculate_eclipse_duration() < 0.01 * orbit.calculate_orbital_period()

def test_eclipse_fraction_plus_sunlight_fraction_equals_one(iss_orbit):
    """Eclipse fraction + sunlight fraction must equal 1."""
    eclipse_fraction = iss_orbit.calculate_eclipse_fraction()
    sunlight_fraction = iss_orbit.calculate_sunlight_duration() / iss_orbit.calculate_orbital_period()

    assert eclipse_fraction + sunlight_fraction == pytest.approx(1.0)

def test_eclipse_duration_surface_orbit():
    """At Earth's surface, eclipse duration should be half the orbital period."""
    orbit = Orbit(altitude_km=0)

    eclipse_duration = orbit.calculate_eclipse_duration()
    orbital_period = orbit.calculate_orbital_period()

    assert eclipse_duration == pytest.approx(0.5 * orbital_period, rel=1e-3)

def test_eclipse_duration_near_surface():
    """Near-surface orbit should have eclipse fraction close to 0.5."""
    orbit = Orbit(altitude_km=1)

    eclipse_fraction = orbit.calculate_eclipse_fraction()

    assert eclipse_fraction == pytest.approx(0.5, abs=0.01)