"""
Geolocation module for distance calculations and location-based queries.

Provides:
- Haversine distance calculation between coordinates
- Bounding box calculation for efficient spatial queries
- Location extraction from natural language queries
- Coordinate lookup for major cities
"""
import math
import re
from typing import Optional, Tuple, List, Dict, Any
from dataclasses import dataclass


# ============================================================================
# COORDINATE DATA
# ============================================================================

# Major city coordinates (latitude, longitude)
CITY_COORDINATES: Dict[str, Tuple[float, float]] = {
    # Germany
    "munich": (48.1351, 11.5820),
    "münchen": (48.1351, 11.5820),
    "berlin": (52.5200, 13.4050),
    "hamburg": (53.5511, 9.9937),
    "cologne": (50.9375, 6.9603),
    "köln": (50.9375, 6.9603),
    "frankfurt": (50.1109, 8.6821),
    "stuttgart": (48.7758, 9.1829),
    "dusseldorf": (51.2277, 6.7735),
    "düsseldorf": (51.2277, 6.7735),
    "munich": (48.1351, 11.5820),
    "grassau": (47.7856, 12.4656),
    "baiersbronn": (48.5201, 8.3268),
    "dreis": (49.9377, 6.8109),
    "piesport": (49.8776, 6.9266),
    "perl": (49.5352, 6.3872),
    "sulzburg": (47.8405, 7.7089),
    "wachenheim": (49.4385, 8.1820),
    "hanover": (52.3759, 9.7320),
    "hannover": (52.3759, 9.7320),
    "karlsruhe": (49.0069, 8.4037),
    "mannheim": (49.4875, 8.4660),
    "constance": (47.6674, 9.1876),
    "konstanz": (47.6674, 9.1876),
    "krün": (47.4622, 11.1862),
    "sankt ingbert": (49.2729, 7.1120),
    "dortmund": (51.5136, 7.4653),
    "leipzig": (51.3397, 12.3731),
    "dresden": (51.0504, 13.7373),
    "bremen": (53.0793, 8.8017),
    "hanover": (52.3759, 9.7320),
    "nies": (52.3744, 9.7386),
    # Denmark
    "copenhagen": (55.6761, 12.5683),
    "københavn": (55.6761, 12.5683),
    "gentofte": (55.7481, 12.5412),
    # Norway
    "oslo": (59.9139, 10.7522),
    "stavanger": (58.9700, 5.7331),
    # Sweden
    "stockholm": (59.3293, 18.0686),
    # Japan
    "tokyo": (35.6762, 139.6503),
    "osaka": (34.6937, 135.5023),
    "kyoto": (35.0116, 135.7681),
    # Belgium
    "brussels": (50.8503, 4.3517),
    "antwerp": (51.2211, 4.4026),
    "antwerpen": (51.2211, 4.4026),
    "roeselare": (50.9374, 3.1404),
    # Slovenia
    "kobarid": (46.2472, 13.5379),
    # UAE
    "dubai": (25.2048, 55.2708),
    # France
    "paris": (48.8566, 2.3522),
    # Netherlands
    "amsterdam": (52.3676, 4.9041),
    # Switzerland
    "zurich": (47.3769, 8.5417),
    "geneva": (46.2044, 6.1432),
    # Italy
    "milan": (45.4642, 9.1900),
    "rome": (41.9028, 12.4964),
    # Spain
    "barcelona": (41.3851, 2.1734),
    "madrid": (40.4168, 3.7038),
    # UK
    "london": (51.5074, -0.1278),
    # Austria
    "vienna": (48.2082, 16.3738),
    "wien": (48.2082, 16.3738),
}


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class Location:
    """Represents a geographic location."""
    latitude: float
    longitude: float
    name: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "name": self.name
        }


@dataclass
class BoundingBox:
    """Bounding box for spatial queries."""
    north: float
    south: float
    east: float
    west: float

    def to_dict(self) -> Dict[str, float]:
        return {
            "north": self.north,
            "south": self.south,
            "east": self.east,
            "west": self.west
        }


# ============================================================================
# HAVERSINE DISTANCE
# ============================================================================

