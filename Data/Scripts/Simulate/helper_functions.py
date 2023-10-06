"""
    This script helps users to generate addresses and geolocations
    of random places in London.
    It Also, generates random IDs,
    and random dates-times.
    Users can also extract
    a random item from a list using the choice_status function.

    This script required 'faker' and 'geopy' python libraries.
"""

import datetime
import random
from datetime import timedelta

import pandas as pd
from faker import Faker
from geopy.distance import distance
from geopy.geocoders import Nominatim

fake = Faker()

MINUTES_UNDER_ONE_MILE = [3, 5, 6, 7]
MINUTES_ONE_TWO = [8, 9, 10, 11, 12, 13, 14, 15]
MINUTES_TWO_FOUR = [18, 20, 23, 25, 30]
MINUTES_FOUR_SIX = [35, 38, 40, 42, 45, 50, 55]


def generate_location() -> tuple:
    """
    Generate random location in London.

    Returns:
    -------
    tuple
        A tuple contain Latitude, longitude and geolocator variable
    """

    geolocator = Nominatim(user_agent='AutoRide')
    location = geolocator.geocode('London, UK', timeout=500)

    london_latitude = location.latitude
    london_longitude = location.longitude

    latitude = random.uniform(london_latitude - 0.1, london_latitude + 0.1)
    longitude = random.uniform(london_longitude - 0.1, london_longitude + 0.1)

    return latitude, longitude, geolocator


def generate_date_time(start_date="-10y", end_time="now"):
    """
    Generates the random date-time in a date-time interval

    Parameters
    ----------
    start_date: str
        First time interval

    end_time: str
        Second time interval

    Returns
    -------
    datetime
        random datetime
    """
    fake_datetime = fake.date_time_between(start_date=start_date, end_date=end_time)

    return fake_datetime


def generate_date_time_between(start_time, end_time):
    return fake.date_time_between_dates(datetime_start=start_time, datetime_end=end_time)


def generate_id(start_int=1, end_int=100) -> int:
    """
    Creates a random number between two selected numbers.

    Parameters
    ----------
    start_int: int
        First number
    end_int: int
        Second number

    Returns
    -------
    int
        A random number
    """
    return random.randint(start_int, end_int)


def choice_status(status_list):
    """
    It randomly selects an item from a list

    Parameters
    ---------
    status_list: list
        A list contains items. (In this project list contain status of, vehicle, trip, and payment

    Returns
    -------
    list item
        An item from list

    """
    random.shuffle(status_list)
    return random.choice(status_list)


def choice_status_weight(status_list, w, k):
    return random.choices(status_list, k=k, weights=w)


