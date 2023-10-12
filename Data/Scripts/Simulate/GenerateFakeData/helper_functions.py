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
import string
import uuid
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


def generate_random_string(length=15):
    """Generates a random string of the given length."""
    alphabet = string.ascii_lowercase + string.digits
    random_string = ""
    for i in range(length):
        random_string += random.choice(alphabet)
    return random_string


def generate_location() -> tuple:
    """
    Generate random location in London.

    Returns:
    -------
    tuple
        A tuple contain Latitude, longitude and geolocator variable
    """

    geolocator = Nominatim(user_agent=generate_random_string())
    # geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    location = geolocator.geocode('London, UK', timeout=60)

    london_latitude = location.latitude
    london_longitude = location.longitude

    latitude = random.uniform(london_latitude - 0.1, london_latitude + 0.1)
    longitude = random.uniform(london_longitude - 0.1, london_longitude + 0.1)

    return latitude, longitude, geolocator


def generate_date_time(start_date: datetime = "-10y", end_time: datetime = "now") -> datetime.datetime:
    """
    Get a datetime object based on a random date between
    two given dates. Accepts date strings that can be recognized by strtotime().

    Parameters
    ----------
    start_date: str | date object
        First time interval

    end_time: str | date object
        Second time interval

    Returns
    -------
    datetime
        random datetime
    """
    fake_datetime = fake.date_time_between(start_date=start_date, end_date=end_time)

    return fake_datetime


# def generate_date_time_between(start_time: datetime.datetime, end_time: datetime.datetime) -> datetime.datetime:
#     """
#     Takes two datetime objects and returns a random datetime between the two given datetimes.
#     Accepts datetime objects.
#
#     Parameters
#     ----------
#     start_time: datetime.datetime
#     end_time: datetime.datetime
#
#     Returns
#     -------
#     datetime.datetime
#     """
#     return fake.date_time_between_dates(datetime_start=start_time, datetime_end=end_time)


# def choice_status(status_list: list) -> str:
#     """
#     It randomly selects an item from a list
#
#     Parameters
#     ---------
#     status_list: list
#         A list contains items. (In this project list contain status of, vehicle, trip, and payment
#
#     Returns
#     -------
#     list item
#         An item from list (In this case str)
#
#     """
#     random.shuffle(status_list)
#     return random.choice(status_list)


def choice_status_weight(status_list: list, w: list, k: int) -> list:
    """
    This function creates a k list of elements chosen randomly and uses weight.
    Parameter
    ---------
    status_list: list
        A list of elements.
    w: list
        A list contains weight.
    k: int
        Number of elements we want to create.
    :return:
    """
    return random.choices(status_list, k=k, weights=w)


