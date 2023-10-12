# TODO Use UUID, trip and payment
# TODO Add request time for trip
# TODO Change the name of csv columns
# TODO Edit transaction code style.
# TODO Review the code and Docstrings
# TODO Modify code for generate Postgresql
# TODO complete the Mongodb Database generator
# TODO check file and databases
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
import uuid

import numpy
import pandas as pd

from GenerateFakeData import customer_generator
from GenerateFakeData import payment_generator
from GenerateFakeData import trip_generator
from GenerateFakeData import vehicle_generator
from GenerateFakeData.helper_functions import convert_string_datetime_to_datetime, choice_status_weight, \
    create_trip_start_time, generate_transaction_time, generate_random_time_between, generate_date_and_amount, generate_random_time_between


def create_fake_vehicle_information(number_of_items: int) -> pd.DataFrame:
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
        item_list.append(vehicle_generator.generate_vehicle_info_dict(uuid.uuid4(), vehicle_status[i]))

    df_vehicle = pd.DataFrame(item_list)

    return df_vehicle


def create_fake_customer_information(number_of_items: int) -> pd.DataFrame:
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
        item_list.append(customer_generator.generate_customer_info_dict(uuid.uuid4()))

    df_customer = pd.DataFrame(item_list)
    # Pandas do not know the format datetime.date, so it saved as a panda object (str)
    df_customer["DateOfBirth"] = pd.to_datetime(df_customer["DateOfBirth"], format='%Y-%m-%d %H:%M:%S')

    return df_customer


def create_fake_trip(number_of_trips: int) -> list:
    """
    This function creates a list of trip information.
    It generates random customer and vehicle id to simulation of a real word situation.

    VEHICLE_STATUS = ['Busy', 'UnderRepair', 'Vacant'] respectively index [0, 1, 2]
    TRIP_STATUS = ['Started', 'Completed', 'Canceled'] respectively wight [25, 65, 10]

    Parameters
    ---------
    number_of_trips : int
        Total number of information we want to create.

    Returns
    -------
    list of trip information
    """

    trip_list = []
    trip_status = choice_status_weight(trip_generator.TRIP_STATUS, [20, 60, 20], number_of_trips)

    df_customer = pd.read_csv("csv/customer_info.csv")
    df_vehicle = pd.read_csv("csv/vehicle_info.csv")

    customer_id_list = df_customer["CustomerId"].values.tolist()
    vehicle_id_list = df_vehicle["VehicleId"].values.tolist()

    df_vehicle = df_vehicle[["VehicleId", "Status", "LastTime"]]

    for i in range(number_of_trips):
        payment_uuid = uuid.uuid4()
        # Generate random id for customer and vehicle.
        random_customer_id = random.choice(customer_id_list)
        random_vehicle_id = random.choice(vehicle_id_list)
        start_datetime = create_trip_start_time(df_vehicle, random_vehicle_id, df_customer, random_customer_id)
        # if trip status == started
        if trip_status[i] == trip_generator.TRIP_STATUS[0]:

            # Now datatime
            start_trip_time = (datetime.datetime.now())
            start_trip_time = start_trip_time - datetime.timedelta(hours=random.choice([1, 2, 3]))

            start_datetime = generate_random_time_between(start_trip_time, datetime.datetime.now())
        # create null value for canceled status
        elif trip_status[i] == trip_generator.TRIP_STATUS[2]:
            payment_uuid = numpy.NaN

        # Generate fake trip information.
        trip_list.append(trip_generator.generate_trip_info_dict(uuid.uuid4(),
                                                                random_customer_id,
                                                                random_vehicle_id,
                                                                payment_uuid,
                                                                start_datetime,
                                                                trip_status[i]))

    return trip_list


