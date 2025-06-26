from classes import Room
from cred import ROOMS
from funcs import write_energydb, get_tibber

roomlist = []


for i in ROOMS:
    r = Room(name=i, dbtable=ROOMS[i]["dbtable"], ipaddress=ROOMS[i]["ipaddress"])
    roomlist.append(r)

for ro in roomlist:
    write_energydb(ro.dbtable, ro.consumption)


get_tibber()

write_energydb("smartmeter", get_tibber())