import requests

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
USER_AGENT = "DisasterResponseAgent/1.0"

def find_nearby_resources(latitude: float, longitude: float, radius: int = 5000) -> dict:
    """Finds nearby emergency resources (hospitals, clinics).

    Args:
        latitude: Latitude of the incident location.
        longitude: Longitude of the incident location.
        radius: Search radius in meters (default 5000 = 5 km).

    Returns:
        A dict with keys 'hospitals', 'shelters', and 'note'.
    """
    overpass_query = f"""
    [out:json];
    (
      node["amenity"="hospital"](around:{radius},{latitude},{longitude});
      node["amenity"="clinic"](around:{radius},{latitude},{longitude});
      node["emergency"="disaster_response"](around:{radius},{latitude},{longitude});
    );
    out body;
    """
    headers = {"Accept": "application/json", "User-Agent": USER_AGENT}

    try:
        response = requests.get(
            OVERPASS_URL,
            params={"data": overpass_query},
            headers=headers,
            timeout=15,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {
            "hospitals": [],
            "shelters": [],
            "error": f"Resource lookup temporarily unavailable: {str(e)}",
            "note": "Could not reach OpenStreetMap data source. Proceed with protocol guidance only.",
        }

    elements = response.json().get("elements", [])

    hospitals = []
    shelters = []

    for el in elements:
        tags = el.get("tags", {})
        name = tags.get("name", "Unnamed facility")
        lat = el.get("lat")
        lon = el.get("lon")
        amenity = tags.get("amenity", "")

        entry = {"name": name, "latitude": lat, "longitude": lon}

        if amenity in ("hospital", "clinic"):
            hospitals.append(entry)
        else:
            shelters.append(entry)

    return {
        "hospitals": hospitals[:10],
        "shelters": shelters[:10],
        "note": f"Resources within {radius/1000:.1f} km of ({latitude}, {longitude})",
    }