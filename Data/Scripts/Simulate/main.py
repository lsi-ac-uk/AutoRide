"""
    This is the main script and responsible to generate fake information
    about customer, vehicle, trip, and payment.
    Also, it creates CSV files from DataFrames.

    Functions:
    create_fake_vehicle_information(number_of_items):
        This function takes the desired number of cars as input, then assigns weights to the status of the car
        and produces the desired number of cars.
        The output of this function is a dataframe of cars.

    create_fake_customer_information(number_of_items):
        This function takes the desired number of customers as input, and produces the desired number of customers.
        The output of this function is a dataframe of customers.

    create_fake_trip(number_of_items):
        This function is the number of trips we want to create, get the last ID generated for the customer and the last
        ID generated for the car as input.
        This function chose random customer and random vehicle by generate random ids in there range then
        it uses create_trip_start_time to generate random start trip time
        Start trip time is less than vehicle last seen time.



    This script required 'Pandas' library.
"""

import datetime
import os
import random

import pandas as pd

import customer_generator
import helper_functions
import payment_generator
import trip_generator
import vehicle_generator
from helper_functions import generate_id, convert_string_datetime_to_datetime, choice_status_weight, \
    create_trip_start_time


def generate_transaction_time_id(start_trip_time, end_trip_time):
    transaction_id = payment_generator.generate_transaction_id()
    trip_start_time = convert_string_datetime_to_datetime(start_trip_time)
    trip_end_time = convert_string_datetime_to_datetime(end_trip_time)

    transaction_time = helper_functions.generate_date_time_between(trip_start_time, trip_end_time)
    return transaction_id, transaction_time


def create_fake_vehicle_information(number_of_items):
    """
    This function get number of cars and then create random information about each of them.

    Parameters:
    ----------
    number_of_items: int
        Number of total cars we want to create information about them.

    Returns:
    --------
    Pandas DataFrame
        A DataFrame contains information about cars.
    """
    item_list = []

    vehicle_status = choice_status_weight(vehicle_generator.VEHICLE_STATUS, [35, 30, 35], number_of_items)

    for i in range(number_of_items):
        item_list.append(vehicle_generator.generate_vehicle_info_dict(i + 1, vehicle_status[i]))

    df_vehicle = pd.DataFrame(item_list)
    # df_vehicle["last_service"] = pd.to_datetime(df_vehicle["last_service"], format='%Y-%m-%d %H:%M:%S')
    # df_vehicle["last_time"] = pd.to_datetime(df_vehicle["last_time"], format='%Y-%m-%d %H:%M:%S')
    return df_vehicle


def create_fake_customer_information(number_of_items):
    """
    This function can receive generate_customer_info_dict or generate_vehicle_info_dict
    functions and generate a Pandas DataFrame.

    Parameters
    ----------
    number_of_items : int
        Total number of information we want to create.

    Returns
    -------
    Pandas DataFrame
        A DataFrame contains information about customers.
    """

    item_list = []

    for i in range(number_of_items):
        item_list.append(customer_generator.generate_customer_info_dict(i + 1))

    df_customer = pd.DataFrame(item_list)
    # Pandas do not know the format datetime.date, so it saved as a panda object (str)
    df_customer["date_of_birth"] = pd.to_datetime(df_customer["date_of_birth"], format='%Y-%m-%d %H:%M:%S')
    # df_customer["join_date"] = pd.to_datetime(df_customer["join_date"], format='%Y-%m-%d %H:%M:%S')
    return df_customer


def create_fake_trip(number_of_trips, customer_max_id, vehicle_max_id):
    """
    This function creates a Pandas DataFrame for trip information.
    It generates random customer and vehicle id to simulation of a real word situation.

    VEHICLE_STATUS = ['Busy', 'UnderRepair', 'Vacant'] respectively index [0, 1, 2]
    TRIP_STATUS = ['Start', 'End', 'Cancel'] respectively wight [25, 65, 10]

    Parameters
    ---------
    number_of_trips : int
        Total number of information we want to create.
    customer_max_id : int
        Maximum id number for customer.
    vehicle_max_id : int
        Maximum id number for vehicle.

    Returns
    -------
    Pandas Dataframe
    """

    trip_list = []
    trip_status = choice_status_weight(trip_generator.TRIP_STATUS, [20, 60, 20], number_of_trips)

    df_customer = pd.read_csv("csv/customer_info.csv")
    df_vehicle = pd.read_csv("csv/vehicle_info.csv")
    df_vehicle = df_vehicle[["vehicle_id", "status", "last_time"]]
    # TODO some Busy status in trip table have status End or cancel
    for i in range(number_of_trips):
        # Generate random id for customer and vehicle.
        random_customer_id = generate_id(1, customer_max_id)
        random_vehicle_id = generate_id(1, vehicle_max_id)
        # if trip status == start
        if trip_status[i] == trip_generator.TRIP_STATUS[0]:

            # Now datatime
            start_trip_time = (datetime.datetime.now())
            start_trip_time = start_trip_time - datetime.timedelta(hours=random.choice([1, 2, 3]))

            start_datetime = helper_functions.generate_random_time_between(start_trip_time, datetime.datetime.now())

        else:
            # Create start trip date time
            start_datetime = create_trip_start_time(df_vehicle, random_vehicle_id, df_customer, random_customer_id)


        # Generate fake trip information.
        trip_list.append(trip_generator.generate_trip_info_dict(i + 1,
                                                                random_customer_id,
                                                                random_vehicle_id,
                                                                i + 1,
                                                                start_datetime,
                                                                trip_status[i]))

    return trip_list


