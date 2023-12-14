"""
    This scrip responsible to create postgresql database and their tables.
    Also, it can fill the tables with fake data which provided in csv file.
"""

import numpy as np
import pandas as pd
import psycopg2
from psycopg2.extensions import register_adapter, AsIs, Float
from rich.console import Console, Theme

from CreatePostgresql import table_query
from CreatePostgresql.config import config

# Convert numpy.NaN to a postgresql type.
register_adapter(np.int64, AsIs)
register_adapter(float, lambda f: AsIs('NULL') if np.isnan(f) else Float(f))

custom_theme = Theme({"success": "green", "error": "red", "msg": "cyan"})
console = Console(theme=custom_theme)


def create_connection(config_name: str = "autoride") -> tuple:
    """
    This function creates a connection to connect to Postgresql.
    If DatabaseError occur then return a tuple of None

    Parameter
    ---------
    config_name: str
        Database.ini section name.
    Return
        Tuple contains database connection and cursor
    ------

    """
    try:
        db_params = config(section=config_name)
        console.print("Connecting to PostgreSQL...", style="success")

        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        return connection, cursor

    except(Exception, psycopg2.DatabaseError) as err:
        console.print(err, style="error")
        return None, None


def close_connection(connection: "database connection", cursor: "database cursor") -> None:
    """
    This function closes the connection to the Postgresql database.

    Parameter
    ---------
    connection: object
        Postgresql connection object.
    cursor: object
        Postgresql cursor object.
    """

    if cursor is not None:
        cursor.close()
        console.print("Database cursor terminated.", style="cyan")

    if connection is not None:
        connection.close()
        console.print("Database connection terminated.", style="cyan")


def create_db(config_name: str, db_name: str) -> None:
    """
    This function get database.ini section name and
    database name then it creates a Postgresql database.

    Parameters
    ---------
    config_name: str
        Section name of database.ini
    db_name: str
        Database name which we want to create.

    Returns
    -------
    None
    """

    console.print("create db ...", style="success")
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
                console.print(f"Creating {db_name} database id Done!\n", style="success")
        except(Exception, psycopg2.DatabaseError) as err:
            console.print(err, style="error")
        finally:
            close_connection(connection, cursor)


def check_pgsql_version(config_name: str) -> None:
    """
    This function shows the version of Postgresql.

    Parameters
    ----------
    config_name: str
        Section name of database.ini
    """
    connection, cursor = create_connection(config_name)
    if connection is not None and cursor is not None:
        try:
            console.print("Postgresql database version: ", style="success")
            cursor.execute("SELECT version()")
            db_version = cursor.fetchone()
            print(db_version, "\n")
        except(Exception, psycopg2.DatabaseError) as err:
            console.print(err, style="error")
        finally:
            close_connection(connection, cursor)


def create_table(config_name: str, db_query: str) -> None:
    """
    This function runs our queries to create our tables.

    Parameters:
    -----------
    config_name: str
        Section name of database.ini
    db_query: str
        Postgresql query.

    """

    connection, cursor = create_connection(config_name)

    if connection is not None and cursor is not None:
        try:
            cursor.execute(db_query)
            connection.commit()
        except(Exception, psycopg2.DatabaseError) as err:
            console.print(err, style="error")
        finally:
            close_connection(connection, cursor)


def database_exist(config_name: str = "postgresql"):
    connection, cursor = create_connection(config_name)
    list_database = []

    if connection is not None and cursor is not None:
        try:
            cursor.execute("SELECT datname FROM pg_database;")
            list_database = cursor.fetchall()
        except(Exception, psycopg2.DatabaseError) as err:
            console.print(err, style="error")
        finally:
            close_connection(connection, cursor)
    return list_database


def fill_the_table(config_name: str, csv_address: str, table_name: str, table_columns: str) -> None:
    """
    This function fills the tables with fake information from csv files.

    Parameters
    ----------
    config_name: str
        Section name of database.ini
    csv_address: str
        Folder address of csv files.
    table_name: str
        Name of the table which we want to fill it.
    table_columns: str
        A sequence of column's table names.
    """

    # Read the csv file
    df_temp = pd.read_csv(csv_address)
    # df_temp_non_id = df_temp.iloc[:, 1:] # in some cases we do not need the id column.
    list_of_tuples = [tuple(x) for x in df_temp.to_records(index=False)]

    records = ", ".join(["%s"] * len(list_of_tuples))
    # Create the insert query.
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


def create_tables(config_name: str, enums: dict, tables: dict) -> None:
    for key, value in enums.items():
        console.print(f"Creating table ... {key}", style="msg")
        create_table(config_name, value)
        console.print(f"Empty table {key} is created!\n", style="success")

    for key, value in tables.items():
        console.print(f"Creating table {key}", style="msg")
        create_table(config_name, value)
        console.print(f"Empty table {key} is created\n", style="success")


def fill_tables(config_name: str):
    columns_dict = table_query.table_columns
    for key, value in columns_dict.items():
        fill_the_table("autoride",
                       "csv/" + key,
                       key.split("_")[0],
                       table_query.table_columns[key])
        console.print(f"Table {key.split('_')[0]} is fill with fake data.", style="success")


def create_empty_db() -> None:
    create_db("postgresql", "autoride")

    create_tables("autoride", table_query.enums_query, table_query.tables_query)


def create_and_fill_postgresql() -> None:
    create_db("postgresql", "autoride")

    create_tables("autoride", table_query.enums_query, table_query.tables_query)
    fill_tables("autoride")


if __name__ == "__main__":
    # Create autoride
    create_and_fill_postgresql()
