import datetime

from mongoengine import StringField, connect, DateTimeField, EmailField, SequenceField, ListField
from mongoengine import register_connection, Document

# connect('mongoennTest')


VEHICLE_STATUS = ('Busy', 'UnderRepair', 'Vacant')


def connection():
    register_connection(alias="autoride", name="AutoRideTest")


class Customer(Document):
    id = SequenceField(primary_key=True)
    FirstName = StringField(required=True)
    LastName = StringField(required=True)
    DateOfBirth = DateTimeField(default=datetime.datetime.now)
    Email = EmailField(default="test@gmail.com")
    Phone = StringField(default="06589745")
    Address = StringField(default="water spring, b34, London, UK")
    ZipCode = StringField(required=True)
    JoinDate = DateTimeField(default=datetime.datetime.now)


class Vehicle(Document):
    Id = SequenceField(primary_key=True)
    LicensePlate = StringField(required=True)
    VehicleStatus = StringField(choices=VEHICLE_STATUS)
    LastService = DateTimeField(default=datetime.datetime.now)
    coordinates = ListField()
    Model = StringField()
    Make = StringField()
    LastTime = DateTimeField(default=datetime.datetime.now)


if __name__ == "__main__":
    # Update examples
    # customer = Customer.objects(email="test@gmail.com")
    # customer.update(first_name="Bahare")
    #
    # customer_two = Customer.objects(email="test@gmail.com")
    # update_fields = {
    #     "first_name": "Hello",
    #     "last_name": "Goodbye"
    # }
    # customer_two.update(**update_fields)
    connect('AutoRideTest')

    # cutomer = Customer(FirstName="Bahare",
    #                   LastName="Sadeghi",
    #                   DateOfBirth=datetime.datetime.now(),
    #                   Email="bahara.cake@gmail.com",
    #                   Address="I don't know what an i what now!",
    #                   ZipCode="7789996",
    #                   JoinDate=datetime.datetime.now())
    # cutomer.save()

    vehicle = Vehicle(
        LicensePlate="86416fdsf",
        VehicleStatus="Busy",
        LastService=datetime.datetime.now(),
        coordinates=[-562852, -8001],
        Model="m2",
        Make="bmw",
        LastTime=datetime.datetime.now())

    vehicle.save()
