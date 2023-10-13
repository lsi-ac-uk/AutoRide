# AutoRide - Script/Simulate

## Table of Contents
- [🌟 Introduction](#introduction)
- [📁 CreateMongodb](#createmongodb)
- [📁 CreatePostgresql](#createposgresql)
- [📁 GenerateFakeData](#generatefakedata)
- [📁 main.py](#main.py)
- [🚀 run.bat](#run.bat)

---

## 🌟 Introduction

### Script/Simulate 
This folder includes codes for generating fake data and databases Postgresql and Mongodb.
To run this program, download your contents and run the run.bat file.
Before running the run.bat file, ensure that Python, Postgresql, and MongoDB are installed on your computer or laptop.


<<<<<<< HEAD
## 🚀 Features

- **User Authentication**: Secure authentication and authorization for riders and drivers.
- **Real-Time Tracking**: Track the location of your ride in Real-time using GPS.
- **Ride Booking**: Users can easily book a ride with just a few clicks.
- **Driver Matching**: Efficient algorithm to match riders with nearby available drivers.
- **Payment Integration**: Seamless integration with popular payment gateways for secure transactions.
- **Reviews and Ratings**: Users can rate and review their rides, enhancing trust and transparency.
- **Admin Dashboard**: An admin panel to manage users, rides, and monitor platform activity.
- **Multi-Platform Support**: Web and mobile apps for both Android and iOS.


## 📁 Folder Structure

- **Data**: Contains database-related files.
  - **CSV**: CSV files for importing/exporting data.
  - **Schema**:  Database schema and structure files.
  - **Scripts**: Scripts for database setup.
  
- **Src/dotnet**: This folder contains the backend server built with the .NET framework.
  It includes controllers, models, services, and other components necessary to run the server.
  - **API**:
  - **Domain**: Contain C# classes.
  - **UI/Blazor**: Blazor UI components for the frontend
    - **Admin**: Admin user interface
    -  **EndUser**: User interface


## 🖼️ UML Diagrams

### Use Case Diagram
A Use Case Diagram is a visual representation in the Unified Modeling Language (UML) that illustrate the various
interaction between users (actors) and a system. It provides a high-level view of the functionalities a system 
offers and the actors involved in using those functionalities.

#### AutoRide Use Case Diagram
The Use Case Diagram for the AutoRide Online Cab Sharing Platform illustrates the interactions 
between three key actors: The customer, the Self-Driving Car, and the Platform.

* Customer: Represents the end-user of the platform who initiates ride requests. The customer
  interacts with the system through actions such as logging into the app, selecting their origin
  and destination, and sending a ride request.
* Self-Driving Car: Represent the autonomous vehicles within the platform's fleet. The self-driving car
  interacts with the system by performing actions like contacting the passenger to confirm the ride, starting
  and ending the trip, and handling payment processing.
* Platform: Serves as the central intelligence of the cab-sharing ecosystem. It's responsible for analyzing ride requests,
  dispatching orders to available cars, and managing the allocation of cars to specific rides.



<img src="https://docs.google.com/drawings/d/e/2PACX-1vQONHzYOF_zcqDKKBPZMNkr9dGVi-ymSeeFNniDWwpr3iUkxV3-uOK4VSrfkRfdn5Is5JIqdX1unJAf/pub?w=960&amp;h=720">


### Class Diagram
A class Diagram is a visual representation in the Unified Modeling Language (UML) that provides a structural view of
a system. it depicts the classes, their attributes, methods, and the relationships between them.

In a Class Diagram:
* Classes: Represent the objects or entities in the system. They encapsulate data (attributes)
  and behavior (methods) related to those entities.
* Attributes: Describe the properties or characteristics of a class. They define what data a class holds.
* Methods: Specify the actions or behaviors that a class can perform. They define the operations
  that can be applied to the class.
* Relationships: Illustrate how classes are connected or related to one another. These
  relationships include associations, dependencies, inheritances, and more.

Class Diagrams are invaluable for modeling the structure of a system, providing a blueprint
for developers to understand the relationships and responsibilities of different classes.
They serve as a communication tool for stakeholders to visualize the system's architecture, 
aiding in system design and development.

#### AutoRide Use Class Diagram
This project represents an application for managing customer data, trips,
payments, vehicles, and locations in a cab-sharing service.

- **Customer**: Represents a customer with attributes like ID, name, gender, and contact information.
- **Location**: Contains information about a specific geographical location, including its latitude and longitude.
- **Payment**: Manages payment details including amount, method, and status. Each payment is associated with a specific customer.
- **Trip**: Represents a trip made by a customer using a vehicle. It includes start and end locations, trip status, and associated payment information.
- **Vehicle**: Contains information about the Autonomous car such as status, last service, and last location.
- **VehicleBasicInformation**: Contains details about vehicles such as manufacturer, name, and type.

- **Enums**:
    - **Genders**: Represent the gender of a customer (Male, Female, Unknown).
    - **PaymentMethods**: Indicates the method used for payment (Cash, Credit, Online)
    - **PaymentStatus**: Describes the status of a payment (Successful, Unsuccessful, Cance, InProgress).
    - **TripStatus**: Represent the status of a trip (Started, Done, Canceled).
    - **VehicleStatus**: Indicates the status of a vehicle (UnderRepair, Vacant, Full, OutOfOrder)
    - **VehicleTypes**: Specifies the type of vehicles (Sedan, SUV, CrossOver, Hatchback, Minivan, Van)
 
This class diagram serves as a visual guide for understanding the relationships between the various components of the AutoCar application.
For a detailed explanation of each class and their respective properties and methods, refer to the code files in the repository.

![Example Image](https://drive.google.com/uc?id=1at64tKIARZebT_NMX0lGB1zW0i_7DYXZ)

To get started with <YourCompany>, follow these steps:

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/<YourUsername>/<YourRepository>.git


## 🔧 Usage
## Contributing
## License

=======
## 📁 CreateMongodb

- **create_mongodb.py**: This script contains functions and classes to create MongoDB Collection and Documents.
    mongoengine library is used to connect to the MongoDB.
    - **Classes to create document schema:**
      - Customer
      - Vehicle
      - Trip
      - Payment
    - **Functions to create collections and documents and fill them with fake data:**
      - customer_fill_data
      - vehicle_fill_data
      - trip_fill_data
      - payment_fill_data
      - create_and_fill_mongo
  
## 📁 CreatePostgresql
This folder contains Python files to create Postgresql database and tables. Also, fill the tables with fake data.

  - **config.py**: Retun database information.
  - **table_query.py**: It contains queries to create database tables.
  - **database.ini**: It contains database information to connect to it.
  - **create_postgresql**: It contains functions to open and close the connection and create and fill the tables with fake data.

## 📁 GenerateFakeData  
This folder contains Python files to generate fake data and create CSV files.
  
  - **customer_generator.py**: It contains functions to generate customer fake data.
  - **fake_data_generator.py**: Using other functions to generate fake data and save them as CSV.
  - **helper_function.py**: It contains functions to help generate fake data.
  - **payment_generator.py**: It contains functions to generate payment fake data.
  - **trip_generator.py**: It contains functions to generate trip fake data.
  - **vehicle_generator.py**: It contains functions to generate vehicle fake data.
  
## 📁 main.py
This file is responsible for communication and receiving input from the user. 
Also, at the request of the user, it executes the functions required to build the database and generate fake data.

## 🚀 run.bat
This file executes the main.py. Users just need to run this file.





>>>>>>> 91951151e9e567eec9b308a91d5cf803bc346249

