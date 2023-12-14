import datetime
import uuid

import pandas as pd
from mongoengine import Document
from mongoengine import StringField, connect, DateTimeField, FloatField, ListField, UUIDField
from rich.console import Console, Theme

# TODO add required for customer name and family

VEHICLE_STATUS = ('Busy', 'UnderRepair', 'Vacant')
TRIP_STATUS = ('Started', 'Completed', 'Canceled')
PAYMENT_STATUS = ('Successful',)

custom_theme = Theme({"success": "green", "error": "red", "msg": "cyan"})
console = Console(theme=custom_theme)


def is_uuid(item) -> bool:
    """
    Returns True if the item is a UUID, False otherwise.

    Parameters
    ----------
    item: uuid | nan
    """

    try:
        uuid.UUID(item)
        return True
    except:
        return False


class EmptyDocument(Document):
    id = UUIDField(primary_key=True, binary=False)
    FirstName = StringField(required=True)
    LastName = StringField(required=True)
    DateOfBirth = DateTimeField()
    Email = StringField()
    Phone = StringField()
    Address = StringField()
    ZipCode = StringField()
    JoinDate = DateTimeField()


class Customer(Document):
    """
    Schema of a customer document in AutoRide collection
    """
    id = UUIDField(primary_key=True, binary=False, default=lambda: uuid.uuid4())
    FirstName = StringField()
    LastName = StringField()
    DateOfBirth = DateTimeField()
    Email = StringField()
    Phone = StringField()
    Address = StringField()
    ZipCode = StringField()
    JoinDate = DateTimeField()


class Vehicle(Document):
    """
        Schema of a vehicle document in AutoRide collection
    """
    Id = UUIDField(primary_key=True, binary=False)
    LicensePlate = StringField(required=True)
    VehicleStatus = StringField(choices=VEHICLE_STATUS)
    LastService = DateTimeField(default=datetime.datetime.now)
    coordinates = ListField()
    Model = StringField()
    Make = StringField()
    LastTime = DateTimeField(default=datetime.datetime.now)


class Trip(Document):
    """
        Schema of a trip document in AutoRide collection
    """
    Id = UUIDField(primary_key=True, binary=False)
    CustomerId = UUIDField(binary=False)
    VehicleId = UUIDField(binary=False)
    PaymentId = UUIDField(binary=False)
    StartTripLocation = ListField()
    EndTripLocation = ListField()
    StartTripTime = DateTimeField()
    RequestTripTime = DateTimeField()
    EndTripTime = StringField()
    Amount = FloatField()
    TripStatus = StringField(choices=TRIP_STATUS)


class Payment(Document):
    """
        Schema of a payment document in AutoRide collection
    """
    Id = UUIDField(primary_key=True, binary=False)
    CustomerId = UUIDField(binary=False)
    Amount = FloatField()
    TransactionId = StringField()
    TransactionTime = DateTimeField()
    Status = StringField(choices=PAYMENT_STATUS)


def customer_fill_data():
    """
    This function load customer information
    from csv file, then create and fill the data on the
    customer document.

    """
    try:
        df_customer = pd.read_csv("csv/customer_info.csv")
        customer_list = df_customer.values.tolist()

        for customer in customer_list:
            customer_doc = Customer(
                id=customer[0],
                FirstName=customer[1],
                LastName=customer[2],
                DateOfBirth=customer[3],
                Email=customer[4],
                Phone=customer[5],
                Address=customer[6],
                ZipCode=customer[7],
                JoinDate=customer[8])

            customer_doc.save()
        console.print("Customer document created successfully", style="success")
    except Exception as e:
        console.print(f"Error creating and saving Customer documents: {e}", style="error")


def vehicle_fill_data():
    """
        This function load vehicle information
        from csv file, then create and fill the data on the
        vehicle document.

    """
    try:
        df_vehicle = pd.read_csv("csv/vehicle_info.csv")
        vehicle_list = df_vehicle.values.tolist()

        for vehicle in vehicle_list:
            vehicle_doc = Vehicle(
                id=vehicle[0],
                LicensePlate=vehicle[1],
                VehicleStatus=vehicle[2],
                LastService=vehicle[3],
                coordinates=[vehicle[4], vehicle[5]],
                Model=vehicle[6],
                Make=vehicle[7],
                LastTime=vehicle[8])

            vehicle_doc.save()
        console.print("Vehicle document created successfully", style="success")
    except Exception as e:
        console.print(f"Error creating and saving Vehicle documents: {e}", style="error")


def payment_fill_data():
    """
        This function load payment information
        from csv file, then create and fill the data on the
        payment document.

    """
    try:
        df_payment = pd.read_csv("csv/payment_info.csv")
        payment_list = df_payment.values.tolist()

        for payment in payment_list:
            payment_doc = Payment(
                Id=payment[0],
                CustomerId=payment[1],
                Amount=payment[2],
                TransactionId=payment[3],
                TransactionTime=payment[4],
                Status=payment[5])

            payment_doc.save()
        console.print("Payment document created successfully", style="success")
    except Exception as e:
        print(f"Error creating and saving Payment documents: {e}")


def trip_fill_data():
    """
        This function load trip information
        from csv file, then create and fill the data on the
        trip document.
    """
    try:
        df_trip = pd.read_csv("csv/trip_info_psql.csv")
        trip_list = df_trip.values.tolist()

        for trip in trip_list:

            if is_uuid(trip[3]):
                trip_doc = Trip(
                    Id=trip[0],
                    CustomerId=trip[1],
                    VehicleId=trip[2],
                    PaymentId=trip[3],
                    StartTripLocation=[trip[4], trip[5]],
                    EndTripLocation=[trip[6], trip[7]],
                    StartTripTime=trip[8],
                    RequestTripTime=trip[9],
                    EndTripTime=str(trip[10]),
                    Amount=trip[11],
                    TripStatus=trip[12])
            else:
                trip_doc = Trip(
                    Id=trip[0],
                    CustomerId=trip[1],
                    VehicleId=trip[2],
                    StartTripLocation=[trip[4], trip[5]],
                    EndTripLocation=[trip[6], trip[7]],
                    StartTripTime=trip[8],
                    RequestTripTime=trip[9],
                    EndTripTime=str(trip[10]),
                    Amount=trip[11],
                    TripStatus=trip[12])

            trip_doc.save()
        console.print("Trip document created successfully", style="success")
    except Exception as e:
        console.print(f"Error creating and saving Customer documents: {e}", style="error")


def create_empty_doc():
    connect('autoride')
    empty_customer = Customer()

    # Save the empty document to the database
    try:
        empty_customer.save()
        console.print("Empty customer document created and saved successfully.", style="success")
    except Exception as e:
        console.print(f"Error saving empty customer document: {e}", style="error")


def create_and_fill_mongo():
    try:
        connect('autoride')
        console.print("Connected to MongoDB successfully.", style="success")
    except Exception as e:
        console.print(f"Error connecting to MongoDB: {e}", style="error")
        # Handle the error appropriately (e.g., log the error, exit the program, etc.)

        # Insert a document
    customer_fill_data()
    vehicle_fill_data()
    payment_fill_data()
    trip_fill_data()
    # Query the database


if __name__ == "__main__":
    create_and_fill_mongo()
