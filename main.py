from classes import Room
from cred import ROOMS
from funcs import getutc, write_energydb
import mariadb

roomlist = []

print(ROOMS)

for i in ROOMS:
    r = Room(name=i, dbtable=ROOMS[i]["dbtable"], shellydeviceid=ROOMS[i]["shellydeviceid"])
    roomlist.append(r)

for ro in roomlist:
    print(ro.name, ro.consumption, "Watt")
    write_energydb(ro.dbtable, ro.consumption)

