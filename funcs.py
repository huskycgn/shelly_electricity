from datetime import datetime
from cred import db_host, db_name, db_user, db_pass
import mariadb


def getutc():
    return datetime.utcnow()


def write_energydb(table, con) -> None:
    """Accepts and executes SQL Statements
    :param statement:
    :return:
    """
    connection = mariadb.connect(
        host=db_host, user=db_user, password=db_pass, database=db_name
    )
    statement = f"INSERT INTO {table} (time, consumption) VALUES('{getutc()}', {con});"

    cursor = connection.cursor()
    cursor.execute(statement)
    connection.commit()
    return None
