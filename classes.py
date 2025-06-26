from cred import SHELLY_API_KEY
import requests


class Room:
    def __init__(self, name, dbtable, ipaddress):
        self.name = name
        self.dbtable = dbtable
        self.ipaddress = ipaddress
        self.consumption = self.get_shelly_lan()

    def get_shelly_lan(self):
        base_url = f"http://{self.ipaddress}/rpc/Switch.GetStatus?id=0"
        response = requests.get(url=base_url)
        json_data = response.json()
        return json_data["apower"]