from datetime import datetime, timezone

import psycopg2
import tibber

from cred import db_host, db_name, db_user, db_pass, TIBBER_API_KEY

import aiohttp
import asyncio


import socket

# --- IPv4-ONLY PATCH START ---
orig_getaddrinfo = socket.getaddrinfo

def patched_getaddrinfo(*args, **kwargs):
    responses = orig_getaddrinfo(*args, **kwargs)
    # Filtert alle IPv6 (AF_INET6) Adressen gnadenlos aus
    return [res for res in responses if res[0] == socket.AF_INET]

socket.getaddrinfo = patched_getaddrinfo
# --- IPv4-ONLY PATCH END ---


# Wir patchen den Standard-Timeout für ALLE aiohttp-Sessions
# Das zwingt die tibber-Library zu mehr Geduld
class ForceTimeout(aiohttp.ClientSession):
    def __init__(self, *args, **kwargs):
        if 'timeout' not in kwargs:
            kwargs['timeout'] = aiohttp.ClientTimeout(total=60, connect=30)
        super().__init__(*args, **kwargs)

# Wir "mogeln" der Library unsere geduldige Session unter
aiohttp.ClientSession = ForceTimeout



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