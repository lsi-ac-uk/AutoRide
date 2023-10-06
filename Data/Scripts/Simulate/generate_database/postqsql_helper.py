import numpy as np
import pandas as pd
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extensions import register_adapter, AsIs, Float

import table_query
from config import config

register_adapter(np.int64, AsIs)
register_adapter(float, lambda f: AsIs('NULL') if np.isnan(f) else Float(f))


def create_connection(config_name="postgresql"):
    try:
        db_params = config(section=config_name)
        print("Connecting to PostgreSQL...")
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        return connection, cursor
    except(Exception, psycopg2.DatabaseError) as err:
        print(err)
        return None, None


def close_connection(connection, cursor):
    if cursor is not None:
        cursor.close()
        print("Database cursor terminated!")

    if connection is not None:
        connection.close()
        print("Database connection terminated!")


def create_database():
    connection = psycopg2.connect(user="postgres", password="geeks", port=5433)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = connection.cursor()
    name_db = "AutoRide"
    create_query = "CREATE DATABASE " + name_db + ";"
    cursor.execute(create_query)


def create_db(config_name, db_name):
    print("create db ...")
    connection, cursor = create_connection(config_name)
    if connection is not None and cursor is not None:
        try:
            # Check if the database already exists
            connection.autocommit = True
            cursor = connection.cursor()
            cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
            exists = cursor.fetchone()

            if not exists:
                # If the database does not exist, create it
                cursor.execute("CREATE DATABASE {}".format(db_name))
                print("Creating AutoRide database id Done!\n")
        except(Exception, psycopg2.DatabaseError) as err:
            print(err)
        finally:
            close_connection(connection, cursor)


# def connect(config_name="postgresql"):
#     connection = None
#     try:
#         db_params = config(section=config_name)
#         print("Connecting to Postgresql...")
#         connection = psycopg2.connect(**db_params)
#         cursor = connection.cursor()
#
#         check_pgsql_version(cursor)
#
#         cursor.close()
#         print("Database cursor terminate!")
#     except(Exception, psycopg2.DatabaseError) as err:
#         print(err)
#     finally:
#         if connection is not None:
#             connection.close()
#             print("Database connection terminate!")


def check_pgsql_version(config_name):
    connection, cursor = create_connection(config_name)
    if connection is not None and cursor is not None:
        try:
            print("Postgresql database version: ")
            cursor.execute("SELECT version()")
            db_version = cursor.fetchone()
            print(db_version, "\n")
        except(Exception, psycopg2.DatabaseError) as err:
            print(err)
        finally:
            close_connection(connection, cursor)


def create_tables(config_name, db_query):
    print("create table ...")
    connection, cursor = create_connection(config_name)

    if connection is not None and cursor is not None:
        try:
            cursor.execute(db_query)
            connection.commit()
        except(Exception, psycopg2.DatabaseError) as err:
            print(err)
        finally:
            close_connection(connection, cursor)


def fill_the_table(config_name, csv_address, table_name, table_columns):
    df_temp = pd.read_csv(csv_address)
    df_temp_non_id = df_temp.iloc[:, 1:]
    list_of_tuples = [tuple(x) for x in df_temp_non_id.to_records(index=False)]

    records = ", ".join(["%s"] * len(list_of_tuples))
    insert_query = (
        f"""INSERT INTO {table_name} ({table_columns}) VALUES {records}"""
    )

    connection, cursor = create_connection(config_name)
    if connection is not None and cursor is not None:
        try:
            cursor.execute(insert_query, list_of_tuples)
            connection.commit()
        except(Exception, psycopg2.DatabaseError) as err:
            print(err)
        finally:
            close_connection(connection, cursor)


if __name__ == "__main__":
    # Create autoride
    create_db("postgresql", "autoride")
    print("AutoRide db is created!")
    # Create enums
    create_tables("autoride", table_query.CREATE_ENUM_PAYMENT_STATUS)
    create_tables("autoride", table_query.CREATE_ENUM_TRIP_STATUS)
    create_tables("autoride", table_query.CREATE_ENUM_VEHICLE_STATUS)
    print("Enums are created")

    # Create tables
    create_tables("autoride", table_query.CREATE_CUSTOMER_TABLE)
    create_tables("autoride", table_query.CREATE_VEHICLE_TABLE)
    create_tables("autoride", table_query.CREATE_PAYMENT_TABLE)
    create_tables("autoride", table_query.CREATE_TRIP_TABLE)

    print(" ----- Customer -----")
    fill_the_table("autoride",
                   "../csv/customer_info.csv",
                   "customer",
                   table_query.CUSTOMER_COLUMNS)
    print("Customer table is fill with information")
    print("-" * 10)
    print(" ----- vehicle -----")
    fill_the_table("autoride",
                   "../csv/vehicle_info.csv",
                   "vehicle",
                   table_query.VEHICLE_COLUMNS)
    print("vehicle table is fill with information")
    print("-" * 10)
    print(" ----- Payment -----")
    fill_the_table("autoride",
                   "../csv/payment_info.csv",
                   "payment",
                   table_query.PAYMENT_COLUMNS)
    print("payment table is fill with information")
    print("-" * 10)
    print(" ----- TRIP -----")
    fill_the_table("autoride",
                   "../csv/trip_info_psql.csv",
                   "trip",
                   table_query.TRIP_COLUMNS)
    print("trip table is fill with information")

