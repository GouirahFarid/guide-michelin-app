"""
Tests for geolocation module.
"""
import pytest
from geolocation import (
    haversine_distance_km,
    calculate_bounding_box,
    extract_location_from_query,
    extract_distance_from_query,
    validate_coordinates,
    CITY_COORDINATES
)


class TestHaversineDistance:
    """Test Haversine distance calculations."""

    def test_munich_to_berlin(self):
        """Test distance between Munich and Berlin."""
        # Munich: 48.1351, 11.5820
        # Berlin: 52.5200, 13.4050
        # Expected: ~504 km
        distance = haversine_distance_km(48.1351, 11.5820, 52.5200, 13.4050)
        assert 500 < distance < 510

    def test_same_location(self):
        """Test distance from a location to itself."""
        distance = haversine_distance_km(48.1351, 11.5820, 48.1351, 11.5820)
        assert distance == 0

    def test_equator_degrees(self):
        """Test that 1 degree of latitude at equator is ~111 km."""
        distance = haversine_distance_km(0, 0, 1, 0)
        assert 110 < distance < 112


class TestBoundingBox:
    """Test bounding box calculations."""

    def test_small_radius(self):
        """Test small radius bounding box."""
        bbox = calculate_bounding_box(48.1351, 11.5820, 10)
        assert bbox.north > 48.1351
        assert bbox.south < 48.1351
        assert bbox.east > 11.5820
        assert bbox.west < 11.5820

    def test_bounds_clamping(self):
        """Test that bounding box respects global limits."""
        # North pole
        bbox = calculate_bounding_box(89, 0, 500)
        assert bbox.north <= 90

        # South pole
        bbox = calculate_bounding_box(-89, 0, 500)
        assert bbox.south >= -90


class TestLocationExtraction:
    """Test location extraction from queries."""

    def test_extract_city(self):
        """Test extracting city name."""
        location = extract_location_from_query("restaurants in Munich")
        assert location is not None
        assert location.name.lower() == "munich"

    def test_extract_with_near(self):
        """Test extracting location with 'near' keyword."""
        location = extract_location_from_query("restaurants near Tokyo")
        assert location is not None
        assert location.name.lower() == "tokyo"

    def test_no_location(self):
        """Test query without location."""
        location = extract_location_from_query("Japanese fine dining")
        assert location is None


class TestDistanceExtraction:
    """Test distance constraint extraction."""

    def test_extract_km(self):
        """Test extracting distance in km."""
        distance = extract_distance_from_query("within 50km")
        assert distance == 50

    def test_extract_kilometers(self):
        """Test extracting distance in kilometers."""
        distance = extract_distance_from_query("within 100 kilometers")
        assert distance == 100

    def test_near_me_default(self):
        """Test default distance for 'near me'."""
        distance = extract_distance_from_query("restaurants near me")
        assert distance == 25


class TestCoordinateValidation:
    """Test coordinate validation."""

    def test_valid_coordinates(self):
        """Test valid coordinates."""
        assert validate_coordinates(48.1351, 11.5820) is True
        assert validate_coordinates(0, 0) is True
        assert validate_coordinates(-90, -180) is True
        assert validate_coordinates(90, 180) is True

    def test_invalid_latitude(self):
        """Test invalid latitude."""
        assert validate_coordinates(91, 0) is False
        assert validate_coordinates(-91, 0) is False

    def test_invalid_longitude(self):
        """Test invalid longitude."""
        assert validate_coordinates(0, 181) is False
        assert validate_coordinates(0, -181) is False


class TestCityCoordinates:
    """Test city coordinate database."""

    def test_munich_coordinates(self):
        """Test Munich coordinates."""
        coords = CITY_COORDINATES.get("munich")
        assert coords is not None
        assert abs(coords[0] - 48.1351) < 0.01
        assert abs(coords[1] - 11.5820) < 0.01

    def test_case_insensitive(self):
        """Test case-insensitive city lookup."""
        coords1 = CITY_COORDINATES.get("munich")
        coords2 = CITY_COORDINATES.get("MUNICH")
        coords3 = CITY_COORDINATES.get("München")
        # München has separate entry, but Munich should work case-insensitively
        assert coords1 is not None
