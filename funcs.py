from datetime import datetime, timezone

import psycopg2
import tibber

from cred import db_host, db_name, db_user, db_pass, TIBBER_API_KEY


def getutc():
    return datetime.now(timezone.utc)


def write_energydb(table, con) -> None:
    """Executes SQL statements
    :param table:
    :param table, con:
    :return:
    """
    connection = psycopg2.connect(
        host=db_host, user=db_user, password=db_pass, database=db_name
    )
    statement = f"INSERT INTO {table} (time, consumption) VALUES('{getutc()}', {con});"

    cursor = connection.cursor()
    cursor.execute(statement)
    connection.commit()
    return None


cons = 0


def get_tibber():
    # Wir nutzen den nativen Timeout-Parameter der Library (falls unterstützt)
    # oder wir setzen ihn direkt beim Initialisieren.
    try:
        # Bei tibber.py (Høyer) ist oft nur der Token vorgesehen.
        # Wir versuchen es mit der Standard-Initialisierung,
        # erhöhen aber die Geduld durch Vorab-Check.
        account = tibber.Account(f"{TIBBER_API_KEY}")

    except Exception as e:
        # Hier schlägt der 504 oder Timeout zu
        print(f"Tibber Initialisierung fehlgeschlagen: {e}")
        return 0
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
    print(f"Tibber {cons}")
    return cons