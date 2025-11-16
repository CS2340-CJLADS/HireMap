"""Utility functions for seeker app"""
import math


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points on Earth using the Haversine formula.
    Returns distance in miles.

    Args:
        lat1, lon1: Latitude and longitude of first point (in degrees)
        lat2, lon2: Latitude and longitude of second point (in degrees)

    Returns:
        Distance in miles
    """
    # Radius of Earth in miles
    R = 3958.8

    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))

    distance = R * c

    return distance


def filter_jobs_by_commute(jobs, user_lat, user_lon, max_distance_miles):
    """
    Filter a queryset of jobs to only include those within max_distance_miles
    from the user's location.

    Args:
        jobs: QuerySet of JobPosting objects
        user_lat, user_lon: User's latitude and longitude
        max_distance_miles: Maximum distance in miles

    Returns:
        List of job IDs that are within the commute radius
    """
    if not user_lat or not user_lon or not max_distance_miles:
        return jobs

    job_ids_within_radius = []

    for job in jobs:
        # Skip jobs without location coordinates
        if not job.location_lat or not job.location_lon:
            continue

        # Remote jobs are always included (no commute needed)
        if job.remote:
            job_ids_within_radius.append(job.id)
            continue

        # Calculate distance
        distance = calculate_distance(
            user_lat, user_lon,
            job.location_lat, job.location_lon
        )

        # Include job if within radius
        if distance <= float(max_distance_miles):
            job_ids_within_radius.append(job.id)

    return job_ids_within_radius

