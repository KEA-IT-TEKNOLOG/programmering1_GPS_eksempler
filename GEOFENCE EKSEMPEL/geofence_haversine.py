import math

def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in meters
    earth_radius = 6371000  # meters

    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Calculate the distance
    distance = earth_radius * c

    return distance

def is_within_geofence(lat1, lon1, geofence_lat, geofence_lon, radius=10):
    # Calculate the distance between the GPS coordinate and the center of the geofence
    distance = haversine(lat1, lon1, geofence_lat, geofence_lon)

    # Check if the distance is less than or equal to the radius
    return distance <= radius

# Example usage:
geofence_lat = 55.694340  # Latitude of the geofence center
geofence_lon = 12.548808  # Longitude of the geofence center
lat1 = 55.694132  # Latitude of the GPS coordinate to check
lon1 = 12.548588  # Longitude of the GPS coordinate to check

result = is_within_geofence(lat1, lon1, geofence_lat, geofence_lon, radius=10)
if result:
    print("The GPS coordinate is within the geofence.")
else:
    print("The GPS coordinate is outside the geofence.")
