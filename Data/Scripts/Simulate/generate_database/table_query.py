CUSTOMER_COLUMNS = "FirstName, LastName, DateOfBirth, Email, Phone, Address, ZipCode, JoinDate"
VEHICLE_COLUMNS = "LicensePlate, VehicleStatus, LastService, Latitude, Longitude, Model, Make, LastTime"
TRIP_COLUMNS = "CustomerId, VehicleId, PaymentId, StartLatitude, StartLongitude, EndLatitude, EndLongitude, StartTripTime, EndTripTime, Amount, Status"
PAYMENT_COLUMNS = "CustomerId, Amount, TransactionId, TransactionTime, Status"

CREATE_DATABASE = "CREATE DATABASE AutoRide;"

CREATE_CUSTOMER_TABLE = """
    CREATE TABLE IF NOT EXISTS customer(
        Id SERIAL PRIMARY KEY NOT NULL,
        FirstName VARCHAR(30) NOT NULL,
        LastName VARCHAR(30) NOT NULL,
        DateOfBirth DATE, 
        Email VARCHAR(50),
        Phone VARCHAR(30),
        Address VARCHAR(400),
        ZipCode VARCHAR(30) NOT NULL,
        JoinDate TIMESTAMP);
"""

CREATE_VEHICLE_TABLE = """
    CREATE TABLE IF NOT EXISTS Vehicle(
        Id SERIAL PRIMARY KEY NOT NULL,
        LicensePlate VARCHAR(20) NOT NULL,
        VehicleStatus VehicleStatus NOT NULL,
        LastService TIMESTAMP,
        Latitude FLOAT,
        Longitude FLOAT,
        Model VARCHAR(50),
        Make VARCHAR(50),
        LastTime TIMESTAMP);
        """

CREATE_TRIP_TABLE = """
    CREATE TABLE IF NOT EXISTS trip(
        Id SERIAL PRIMARY KEY NOT NULL,
        CustomerId INTEGER REFERENCES customer(Id) NOT NULL,
        VehicleId INTEGER REFERENCES vehicle(Id) NOT NULL,
        PaymentId INTEGER REFERENCES payment (Id),
        StartLatitude FLOAT NOT NULL,
        StartLongitude FLOAT NOT NULL,
        EndLatitude FLOAT,
        EndLongitude FLOAT,
        StartTripTime TIMESTAMP,
        EndTripTime TIMESTAMP DEFAULT NULL,
        Amount FLOAT,
        Status TripStatus NOT NULL);
"""

CREATE_PAYMENT_TABLE = """
    CREATE TABLE IF NOT EXISTS payment(
        Id SERIAL PRIMARY KEY NOT NULL,
        CustomerId INTEGER REFERENCES customer(Id) NOT NULL,
        Amount FLOAT,
        TransactionId VARCHAR(200),
        TransactionTime TIMESTAMP DEFAULT NULL,
        Status PaymentStatus NOT NULL);
    """

CREATE_ENUM_TRIP_STATUS = """
    CREATE TYPE TripStatus AS ENUM(
        'Start', 'End', 'Cancel');
"""

CREATE_ENUM_VEHICLE_STATUS = """
    CREATE TYPE VehicleStatus AS ENUM(
        'Busy', 'UnderRepair', 'Vacant');
"""

CREATE_ENUM_PAYMENT_STATUS = """ 
    CREATE TYPE PaymentStatus AS ENUM(
        'Successful', 'Unsuccessful');

"""
