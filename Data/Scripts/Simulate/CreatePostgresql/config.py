"""
    This script read 'config.ini' and return database connection information.
"""
from configparser import ConfigParser


def config(filename: str = "CreatePostgresql/database.ini", section: str = "autoride") -> dict:
    """
    Parameters
    ----------
    filename: str
        Name of the .ini file.
    section: str
        specifies the section which needs to read.

    Return
    ------
    Python Dictionary
        Database connection information
    """
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} is not found in the {filename} file")

    return db
