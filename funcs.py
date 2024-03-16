from datetime import datetime
from cred import db_host, db_name, db_user, db_pass, TIBBER_API_KEY
import mariadb
import tibber


def getutc():
    return datetime.utcnow()


def write_energydb(table, con) -> None:
    """Executes SQL statements
    :param table, con:
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


cons = 0


def get_tibber():
    account = tibber.Account(f"{TIBBER_API_KEY}")
    home = account.homes[0]

    @home.event("live_measurement")
    async def process_data(data):
        pass

    def my_exit_function(live_measurement_data):
        global cons
        cons = live_measurement_data.power
        return cons != 0

    # Now start retrieving live measurements
    home.start_live_feed(exit_condition=my_exit_function,
                         user_agent="UserAgent/0.0.1")
    return cons

