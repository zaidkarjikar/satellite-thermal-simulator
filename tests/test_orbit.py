import pytest
import math
from src.orbit import Orbit
from config.defaults import EARTH_RADIUS
from hypothesis import given, strategies as st

# -------------------------------------------------------------------
# Constants used in tests
# -------------------------------------------------------------------

ISS_ALTITUDE = 408
LOW_LEO_ALTITUDE = 200
HIGH_LEO_ALTITUDE = 2000
GEO_ALTITUDE = 35786

# --------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------

@pytest.fixture
def iss_orbit():
    """Orbit instance at ISS altitude."""
    return Orbit(altitude_km=ISS_ALTITUDE)

@pytest.fixture
def low_leo_orbit():
    """Orbit instance at low LEO altitude."""
    return Orbit(altitude_km=LOW_LEO_ALTITUDE)

@pytest.fixture
def high_leo_orbit():
    """Orbit instance at high LEO altitude."""
    return Orbit(altitude_km=HIGH_LEO_ALTITUDE)

@pytest.fixture
def geo_orbit():
    """Orbit instance at GEO altitude."""
    return Orbit(altitude_km=GEO_ALTITUDE)

# ---------------------------------------------------------------------
# Orbit Geometry
# ---------------------------------------------------------------------

def test_orbital_radius_calculation():
    """Orbital radius should equal Earth radius plus altitude."""
    orbit = Orbit(altitude_km=ISS_ALTITUDE)

    expected = (EARTH_RADIUS + ISS_ALTITUDE) * 1000

    assert orbit.orbital_radius == pytest.approx(expected)

def test_orbital_radius_increases_with_altitude():
    """Orbital radius should increase as altitude increases."""
    low = Orbit(altitude_km=LOW_LEO_ALTITUDE)
    high = Orbit(altitude_km=HIGH_LEO_ALTITUDE)

    assert high.orbital_radius > low.orbital_radius

# ---------------------------------------------------------------------
# Orbital Period
# ---------------------------------------------------------------------

@pytest.mark.parametrize(
    "altitude, expected_period, tolerance",
    [
        (LOW_LEO_ALTITUDE, 5280, 60),
        (ISS_ALTITUDE, 5556, 10),
        (HIGH_LEO_ALTITUDE, 7620, 60),
        (GEO_ALTITUDE, 86164, 60)
    ]
)
def test_orbital_period_reference_values(altitude, expected_period, tolerance):
    """Orbital period for different altitudes should match known reference values."""
    orbit = Orbit(altitude_km=altitude)

    assert orbit.calculate_orbital_period() == pytest.approx(expected_period, abs=tolerance)

@pytest.mark.parametrize(
    "lower_altitude, higher_altitude",
    [
        (LOW_LEO_ALTITUDE, ISS_ALTITUDE),
        (ISS_ALTITUDE, HIGH_LEO_ALTITUDE),
        (HIGH_LEO_ALTITUDE, GEO_ALTITUDE)
    ]
)
def test_orbital_period_increases_with_altitude(lower_altitude, higher_altitude):
    """Orbital period must increase with orbital altitude (Kepler's third law)."""
    lower_orbit = Orbit(altitude_km=lower_altitude)
    higher_orbit = Orbit(altitude_km=higher_altitude)

    assert higher_orbit.calculate_orbital_period() > lower_orbit.calculate_orbital_period()

@pytest.mark.parametrize(
    "inclination",
    [0, 45, 90]
)
def test_orbital_period_unaffected_by_inclination(inclination):
    """Orbital period should depend only on altitude in this simplified model."""
    o1 = Orbit(altitude_km=ISS_ALTITUDE, inclination_deg=0)
    o2 = Orbit(altitude_km=ISS_ALTITUDE, inclination_deg=inclination)

    assert o1.calculate_orbital_period() == o2.calculate_orbital_period()

# ---------------------------------------------------------------------
# Eclipse Fraction
# ---------------------------------------------------------------------

def test_eclipse_fraction_iss_reference(iss_orbit):
    """ISS eclipse fraction should be approximately 0.39 for beta = 0°."""
    assert iss_orbit.calculate_eclipse_fraction() == pytest.approx(0.39, abs=0.01)

