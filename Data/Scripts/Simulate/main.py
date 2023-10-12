from GenerateFakeData import fake_data_generator as fkgn
from CreatePostgresql.create_postgresql import create_and_fill_postgresql
from CreateMongodb.create_mongodb import create_and_fill_mongo
exit_msg = ""
print(f"Hello, this program help you to generate fake data and create your databases.\n"
      f"You can chose the number of Customers, Vehicles, and Trips\n"
      f"You can also create data with default values that we have provided.\n"
      f"The default values for each of the tables are as follows:\n"
      f"- Number of customers: 100\n"
      f"- Number of vehicles: 50\n"
      f"- Number of trips: 200\n")

print("Please select one option:\n"
      "1- Modify default parameters and generate fake data.\n"
      "2- Generate fake data with default parameters.\n"
      "3- Create Postgresql database.\n"
      "4- Create Mongodb database.\n")

while True:

    user_msg = input("Please chose one option:\n")

    if user_msg.casefold() == "quit":
        break
    if user_msg.isnumeric():
        if int(user_msg) == 1:
            print("Modify default parameters and generate fake data")

        elif int(user_msg) == 2:
            fkgn.start_fake_data_generation()

        elif int(user_msg) == 3:
            create_and_fill_postgresql()

        elif int(user_msg) == 4:
            create_and_fill_mongo()

        else:
            print("Please select one option.")
    else:
        print("Please enter valid number.")
