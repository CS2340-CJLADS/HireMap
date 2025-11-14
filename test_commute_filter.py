"""
Test cases for the commute radius filter feature
"""
from seeker.utils import calculate_distance, filter_jobs_by_commute


def test_calculate_distance():
    """Test the Haversine distance calculation"""

    # Test 1: Distance from New York to Los Angeles (known ~2,451 miles)
    ny_lat, ny_lon = 40.7128, -74.0060
    la_lat, la_lon = 34.0522, -118.2437
    distance = calculate_distance(ny_lat, ny_lon, la_lat, la_lon)
    print(f"New York to Los Angeles: {distance:.2f} miles")
    assert 2400 < distance < 2500, "Distance should be approximately 2,451 miles"

    # Test 2: Distance from San Francisco to San Jose (known ~42 miles)
    sf_lat, sf_lon = 37.7749, -122.4194
    sj_lat, sj_lon = 37.3382, -121.8863
    distance = calculate_distance(sf_lat, sf_lon, sj_lat, sj_lon)
    print(f"San Francisco to San Jose: {distance:.2f} miles")
    assert 40 < distance < 50, "Distance should be approximately 42 miles"

    # Test 3: Same location (should be 0)
    distance = calculate_distance(sf_lat, sf_lon, sf_lat, sf_lon)
    print(f"Same location distance: {distance:.2f} miles")
    assert distance < 0.1, "Distance to same location should be approximately 0"

    # Test 4: Atlanta to Boston (known ~946 miles)
    atl_lat, atl_lon = 33.7490, -84.3880
    bos_lat, bos_lon = 42.3601, -71.0589
    distance = calculate_distance(atl_lat, atl_lon, bos_lat, bos_lon)
    print(f"Atlanta to Boston: {distance:.2f} miles")
    assert 900 < distance < 1000, "Distance should be approximately 946 miles"

    print("\n✓ All distance calculation tests passed!")


def test_filter_jobs_by_commute_mock():
    """Test the job filtering logic with mock data"""

    # Mock job class
    class MockJob:
        def __init__(self, id, title, lat, lon, remote=False):
            self.id = id
            self.title = title
            self.location_lat = lat
            self.location_lon = lon
            self.remote = remote

    # User location: San Francisco
    user_lat, user_lon = 37.7749, -122.4194

    # Create mock jobs
    jobs = [
        MockJob(1, "Job in SF", 37.7749, -122.4194, False),  # Same location (~0 miles)
        MockJob(2, "Job in San Jose", 37.3382, -121.8863, False),  # ~42 miles
        MockJob(3, "Job in Oakland", 37.8044, -122.2712, False),  # ~12 miles
        MockJob(4, "Job in LA", 34.0522, -118.2437, False),  # ~347 miles
        MockJob(5, "Remote Job in NY", 40.7128, -74.0060, True),  # Remote, always included
        MockJob(6, "Job without coords", None, None, False),  # No coordinates
    ]

    # Test with 50 mile radius
    max_distance = 50
    job_ids = filter_jobs_by_commute(jobs, user_lat, user_lon, max_distance)
    print(f"\nJobs within {max_distance} miles: {job_ids}")

    # Should include: SF (0mi), Oakland (12mi), San Jose (42mi), Remote job
    # Should exclude: LA (347mi), job without coords
    assert 1 in job_ids, "Job in SF should be included"
    assert 2 in job_ids, "Job in San Jose should be included"
    assert 3 in job_ids, "Job in Oakland should be included"
    assert 5 in job_ids, "Remote job should always be included"
    assert 4 not in job_ids, "Job in LA should be excluded"
    assert 6 not in job_ids, "Job without coordinates should be excluded"

    # Test with 10 mile radius
    max_distance = 10
    job_ids = filter_jobs_by_commute(jobs, user_lat, user_lon, max_distance)
    print(f"Jobs within {max_distance} miles: {job_ids}")

    # Should include: SF (0mi), Oakland (~8mi), Remote job
    # Should exclude: San Jose (42mi), LA (347mi)
    assert 1 in job_ids, "Job in SF should be included"
    assert 3 in job_ids, "Job in Oakland should be included"
    assert 5 in job_ids, "Remote job should always be included"
    assert 2 not in job_ids, "Job in San Jose should be excluded"
    assert 4 not in job_ids, "Job in LA should be excluded"

    print("✓ All job filtering tests passed!")


if __name__ == "__main__":
    test_calculate_distance()
    test_filter_jobs_by_commute_mock()
    print("\n✅ All tests passed successfully!")