def add_extra_trips(number_of_trips, customer_max_id, vehicle_max_id):
    trip_list = []

    original_trip_list = create_fake_trip(number_of_trips, customer_max_id, vehicle_max_id)
    last_payment_id = original_trip_list[-1]["trip_id"]  # Get last generated id

    df_vehicle = pd.read_csv("csv/vehicle_info.csv")
    df_vehicle = df_vehicle[["vehicle_id", "status", "last_time"]]
    vehicle_busy_status = df_vehicle[df_vehicle["status"] == vehicle_generator.VEHICLE_STATUS[0]].values.tolist()

    counter = 1
    for i in vehicle_busy_status:
        # Generate random id for customer and vehicle.
        random_customer_id = generate_id(1, customer_max_id)
        random_vehicle_id = i[0]

        start_trip_time = (datetime.datetime.now())
        start_trip_time = start_trip_time - datetime.timedelta(hours=random.choice([1, 2, 3]))
        start_datetime = helper_functions.generate_random_time_between(start_trip_time, datetime.datetime.now())

        trip_list.append(trip_generator.generate_trip_info_dict(last_payment_id + counter,
                                                                random_customer_id,
                                                                random_vehicle_id,
                                                                last_payment_id + counter,
                                                                start_datetime,
                                                                trip_generator.TRIP_STATUS[0]))
        counter += 1

    trip_list = original_trip_list + trip_list

    df_trip = pd.DataFrame(trip_list)
    # df_trip["start_trip_time"] = pd.to_datetime(df_trip["start_trip_time"], format='%Y-%m-%d %H:%M:%S')
    # df_trip["end_trip_time"] = pd.to_datetime(df_trip["end_trip_time"], format='%Y-%m-%d %H:%M:%S')

    return df_trip


def create_fake_payment():
    """
    This function use trip data to generate fake information about payments.
    This function uses trip_end_time to generate estimation of transaction time.

    Trip_info.csv items we need:
        item[0] = trip status,          item[3] = payment id
        item[1] = trip start date-time, item[4] = customer id
        item[2] = trip end date-time,   item[5] = trip amount
        item[6] = start latitude,       item[7] = start longitude
        item[8] = end latitude,         item[9] = end longitude

    Parameters
    ----------
    trip_data : Pandas DataFrame
        A Pandas DataFrame which contains all information about trip.
        This function check customer join date and generate
    Returns
    -------
    Pandas DataFrame
    """

    payment_list = []
    trip_dataframe = pd.read_csv("csv/trip_info.csv")
    trip_sub_list = trip_dataframe[
        ["status", "start_trip_time", "end_trip_time", "payment_id", "customer_id", "amount", "start_latitude_trip",
         "start_longitude_trip", "end_latitude_trip", "end_longitude_trip"]].values.tolist()

    for item in trip_sub_list:
        if item[0] == "End":
            transaction_id, transaction_time = generate_transaction_time_id(item[1], item[2])
            payment_list.append(payment_generator.generate_payment_info_dict(
                item[3], item[4], item[5], payment_generator.PAYMENT_STATUS[0], transaction_id, transaction_time
            ))
        elif item[0] == "Start":
            start_time = convert_string_datetime_to_datetime(item[1])
            estimate_distance, start_trip_time, end_trip_time, estimate_amount = helper_functions.generate_date_and_amount(
                (item[6], item[7]), (item[8], item[9]), start_time)

            transaction_id, transaction_time = generate_transaction_time_id(item[1], str(end_trip_time))
            payment_list.append(payment_generator.generate_payment_info_dict(
                item[3], item[4], item[5], payment_generator.PAYMENT_STATUS[1], transaction_id, transaction_time
            ))
        elif item[0] == "Cancel":
            transaction_id, transaction_time = generate_transaction_time_id(item[1], item[2])
            payment_list.append(payment_generator.generate_payment_info_dict(
                item[3], item[4], item[5], payment_generator.PAYMENT_STATUS[1], transaction_id, transaction_time
            ))

    df_payment = pd.DataFrame(payment_list)
    df_payment["transaction_time"] = pd.to_datetime(df_payment["transaction_time"], format='%Y-%m-%d %H:%M:%S')

    return df_payment


if __name__ == "__main__":
    print("Start generate fake information, please wait ...")

    if not os.path.exists("csv"):
        os.makedirs("csv")
        print("csv directory created!")

    # Generate 100 customer, 50 vehicles and 200 trip fake data.
    customer_data_frame = create_fake_customer_information(100)
    customer_data_frame.to_csv("csv/customer_info.csv", index=False)
    print("Customer information created!")
    vehicle_data_frame = create_fake_vehicle_information(50)
    vehicle_data_frame.to_csv("csv/vehicle_info.csv", index=False)
    print("Vehicle information created!")
    trip_data_frame = add_extra_trips(200, 100, 50)
    trip_data_frame.to_csv("csv/trip_info.csv", index=False)
    print("Trip information created!")

    # Load trip CSV and create payment DataFrame based on information

    payment_data_frame = create_fake_payment()
    payment_data_frame.to_csv("csv/payment_info.csv", index=False)
    print("Payment information created!")

    trip_info_s = trip_data_frame[
        ['trip_id', 'customer_id', 'vehicle_id', 'payment_id', 'start_latitude_trip', 'start_longitude_trip',
         'end_latitude_trip',
         'end_longitude_trip', 'start_trip_time', 'end_trip_time', 'amount', 'status']]

    trip_info_s.to_csv("csv/trip_info_psql.csv", index=False)

    print("Done!")