def haversine_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    unit: str = "km"
) -> float:
    """Calculate the great circle distance between two points on Earth.

    Args:
        lat1: Latitude of first point in decimal degrees
        lon1: Longitude of first point in decimal degrees
        lat2: Latitude of second point in decimal degrees
        lon2: Longitude of second point in decimal degrees
        unit: Distance unit ('km' or 'miles')

    Returns:
        Distance between the two points in the specified unit

    Example:
        >>> haversine_distance(48.1351, 11.5820, 52.5200, 13.4050)
        504.6  # km from Munich to Berlin
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))

    # Radius of Earth in kilometers
    r = 6371.0

    distance = c * r

    if unit == "miles":
        return distance * 0.621371
    return distance


def haversine_distance_km(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float
) -> float:
    """Calculate distance in kilometers."""
    return haversine_distance(lat1, lon1, lat2, lon2, "km")


def haversine_distance_miles(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float
) -> float:
    """Calculate distance in miles."""
    return haversine_distance(lat1, lon1, lat2, lon2, "miles")


# ============================================================================
# BOUNDING BOX CALCULATION
# ============================================================================

def calculate_bounding_box(
    latitude: float,
    longitude: float,
    radius_km: float
) -> BoundingBox:
    """Calculate a bounding box around a center point.

    Args:
        latitude: Center latitude
        longitude: Center longitude
        radius_km: Radius in kilometers

    Returns:
        BoundingBox with north, south, east, west boundaries

    Note:
        This is an approximation using 1 degree of latitude ≈ 111km
        and longitude distance varies with latitude.
    """
    # Approximate degrees per km
    lat_degrees_per_km = 1 / 111.0
    lon_degrees_per_km = 1 / (111.0 * math.cos(math.radians(latitude)))

    # Calculate boundaries
    lat_delta = radius_km * lat_degrees_per_km
    lon_delta = radius_km * lon_degrees_per_km

    return BoundingBox(
        north=min(latitude + lat_delta, 90.0),
        south=max(latitude - lat_delta, -90.0),
        east=min(longitude + lon_delta, 180.0),
        west=max(longitude - lon_delta, -180.0)
    )


def point_in_bounding_box(
    lat: float,
    lon: float,
    bbox: BoundingBox
) -> bool:
    """Check if a point is within a bounding box."""
    return bbox.south <= lat <= bbox.north and bbox.west <= lon <= bbox.east


# ============================================================================
# LOCATION EXTRACTION FROM QUERY
# ============================================================================

def extract_location_from_query(query: str) -> Optional[Location]:
    """Extract location from natural language query.

    Args:
        query: User's query text

    Returns:
        Location object if found, None otherwise

    Examples:
        >>> extract_location_from_query("restaurants near Munich")
        Location(latitude=48.1351, longitude=11.5820, name='Munich')

        >>> extract_location_from_query("dining in Tokyo")
        Location(latitude=35.6762, longitude=139.6503, name='Tokyo')
    """
    query_lower = query.lower()

    # Check for city names in our database
    for city, coords in CITY_COORDINATES.items():
        # Check whole word match to avoid partial matches
        pattern = r'\b' + re.escape(city) + r'\b'
        if re.search(pattern, query_lower):
            return Location(
                latitude=coords[0],
                longitude=coords[1],
                name=city.title()
            )

    # Check for "near me" patterns (user needs to provide location)
    if re.search(r'\b(near\s+me|nearby|around\s+me|close\s+by)\b', query_lower):
        return None  # Indicates user location is needed

    return None


def extract_distance_from_query(query: str) -> Optional[float]:
    """Extract distance constraint from query in kilometers.

    Args:
        query: User's query text

    Returns:
        Distance in kilometers if found, None otherwise

    Examples:
        >>> extract_distance_from_query("within 50km")
        50.0

        >>> extract_distance_from_query("within 100 kilometers")
        100.0
    """
    query_lower = query.lower()

    # Match patterns like "within 50km", "within 100 km", "within 25 kilometers"
    match = re.search(r'within\s+(\d+)\s*(?:km|kilometers?|kilometres?)\b', query_lower)
    if match:
        return float(match.group(1))

    # Match "near me" - default to 25km
    if re.search(r'\b(near\s+me|nearby)\b', query_lower):
        return 25.0

    # Match "around" - default to 50km
    if re.search(r'\baround\b', query_lower):
        return 50.0

    return None


def extract_coordinates_from_query(query: str) -> Optional[Location]:
    """Extract coordinates from query if provided directly.

    Args:
        query: User's query text

    Returns:
        Location with coordinates if found, None otherwise

    Examples:
        >>> extract_coordinates_from_query("at 48.1351, 11.5820")
        Location(latitude=48.1351, longitude=11.5820, name=None)
    """
    # Match coordinate patterns: (lat, lon) or lat, lon or lat lon
    coord_pattern = r'''
        (?:
            \(\s*([-+]?\d+\.?\d*)\s*[,\s]\s*([-+]?\d+\.?\d*)\s*\)  # (lat, lon)
            |
            (?:lat[:\s]*)([-+]?\d+\.?\d*)\s*(?:lon[:\s]*)([-+]?\d+\.?\d*)  # lat:X lon:Y
            |
            \b([-+]?\d{2,3}\.\d+)\s*[,\s]\s*([-+]?\d{2,4}\.\d+)\b  # lat lon
        )
    '''
    match = re.search(coord_pattern, query, re.VERBOSE | re.IGNORECASE)
    if match:
        groups = match.groups()
        lat = None
        lon = None
        for g in groups:
            if g is not None:
                try:
                    val = float(g)
                    if -90 <= val <= 90 and lat is None:
                        lat = val
                    elif -180 <= val <= 180:
                        lon = val
                except ValueError:
                    continue

        if lat is not None and lon is not None:
            return Location(latitude=lat, longitude=lon)

    return None


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def format_distance(distance_km: float, precision: int = 1) -> str:
    """Format distance for display.

    Args:
        distance_km: Distance in kilometers
        precision: Decimal places

    Returns:
        Formatted distance string
    """
    if distance_km < 1:
        return f"{distance_km * 1000:.0f}m"
    return f"{distance_km:.{precision}f}km"


def get_city_coordinates(city_name: str) -> Optional[Tuple[float, float]]:
    """Get coordinates for a city.

    Args:
        city_name: Name of the city

    Returns:
        Tuple of (latitude, longitude) if found, None otherwise
    """
    return CITY_COORDINATES.get(city_name.lower())


def add_distance_to_restaurants(
    restaurants: List[Dict[str, Any]],
    center_lat: float,
    center_lon: float
) -> List[Dict[str, Any]]:
    """Add distance_km field to restaurant dictionaries.

    Args:
        restaurants: List of restaurant dictionaries with lat/lon
        center_lat: Center point latitude
        center_lon: Center point longitude

    Returns:
        List of restaurants with distance_km added
    """
    for restaurant in restaurants:
        lat = restaurant.get('latitude')
        lon = restaurant.get('longitude')
        if lat is not None and lon is not None:
            restaurant['distance_km'] = haversine_distance_km(
                center_lat, center_lon, lat, lon
            )
        else:
            restaurant['distance_km'] = None

    return restaurants


def sort_by_distance(
    restaurants: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Sort restaurants by distance (nearest first).

    Filters out restaurants without distance information.
    """
    with_distance = [r for r in restaurants if r.get('distance_km') is not None]
    without_distance = [r for r in restaurants if r.get('distance_km') is None]

    with_distance.sort(key=lambda x: x['distance_km'])
    return with_distance + without_distance


