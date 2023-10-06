"""
    This script generates fake trip information using 'fake' and 'geopy' Python libraries.

    Fake and geopy libraries randomly generate the date and location.
    For each status, a start date is created between two arbitrary dates,
    and then the generate_date_and_amount function is used to estimate the distance traveled,
    the amount, and the time it takes to reach the destination.
    We do not set an end date for any trip that has the star status.

    Dependencies:
        - fake library (install using 'pip install fake')
        - geopy library
"""

import datetime

import numpy as np
from faker import Faker

from helper_functions import generate_location, generate_date_and_amount

TRIP_STATUS = ['Start', 'End', 'Cancel']

fake_trip = Faker()


def generate_random_location() -> tuple:
    """
    This function generates a random location for start and ends a trip to London.

    Returns
    -------
    tuple
        A tuple contain latitude and longitude.
    """

    lat, long, _ = generate_location()
    return lat, long


def generate_trip_info_dict(trip_id: int,
                            customer_id: int,
                            vehicle_id: int,
                            payment_id: int,
                            start_time: datetime,
                            status: str) -> dict:
    """
    This function creates a dictionary of trip information.
    It tries to generate trip time greater than customer join date.

    Parameters
    ----------
    trip_id: int
    customer_id: int
    vehicle_id: int
    payment_id: int
    start_time: datetime
        Customer join date
    status: str

    Returns
    -------
    Python dictionary
        A dictionary contains trip information.

    """
    # Generate random location for start point and end point.
    start_lat_trip, start_long_trip = generate_random_location()
    end_lat_trip, end_long_trip = generate_random_location()

    # trip_distance = distance((start_lat_trip, start_long_trip), (end_lat_trip, end_long_trip)).miles

    # Estimate the amount, distance and trip time.
    estimate_distance, start_trip_time, end_trip_time, estimate_amount = generate_date_and_amount(
        (start_lat_trip, start_long_trip), (end_lat_trip, end_long_trip), start_time)

    if status == TRIP_STATUS[0]:
        end_trip_time = np.NaN


    return {
        "trip_id": trip_id,
        "customer_id": customer_id,
        "vehicle_id": vehicle_id,
        "payment_id": payment_id,
        "start_latitude_trip": start_lat_trip,
        "start_longitude_trip": start_long_trip,
        "end_latitude_trip": end_lat_trip,
        "end_longitude_trip": end_long_trip,
        "estimate_distance": estimate_distance,
        "start_trip_time": start_time,
        "end_trip_time": end_trip_time,
        "amount": estimate_amount,
        "status": status
    }


if __name__ == "__main__":
    print("Hello!")
