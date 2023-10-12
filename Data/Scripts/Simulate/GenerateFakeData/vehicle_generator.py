"""
    This script generates fake vehicle information using 'fake' Python library.
    It creates model, make, cat, status, latitude, longitude, and time.

    We used the Fake Library and Fake Vehicle Library to create the car.
    Fake vehicles randomly generate vehicle Model and Make.
    Fake Library generates random date time in the current month for last_time_seen variable.
    unique.license_plate() from Fake used to generate unique license plate for each vehicle.
    geopy used to generate random latitude and longitude position of each car.
    Last service time generates between current datetime and -4 years ago by Fake

    Dependencies:
        - fake library (install using 'pip install fake')
"""
from faker import Faker
from faker_vehicle import VehicleProvider
import uuid
from GenerateFakeData.helper_functions import generate_location, generate_date_time

fake_vehicle = Faker("en_UK")
fake_vehicle.add_provider(VehicleProvider)

VEHICLE_STATUS = ['Busy', 'UnderRepair', 'Vacant']


def generate_vehicle() -> tuple:
    """
    This function creates model, make, cat, and model_make

    Returns
    -------
    tuple
        A tuple contain model_make, make, model, and cat
    """

    make = fake_vehicle.vehicle_make()
    # BMW
    model = fake_vehicle.vehicle_model()
    # SL

    return make, model


def generate_vehicle_info_dict(vehicle_id: uuid, vehicle_status: str) -> dict:
    """
    This function creates a dictionary of vehicle information

    Parameters
    -----------
    vehicle_id: uuid
        An id generated for each vehicle (PRIMARY KEY)
    vehicle_status: str
        Current state of vehicle.

    Returns
    -------
     Paython dictionary
        A dictionary contain vehicle information.

    """

    vehicle_make, vehicle_model = generate_vehicle()
    last_time_seen = fake_vehicle.date_time_this_month()
    fake_license = fake_vehicle.unique.license_plate()
    last_seen_lat, last_seen_long, _ = generate_location()

    last_service = generate_date_time("-4y", "now")

    return {
        "VehicleId": vehicle_id,
        "LicensePlate": fake_license,
        "Status": vehicle_status,
        "LastService": last_service,
        "Latitude": last_seen_lat,
        "Longitude": last_seen_long,
        "Model": vehicle_model,
        "Make": vehicle_make,
        "LastTime": last_time_seen
    }


if __name__ == "__main__":
    vehicle = generate_vehicle_info_dict(5, VEHICLE_STATUS[1])