@pytest.mark.parametrize(
    "altitude",
    [LOW_LEO_ALTITUDE, ISS_ALTITUDE, HIGH_LEO_ALTITUDE, GEO_ALTITUDE]
)
def test_eclipse_fraction_between_zero_and_one(altitude):
    """Eclipse fraction must always be between 0 and 1."""
    orbit = Orbit(altitude_km=altitude)
    
    eclipse_fraction = orbit.calculate_eclipse_fraction()

    assert 0 < eclipse_fraction < 1

@pytest.mark.parametrize(
    "lower_altitude, higher_altitude",
    [
        (LOW_LEO_ALTITUDE, ISS_ALTITUDE),
        (ISS_ALTITUDE, HIGH_LEO_ALTITUDE),
        (HIGH_LEO_ALTITUDE, GEO_ALTITUDE)
    ]
)
def test_eclipse_fraction_decreases_with_altitude(lower_altitude, higher_altitude):
    """Eclipse fraction should decrease as orbital altitude increases."""
    low_orbit = Orbit(altitude_km=lower_altitude)
    high_orbit = Orbit(altitude_km=higher_altitude)

    assert high_orbit.calculate_eclipse_fraction() < low_orbit.calculate_eclipse_fraction()

def test_eclipse_fraction_geo_reference(geo_orbit):
    """GEO eclipse fraction should be about 5% of the orbit (~72 minutes)."""
    assert geo_orbit.calculate_eclipse_fraction() == pytest.approx(0.05, abs=0.02)

@pytest.mark.parametrize(
    "inclination",
    [0, 45, 90]
)
def test_eclipse_fraction_unaffected_by_inclination(inclination):
    """Eclipse fraction should not depend on inclination in this simplified model."""
    o1 = Orbit(altitude_km=ISS_ALTITUDE, inclination_deg=0)
    o2 = Orbit(altitude_km=ISS_ALTITUDE, inclination_deg=inclination)

    assert o1.calculate_eclipse_fraction() == o2.calculate_eclipse_fraction()

def test_eclipse_fraction_extreme_altitude():
    """At extremely high altitude eclipse fraction should approach zero."""
    orbit = Orbit(altitude_km=1_000_000)

    assert orbit.calculate_eclipse_fraction() < 0.01

def test_eclipse_fraction_surface_orbit():
    """At Earth's surface eclipse fraction should be approximately 0.5."""
    orbit = Orbit(altitude_km=0)

    assert orbit.calculate_eclipse_fraction() == pytest.approx(0.5, abs=0.01)

# ---------------------------------------------------------------------
# Eclipse Duration
# ---------------------------------------------------------------------

def test_eclipse_duration_iss_reference(iss_orbit):
    """ISS eclipse duration should be about 36 minutes (~2160 seconds)."""
    assert iss_orbit.calculate_eclipse_duration() == pytest.approx(2160, abs=60)

@pytest.mark.parametrize(
    "altitude",
    [LOW_LEO_ALTITUDE, ISS_ALTITUDE, HIGH_LEO_ALTITUDE]
)
def test_eclipse_duration_positive(altitude):
    """Eclipse duration must always be positive."""
    orbit = Orbit(altitude_km=altitude)

    assert orbit.calculate_eclipse_duration() > 0

@pytest.mark.parametrize(
    "altitude",
    [LOW_LEO_ALTITUDE, ISS_ALTITUDE, HIGH_LEO_ALTITUDE, GEO_ALTITUDE]
)
def test_eclipse_duration_less_than_orbital_period(altitude):
    """Eclipse duration cannot exceed the orbital period."""
    orbit = Orbit(altitude_km=altitude)

    assert orbit.calculate_eclipse_duration() < orbit.calculate_orbital_period()

def test_eclipse_duration_geo_reference(geo_orbit):
    """At GEO altitude eclipse duration should be ~4300 seconds."""
    assert geo_orbit.calculate_eclipse_duration() == pytest.approx(4300, abs=500)