def filter_by_radius(
    restaurants: List[Dict[str, Any]],
    radius_km: float
) -> List[Dict[str, Any]]:
    """Filter restaurants to those within a given radius.

    Args:
        restaurants: List of restaurants with distance_km field
        radius_km: Maximum distance in kilometers

    Returns:
        Filtered list of restaurants
    """
    return [
        r for r in restaurants
        if r.get('distance_km') is not None and r['distance_km'] <= radius_km
    ]


# ============================================================================
# GEOLOCATION QUERY ANALYSIS
# ============================================================================

def analyze_geolocation_query(query: str) -> Dict[str, Any]:
    """Analyze a query for geolocation components.

    Args:
        query: User's query text

    Returns:
        Dictionary with geolocation analysis results
    """
    return {
        "is_geo_query": (
            "near" in query.lower() or
            "around" in query.lower() or
            "nearby" in query.lower() or
            "within" in query.lower() or
            extract_location_from_query(query) is not None
        ),
        "location": extract_location_from_query(query),
        "coordinates": extract_coordinates_from_query(query),
        "distance_constraint": extract_distance_from_query(query),
        "needs_user_location": "near me" in query.lower() or "nearby" in query.lower(),
    }


# ============================================================================
# COORDINATE VALIDATION
# ============================================================================

def validate_coordinates(latitude: float, longitude: float) -> bool:
    """Validate that coordinates are within valid ranges."""
    return -90 <= latitude <= 90 and -180 <= longitude <= 180


def normalize_coordinates(latitude: float, longitude: float) -> Tuple[float, float]:
    """Normalize coordinates to valid ranges."""
    lat = max(-90, min(90, latitude))
    lon = ((longitude + 180) % 360) - 180
    return lat, lon