def add_extra_trips(number_of_trips: int) -> pd.DataFrame:
    trip_list = []

    original_trip_list = create_fake_trip(number_of_trips)

    df_customer = pd.read_csv("csv/customer_info.csv")
    customer_id_list = df_customer["CustomerId"].values.tolist()
    df_vehicle = pd.read_csv("csv/vehicle_info.csv")
    df_vehicle = df_vehicle[["VehicleId", "Status", "LastTime"]]
    vehicle_busy_status = df_vehicle[df_vehicle["Status"] == vehicle_generator.VEHICLE_STATUS[0]].values.tolist()

    for i in vehicle_busy_status:
        # Generate random id for customer and vehicle.
        random_customer_id = random.choice(customer_id_list)
        random_vehicle_id = i[0]

        start_trip_time = (datetime.datetime.now())
        start_trip_time = start_trip_time - datetime.timedelta(hours=random.choice([1, 2, 3]))
        start_datetime = generate_random_time_between(start_trip_time, datetime.datetime.now())

        trip_list.append(trip_generator.generate_trip_info_dict(uuid.uuid4(),
                                                                random_customer_id,
                                                                random_vehicle_id,
                                                                uuid.uuid4(),
                                                                start_datetime,
                                                                trip_generator.TRIP_STATUS[0]))

    trip_list = original_trip_list + trip_list

    df_trip = pd.DataFrame(trip_list)

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
        ["Status", "StartTripTime", "EndTripTime", "PaymentId", "CustomerId", "Amount", "StartLatitudeTrip",
         "StartLongitudeTrip", "EndLatitudeTrip", "EndLongitudeTrip"]].values.tolist()

    for item in trip_sub_list:
        if item[0] == trip_generator.TRIP_STATUS[1]:
            transaction_id = payment_generator.generate_transaction_id()
            transaction_time = generate_transaction_time(item[1], item[2])
            payment_list.append(payment_generator.generate_payment_info_dict(
                item[3], item[4], item[5], payment_generator.PAYMENT_STATUS[0], transaction_id, transaction_time
            ))
        elif item[0] == trip_generator.TRIP_STATUS[0]:
            start_time = convert_string_datetime_to_datetime(item[1])
            estimate_distance, start_trip_time, end_trip_time, estimate_amount = generate_date_and_amount(
                (item[6], item[7]), (item[8], item[9]), start_time)

            transaction_id = payment_generator.generate_transaction_id()
            transaction_time = generate_transaction_time(item[1], str(end_trip_time))

            payment_list.append(payment_generator.generate_payment_info_dict(
                item[3], item[4], item[5], payment_generator.PAYMENT_STATUS[0], transaction_id, transaction_time))
        # elif item[0] == "Canceled":
        #     transaction_id = payment_generator.generate_transaction_id()
        #     transaction_time = generate_transaction_time_id(item[1], item[2])
        #     payment_list.append(payment_generator.generate_payment_info_dict(
        #         item[3], item[4], item[5], payment_generator.PAYMENT_STATUS[1], transaction_id, transaction_time
        #     ))

    df_payment = pd.DataFrame(payment_list)
    df_payment["TransactionTime"] = pd.to_datetime(df_payment["TransactionTime"], format='%Y-%m-%d %H:%M:%S')

    return df_payment


def start_fake_data_generation(number_of_customer: int = 100,
                               number_of_vehicle: int = 50,
                               number_of_trip: int = 200):
    print("Start generate fake information, please wait ...")

    if not os.path.exists("csv"):
        os.makedirs("csv")
        print("csv directory created!")

    # Generate 100 customer, 50 vehicles and 200 trip fake data.
    # Generate customer fake data.
    customer_data_frame = create_fake_customer_information(number_of_customer)
    customer_data_frame.to_csv("csv/customer_info.csv", index=False)
    print("Customer information created!")

    # Generate vehicle fake data.
    vehicle_data_frame = create_fake_vehicle_information(number_of_vehicle)
    vehicle_data_frame.to_csv("csv/vehicle_info.csv", index=False)
    print("Vehicle information created!")

    # Generate trip fake data.
    trip_data_frame = add_extra_trips(number_of_trip)
    trip_data_frame.to_csv("csv/trip_info.csv", index=False)
    print("Trip information created!")

    # Load trip csv and create payment DataFrame based on information
    trip_data_frame = pd.read_csv("csv/trip_info.csv")
    payment_data_frame = create_fake_payment()
    payment_data_frame.to_csv("csv/payment_info.csv", index=False)
    print("Payment information created!")

    # Create csv for store in the database.
    trip_info_s = trip_data_frame[
        ['TripId', 'CustomerId', 'VehicleId', 'PaymentId', 'StartLatitudeTrip', 'StartLongitudeTrip',
         'EndLatitudeTrip', 'EndLongitudeTrip', 'RequestTripTime', 'StartTripTime', 'EndTripTime', 'Amount',
         'Status']]

    trip_info_s.to_csv("csv/trip_info_psql.csv", index=False)

    print("Done!")


if __name__ == "__main__":
    start_fake_data_generation()