@pytest.mark.parametrize(
    "lower_altitude, higher_altitude",
    [
        (LOW_LEO_ALTITUDE, ISS_ALTITUDE),
        (ISS_ALTITUDE, HIGH_LEO_ALTITUDE)
    ]
)
def test_eclipse_duration_decreases_with_altitude(lower_altitude, higher_altitude):
    """Eclipse duration should decrease as altitude increases."""
    low_orbit = Orbit(altitude_km=lower_altitude)
    high_orbit = Orbit(altitude_km=higher_altitude)

    assert high_orbit.calculate_eclipse_duration() < low_orbit.calculate_eclipse_duration()

@pytest.mark.parametrize(
    "inclination",
    [0, 45, 90]
)
def test_eclipse_duration_unaffected_by_inclination(inclination):
    """Eclipse duration should not depend on inclination."""
    o1 = Orbit(altitude_km=ISS_ALTITUDE, inclination_deg=0)
    o2 = Orbit(altitude_km=ISS_ALTITUDE, inclination_deg=inclination)

    assert o1.calculate_eclipse_duration() == o2.calculate_eclipse_duration()

# ---------------------------------------------------------------------------
# Sunlight Duration
# ---------------------------------------------------------------------------

def test_sunlight_duration_iss_reference(iss_orbit):
    """ISS sunlight duration should be ~56–57 minutes (~3394 seconds)."""
    assert iss_orbit.calculate_sunlight_duration() == pytest.approx(3394, abs=60)

@pytest.mark.parametrize(
    "altitude",
    [LOW_LEO_ALTITUDE, ISS_ALTITUDE, HIGH_LEO_ALTITUDE]
)
def test_sunlight_duration_positive(altitude):
    """Sunlight duration must always be positive."""
    orbit = Orbit(altitude_km=altitude)

    assert orbit.calculate_sunlight_duration() > 0

@pytest.mark.parametrize(
    "altitude",
    [LOW_LEO_ALTITUDE, ISS_ALTITUDE, HIGH_LEO_ALTITUDE]
)
def test_sunlight_duration_less_than_orbital_period(altitude):
    """Sunlight duration cannot exceed the orbital period."""
    orbit = Orbit(altitude_km=altitude)

    assert orbit.calculate_sunlight_duration() < orbit.calculate_orbital_period()

def test_sunlight_duration_geo_reference(geo_orbit):
    """At GEO altitude sunlight duration should be ~95% of the orbital period (~81800 seconds)."""
    assert geo_orbit.calculate_sunlight_duration() == pytest.approx(81800, abs=1000)

@pytest.mark.parametrize(
    "lower_altitude, higher_altitude",
    [
        (LOW_LEO_ALTITUDE, ISS_ALTITUDE),
        (ISS_ALTITUDE, HIGH_LEO_ALTITUDE),
        (HIGH_LEO_ALTITUDE, GEO_ALTITUDE)
    ]
)
def test_sunlight_duration_increases_with_altitude(lower_altitude, higher_altitude):
    """Sunlight duration should increase as altitude increases."""
    low_orbit = Orbit(altitude_km=lower_altitude)
    high_orbit = Orbit(altitude_km=higher_altitude)

    assert high_orbit.calculate_sunlight_duration() > low_orbit.calculate_sunlight_duration()

# ---------------------------------------------------------------------------
# Lighting Model Identities
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "altitude",
    [LOW_LEO_ALTITUDE, ISS_ALTITUDE, HIGH_LEO_ALTITUDE, GEO_ALTITUDE]
)
def test_sunlight_duration_plus_eclipse_duration_equals_orbital_period(altitude):
    """Sunlight duration plus eclipse duration should equal the orbital period."""
    orbit = Orbit(altitude_km=altitude)
    sunlight_duration = orbit.calculate_sunlight_duration()
    eclipse_duration = orbit.calculate_eclipse_duration()
    orbital_period = orbit.calculate_orbital_period()

    assert sunlight_duration + eclipse_duration == pytest.approx(orbital_period, rel=1e-3)

def test_orbit_lighting_identity(iss_orbit):
    """Sunlight fraction plus eclipse fraction should equal 1."""
    sunlight_fraction = iss_orbit.calculate_sunlight_duration() / iss_orbit.calculate_orbital_period()
    eclipse_fraction = iss_orbit.calculate_eclipse_fraction()

    assert sunlight_fraction + eclipse_fraction == pytest.approx(1.0, rel=1e-6)

