from cred import SHELLY_API_KEY
import requests


class Room:
    def __init__(self, name, dbtable, shellydeviceid):
        self.name = name
        self.dbtable = dbtable
        self.shellydeviceid = shellydeviceid
        self.consumption = self.get_shelly()

    def get_shelly(self):
        api_key = SHELLY_API_KEY
        parameters = {"id": self.shellydeviceid, "auth_key": api_key}

        base_url = "https://shelly-77-eu.shelly.cloud/device/status"

        response = requests.get(url=base_url, params=parameters)
        json_data = response.json()
        # print(json_data)
        consumption = float(json_data["data"]["device_status"]["switch:0"]["apower"])
        return consumption