def convert_string_datetime_to_datetime(str_datetime, format_str="%Y-%m-%d %H:%M:%S.%f"):
    """
    This function convert string date time to datetime.

    Parameters
    ----------
    str_datetime : str
        String date time
    format_str : str
        Format of datetime

    Returns
    -------
    DateTime
    """
    try:
        the_time = datetime.datetime.strptime(str_datetime, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        the_time = datetime.datetime.strptime(str_datetime, "%Y-%m-%d %H:%M:%S.%f")
    return the_time


def estimate_amount_formula(estimated_distance, number):
    return estimated_distance * number


def generate_date_and_amount(start_lat, start_long, start_time: datetime) -> tuple:
    """
    This function generates time of ending a trip and estimates the price.

    Calculation of price:
    Since the speed is measured in miles per hour, the easiest way to go about
    it is to compare your average speed to a single hour. For instance, if you’re
    going 60 mph, you travel 60 miles in one hour. There are 60 minutes in one hour,
    so just divide the miles by that amount, and voila! It takes only one minute to travel 1 mile.

    Parameters
    ----------
    trip_distance: int
        Distance between two points
    start_time: DateTime
        The datetime which trip is started

    Returns
    -------
    tuple
        A tuple contain trip_distance, start_time, end_time, and amount.
    """

    # Lists of minutest for each mile.
    trip_distance = distance(start_lat, start_long).miles
    if trip_distance < 1:
        amount = estimate_amount_formula(trip_distance, 7)
        additional_time = datetime.timedelta(minutes=random.choice(MINUTES_UNDER_ONE_MILE))
    elif 1 <= trip_distance <= 2:
        amount = estimate_amount_formula(trip_distance, number=5)
        additional_time = datetime.timedelta(minutes=random.choice(MINUTES_ONE_TWO))
    elif 2 <= trip_distance <= 4:
        amount = estimate_amount_formula(trip_distance, 4)
        additional_time = datetime.timedelta(minutes=random.choice(MINUTES_TWO_FOUR))
    elif 4 <= trip_distance <= 6:
        amount = estimate_amount_formula(trip_distance, 3)
        additional_time = datetime.timedelta(minutes=random.choice(MINUTES_FOUR_SIX))
    else:
        amount = estimate_amount_formula(trip_distance, 2)
        additional_time = datetime.timedelta(hours=1, minutes=random.choice(MINUTES_FOUR_SIX))

    end_time = (start_time + additional_time)
    end_time = str(end_time).split(".")[0]
    end_time = convert_string_datetime_to_datetime(end_time)

    return trip_distance, start_time, end_time, "{:.2f}".format(amount)


def vehicle_last_time_seen(df_vehicle_modify: pd.DataFrame, vehicle_id):
    last_time = df_vehicle_modify.loc[df_vehicle_modify["vehicle_id"] == vehicle_id, "last_time"].values.tolist()[0]
    last_time = convert_string_datetime_to_datetime(last_time)
    subtract_time = last_time - datetime.timedelta(days=random.choice([3, 8, 4, 9, 2]))

    return subtract_time


def create_trip_start_time(vehicle_info, vehicle_id, customer_info, customer_id):
    # Find vehicle status
    vehicle_last_seen = vehicle_info.loc[vehicle_info["vehicle_id"] == vehicle_id, "last_time"].values.tolist()[0]
    # print(f"vehicle last seen before: {vehicle_last_seen}")
    vehicle_last_seen = convert_string_datetime_to_datetime(vehicle_last_seen)
    # print(f"vehicle_last_seen after convert string: {vehicle_last_seen}\n")

    # Create datetime before vehicle last seen
    days_before_last_seen = vehicle_last_seen - timedelta(days=random.choice([3, 8, 4, 9, 2]))

    # Find customer join date
    customer_join_date = customer_info.loc[customer_info["id"] == customer_id].values.tolist()
    customer_join_date = customer_join_date[0][-1]
    customer_join_date = convert_string_datetime_to_datetime(customer_join_date)

    start_trip_time = generate_date_time(customer_join_date, days_before_last_seen)
    start_trip_time = str(start_trip_time).split(".")[0]
    start_trip_time = convert_string_datetime_to_datetime(start_trip_time)

    return start_trip_time


def generate_random_time_between(start_time, end_time):
    """Generates a random time between two times.

    Args:
      start_time: A datetime object representing the start time.
      end_time: A datetime object representing the end time.

    Returns:
      A datetime object representing the random time.
    """

    # Calculate the duration in seconds between the two times.
    duration = end_time - start_time
    duration_in_seconds = duration.total_seconds()

    # Generate a random number in the range of the start and end times.
    random_second = random.randint(0, int(duration_in_seconds))
    tart_time = start_time + datetime.timedelta(seconds=random_second)
    tart_time = str(tart_time).split(".")[0]
    tart_time = convert_string_datetime_to_datetime(tart_time)

    # Add the random number to the start time to get the random time.
    return tart_time


if __name__ == "__main__":
    TRIP_STATUS = ['Start', 'End', 'Cancel']
    PAYMENT_STATUS = ['Successful', 'Unsuccessful']
    VEHICLE_STATUS = ['Busy', 'UnderRepair', 'Vacant']

    test_1 = choice_status_weight(TRIP_STATUS, k=50, w=[25, 65, 10])
    test_2 = choice_status_weight(PAYMENT_STATUS, k=50, w=[90, 10])
    test_3 = choice_status_weight(VEHICLE_STATUS, k=50, w=[60, 5, 35])
    print(test_1)
    print(test_2)
    print(test_3)
    print("-" * 10)