# ---------------------------------------------------------------------------
# Property-Based Tests (Randomized Orbit Validation)
# ---------------------------------------------------------------------------

@given(
    altitude=st.floats(
        min_value=0, 
        max_value=1_000_000,
        allow_nan=False,
        allow_infinity=False,
        width=32
    )
)
def test_orbital_period_positive_property(altitude):
    """Orbital period should always be positive for valid altitudes."""
    orbit = Orbit(altitude_km=altitude)

    assert orbit.calculate_orbital_period() > 0

@given(
    altitude=st.floats(
        min_value=0, 
        max_value=1_000_000,
        allow_nan=False,
        allow_infinity=False,
        width=32
    )
)
def test_eclipse_fraction_property(altitude):
    """Eclipse fraction should always remain between 0 and 1."""
    orbit = Orbit(altitude_km=altitude)

    assert 0 <= orbit.calculate_eclipse_fraction() <= 1

@given(
    altitude=st.floats(
        min_value=0, 
        max_value=1_000_000,
        allow_nan=False,
        allow_infinity=False,
        width=32
    )
)
def test_lighting_identity_property(altitude):
    """Sunlight duration + eclipse duration should equal the orbital period."""
    orbit = Orbit(altitude_km=altitude)
    sunlight_duration = orbit.calculate_sunlight_duration()
    eclipse_duration = orbit.calculate_eclipse_duration()
    orbital_period = orbit.calculate_orbital_period()

    assert sunlight_duration + eclipse_duration == pytest.approx(orbital_period, rel=1e-6)

@given(
    altitude1=st.floats(
        min_value=0, 
        max_value=1_000_000,
        allow_nan=False,
        allow_infinity=False,
        width=32
    ),
    altitude2=st.floats(
        min_value=0, 
        max_value=1_000_000,
        allow_nan=False,
        allow_infinity=False,
        width=32
    )
)
def test_orbital_period_monotonic_property(altitude1, altitude2):
    """Orbital period should always increase with altitude."""
    import math

@given(
    altitude1=st.floats(
        min_value=0,
        max_value=1_000_000,
        allow_nan=False,
        allow_infinity=False,
        width=32
    ),
    altitude2=st.floats(
        min_value=0,
        max_value=1_000_000,
        allow_nan=False,
        allow_infinity=False,
        width=32
    )
)
def test_orbital_period_monotonic_property(altitude1, altitude2):
    """Orbital period should always increase with altitude."""

    if math.isclose(altitude1, altitude2, rel_tol=1e-9):
        return

    if altitude1 < altitude2:
        lower, higher = altitude1, altitude2
    else:
        lower, higher = altitude2, altitude1

    lower_orbit = Orbit(altitude_km=lower)
    higher_orbit = Orbit(altitude_km=higher)

    assert lower_orbit.calculate_orbital_period() < higher_orbit.calculate_orbital_period()

@given(
    altitude1=st.floats(
        min_value=0,
        max_value=1_000_000,
        allow_nan=False,
        allow_infinity=False,
        width=32
    ),
    altitude2=st.floats(
        min_value=0,
        max_value=1_000_000,
        allow_nan=False,
        allow_infinity=False,
        width=32
    )
)
def test_eclipse_fraction_monotonic_property(altitude1, altitude2):
    """Eclipse fraction should decrease with altitude."""

    if math.isclose(altitude1, altitude2, rel_tol=1e-9):
        return

    lower_orbit = Orbit(altitude_km=altitude1)
    higher_orbit = Orbit(altitude_km=altitude2)

    f1 = lower_orbit.calculate_eclipse_fraction()
    f2 = higher_orbit.calculate_eclipse_fraction()

    if altitude1 < altitude2:
        assert f1 >= f2
    else:
        assert f2 >= f1

@given(
    altitude=st.floats(
        min_value=0,
        max_value=1_000_000,
        allow_nan=False,
        allow_infinity=False,
        width=32
    )
)
def test_orbital_radius_property(altitude):
    """Orbital radius must equal Earth radius + altitude."""
    orbit = Orbit(altitude_km=altitude)

    expected = (EARTH_RADIUS + altitude) * 1000
    assert orbit.orbital_radius == pytest.approx(expected)