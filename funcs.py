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
    global cons
    cons = 0

    try:
        # 1. Account initialisieren
        account = tibber.Account(f"{TIBBER_API_KEY}")

        # 2. Prüfen, ob Häuser vorhanden sind (Sicherheitscheck)
        if not account.homes:
            print("Fehler: Keine Häuser im Tibber-Account gefunden oder API-Timeout bei der Abfrage.")
            return 0

        home = account.homes[0]

        # 3. Listener registrieren BEVOR der Feed startet
        @home.event("live_measurement")
        async def process_data(data):
            global cons
            if data and data.power:
                cons = data.power

        def my_exit_function(live_measurement_data):
            return live_measurement_data is not None and live_measurement_data.power > 0

        # 4. Feed starten
        home.start_live_feed(exit_condition=my_exit_function,
                             user_agent="UserAgent/0.0.1")

        print(f"Tibber {cons}")
        return cons

    except Exception as e:
        print(f"Kritischer Fehler in get_tibber: {e}")
        return 0