def convert_string_datetime_to_datetime(str_datetime) -> datetime.datetime:
    """
    This function convert string date time to datetime.

    Parameters
    ----------
    str_datetime : str
        String date time

    Returns
    -------
    DateTime
    """
    try:
        the_time = datetime.datetime.strptime(str_datetime, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        the_time = datetime.datetime.strptime(str_datetime, "%Y-%m-%d %H:%M:%S.%f")
    return the_time


def estimate_amount_formula(estimated_distance: float, number: int) -> float:
    """
    This function is a simple formula to estimate the price of trip.

    Parameter
    ---------
    estimate_distance: flat
        Estimate distance between start trip location and end trip location.
    number: int
        An int number based on the estimate distance
    """
    return estimated_distance * number


def generate_date_and_amount(start_location: tuple, end_location: tuple, start_time: datetime) -> tuple:
    """
    This function generates time of ending a trip and estimates the price.

    Calculation of price:
    Since the speed is measured in miles per hour, the easiest way to go about
    it is to compare your average speed to a single hour. For instance, if you’re
    going 60 mph, you travel 60 miles in one hour. There are 60 minutes in one hour,
    so just divide the miles by that amount, and voila! It takes only one minute to travel 1 mile.

    Parameters
    ----------
    start_location: list
        A list contains latitude and longitude of start trip location.
    end_location: list
        A list contains latitude and longitude of end trip location.
    start_time: DateTime
        The datetime which trip is started

    Returns
    -------
    tuple
        A tuple contain trip_distance, start_time, end_time, and amount.
    """

    # Estimate trip distance between start location and end location
    trip_distance = distance(start_location, end_location).miles

    # Calculate trip price and travel time based on the distance miles
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

    # Create travel end time
    end_time = (start_time + additional_time)
    end_time = str(end_time).split(".")[0]
    end_time = convert_string_datetime_to_datetime(end_time)

    return trip_distance, start_time, end_time, "{:.2f}".format(amount)


# def vehicle_last_time_seen(df_vehicle_modify: pd.DataFrame, vehicle_id) -> datetime.datetime:
#     """
#     This function generates time before vehicle last time seen.
#
#     :param df_vehicle_modify:
#     :param vehicle_id:
#     :return:
#     """
#     last_time = df_vehicle_modify.loc[df_vehicle_modify["vehicle_id"] == vehicle_id, "last_time"].values.tolist()[0]
#     last_time = convert_string_datetime_to_datetime(last_time)
#     subtract_time = last_time - datetime.timedelta(days=random.choice([3, 8, 4, 9, 2]))
#
#     return subtract_time


def create_trip_start_time(vehicle_info: pd.DataFrame,
                           vehicle_id: uuid,
                           customer_info: pd.DataFrame,
                           customer_id: uuid) -> datetime.datetime:
    """
    This function generate start trip time between customer join date and vehicle last seen datetime

    Parameters
    ----------
    vehicle_info: pandas DataFrame
        Vehicle dataframe (contains vehicle information)
    customer_info: pandas DataFrame
        Customer dataframe (contains customer information)
    vehicle_id: uuid
        ID of a specific vehicle
    customer_id: uuid
        ID of a specific customer

    Returns
    -------
        datetime.datetime
    """
    # Find vehicle status
    vehicle_last_seen = vehicle_info.loc[vehicle_info["VehicleId"] == vehicle_id, "LastTime"].values.tolist()[0]
    vehicle_last_seen = convert_string_datetime_to_datetime(vehicle_last_seen)

    # Create datetime before vehicle last seen
    days_before_last_seen = vehicle_last_seen - timedelta(days=random.choice([3, 8, 4, 9, 2]))

    # Find customer join date
    customer_join_date = customer_info.loc[customer_info["CustomerId"] == customer_id].values.tolist()
    customer_join_date = customer_join_date[0][-1]
    customer_join_date = convert_string_datetime_to_datetime(customer_join_date)

    # Create start trip time
    start_trip_time = generate_date_time(customer_join_date, days_before_last_seen)
    start_trip_time = str(start_trip_time).split(".")[0]
    start_trip_time = convert_string_datetime_to_datetime(start_trip_time)

    return start_trip_time


def generate_random_time_between(start_time: datetime.datetime, end_time: datetime.datetime) -> datetime.datetime:
    """
    This function generates datetime between start trip time and estimated end trip time.
    When trip status is "Started".

    Parameters:
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

    start_time += datetime.timedelta(seconds=random_second)
    start_time = str(start_time).split(".")[0]
    start_time = convert_string_datetime_to_datetime(start_time)

    return start_time


def generate_transaction_time(start_trip_time: str, end_trip_time: str) -> datetime.datetime:
    """
    This function generates datetime for payment transaction randomly.

    Parameters
    ----------
    start_trip_time: str
    end_trip_time: str

    Returns
    -------
    datetime.datetime
    """
    trip_start_time = convert_string_datetime_to_datetime(start_trip_time)
    trip_end_time = convert_string_datetime_to_datetime(end_trip_time)

    transaction_time = generate_date_time(trip_start_time, trip_end_time)

    return transaction_time


if __name__ == "__main__":
    one = generate_transaction_time("2023-10-09 11:48:39", "2023-10-09 11:51:39")
    print(type(one), one)
