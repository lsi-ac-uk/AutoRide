"""
    This script contains queries to create our Postgresql tables
    and their column name.
    There are four tables, Customer, Vehicle, Trip, and Payment Tables include ENUMs
    Vehicle status, Trip status, and Payment Status

"""

CREATE_DATABASE = "CREATE DATABASE AutoRide;"

table_columns = {
    "customer_info.csv": "Id, FirstName, LastName, DateOfBirth, Email, Phone, Address, ZipCode, JoinDate",
    "vehicle_info.csv": "Id, LicensePlate, VehicleStatus, LastService, Latitude, Longitude, Model, Make, LastTime",
    "payment_info.csv": "Id, CustomerId, Amount, TransactionId, TransactionTime, Status",
    "trip_info_psql.csv": "Id, CustomerId, VehicleId, PaymentId, StartLatitude, StartLongitude, EndLatitude, EndLongitude, RequestTripTime, StartTripTime, EndTripTime, Amount, Status"

}

tables_query = {
    "Customer": """
    CREATE TABLE IF NOT EXISTS customer(
        Id UUID PRIMARY KEY NOT NULL,
        FirstName VARCHAR(30) NOT NULL,
        LastName VARCHAR(30) NOT NULL,
        DateOfBirth DATE, 
        Email VARCHAR(50),
        Phone VARCHAR(30),
        Address VARCHAR(400),
        ZipCode VARCHAR(30) NOT NULL,
        JoinDate TIMESTAMP);
    """,
    "Vehicle": """
    CREATE TABLE IF NOT EXISTS Vehicle(
        Id UUID PRIMARY KEY NOT NULL,
        LicensePlate VARCHAR(20) NOT NULL,
        VehicleStatus VehicleStatus NOT NULL,
        LastService TIMESTAMP,
        Latitude FLOAT,
        Longitude FLOAT,
        Model VARCHAR(50),
        Make VARCHAR(50),
        LastTime TIMESTAMP);
        """,
    "Payment": """
    CREATE TABLE IF NOT EXISTS payment(
        Id UUID PRIMARY KEY NOT NULL,
        CustomerId UUID REFERENCES customer(Id) NOT NULL,
        Amount FLOAT,
        TransactionId VARCHAR(200),
        TransactionTime TIMESTAMP DEFAULT NULL,
        Status PaymentStatus NOT NULL);
    """,
    "Trip": """
    CREATE TABLE IF NOT EXISTS trip(
        Id UUID PRIMARY KEY NOT NULL,
        CustomerId UUID REFERENCES customer(Id) NOT NULL,
        VehicleId UUID REFERENCES vehicle(Id) NOT NULL,
        PaymentId UUID REFERENCES payment (Id),
        StartLatitude FLOAT NOT NULL,
        StartLongitude FLOAT NOT NULL,
        EndLatitude FLOAT,
        EndLongitude FLOAT,
        RequestTripTime TIMESTAMP, 
        StartTripTime TIMESTAMP,
        EndTripTime TIMESTAMP DEFAULT NULL,
        Amount FLOAT,
        Status TripStatus NOT NULL);
    """
}

enums_query = {
    "TripStatus": """
    CREATE TYPE TripStatus AS ENUM(
        'Started', 'Completed', 'Canceled');
    """,
    "VehicleStatus": """
    CREATE TYPE VehicleStatus AS ENUM(
        'Busy', 'UnderRepair', 'Vacant');
    """,
    "PaymentStatus": """ 
    CREATE TYPE PaymentStatus AS ENUM(
        'Successful');
    """
}

